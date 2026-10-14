#!/usr/bin/env python3
"""
Documentary Engine v3 — rebuild_pipeline.py

Fixes from v1:
- Voiceover: en-US-AndrewMultilingualNeural at -3% (the Blackpink reference voice)
- Narration: tightened to cinematic short-form (180-200 wpm)
- Visuals: proper 16:9 framing (no black bars, no out-of-frame), Ken Burns on every shot
- Captions: edge-tts WordBoundary (word-level, matches audio exactly)
- Music: dramatic cinematic score (composed, not soft sine drone) + SFX
- Editing: 150-180 shots (vs 74), crossfades between shots, hard cuts at scene boundaries
- Output: 1920x1080, 30fps, h264 CRF16, AAC 192k, mastered to -14 LUFS

The pipeline is resumable. State persists to checkpoints/progress.json.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCREENPLAY_DIR = ROOT / "screenplay"
NARRATION_DIR = ROOT / "assets" / "narration_per_shot"
NARRATION_DIR.mkdir(parents=True, exist_ok=True)
STILLS_DIR = ROOT / "assets" / "stills"
STILLS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR = ROOT / "assets" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
BGM_DIR = ROOT / "assets" / "bgm"
BGM_DIR.mkdir(parents=True, exist_ok=True)
SHOTS_CACHE = ROOT / "checkpoints" / "shot_clips"
SHOTS_CACHE.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROGRESS = ROOT / "checkpoints" / "progress.json"
PROGRESS.parent.mkdir(parents=True, exist_ok=True)

# Voiceover: Blackpink reference (en-US-AndrewMultilingualNeural at -3%)
EDGE_VOICE = "en-US-AndrewMultilingualNeural"
EDGE_RATE = "-3%"

# Render specs (from last-stop-yt-engine assemble.py)
WIDTH = 1344
HEIGHT = 768  # 16:9 source (will upscale to 1920x1080)
FINAL_WIDTH = 1920
FINAL_HEIGHT = 1080
FPS = 30
CRF = 16  # high quality (was 23)
TARGET_LUFS = -14  # broadcast standard

# Shot timing
SILENCE_BETWEEN_SHOTS = 0.4  # seconds of silence between shots within a scene

STYLE_ANCHOR = (
    " Cinematic 16:9, painterly, slight film grain, cold blue-grey Pacific Northwest "
    "palette with warm amber lamp accents. Slight vignette. No text, no watermarks. "
    "Andrew Wyeth tempera feel crossed with cold-climate drama film. Photoreal but not "
    "plastic; skin has texture; wood has grain."
)


# === 1. SCREENPLAY PARSER ===
def parse_screenplay(text):
    scenes = []
    scene_blocks = re.split(r"^## SCENE (\d+)\s*—\s*(.+)$", text, flags=re.MULTILINE)
    i = 1
    while i < len(scene_blocks):
        num = int(scene_blocks[i])
        title = scene_blocks[i+1].strip()
        body = scene_blocks[i+2]
        scene = parse_scene_block(num, title, body)
        if scene:
            scenes.append(scene)
        i += 3
    return scenes


def parse_scene_block(num, title, body):
    scene = {"scene_id": f"S{num:02d}", "scene_number": num, "title": title}
    shots = []
    shot_pattern = re.compile(
        r"-\s+(S\d+_SH\d+)\s+\(([^,]+),\s*([^,]+),\s*(\d+)s\):\s*(.+?)(?=\n  - S|\n- \*\*|\n\*\*|$)",
        re.DOTALL
    )
    for sm in shot_pattern.finditer(body):
        prompt_text = re.sub(r"\s+", " ", sm.group(5).strip())
        shots.append({
            "shot_id": sm.group(1),
            "framing": sm.group(2).strip(),
            "camera": sm.group(3).strip(),
            "duration": float(sm.group(4)),
            "image_prompt": prompt_text + STYLE_ANCHOR,
            "motion": sm.group(3).strip(),
        })
    scene["shots"] = shots
    return scene


def parse_narration_script(text):
    narrations = {}
    blocks = re.split(r"\[SCENE (\d+)\s*—\s*[^\]]+\]", text)
    i = 1
    while i < len(blocks):
        num = int(blocks[i])
        narrations[f"S{num:02d}"] = blocks[i+1].strip()
        i += 2
    return narrations


def split_narration_into_shot_segments(narration, num_shots):
    """Split a scene's narration into `num_shots` segments, breaking on sentence boundaries."""
    sentences = re.split(r'(?<=[.!?])\s+', narration.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return [""] * num_shots
    if num_shots == 1:
        return [narration.strip()]
    total_words = sum(len(s.split()) for s in sentences)
    words_per_shot = total_words / num_shots
    segments = []
    cur = []
    cur_words = 0
    target = words_per_shot
    for i, s in enumerate(sentences):
        cur.append(s)
        cur_words += len(s.split())
        remaining_shots = num_shots - len(segments) - 1
        if remaining_shots > 0 and cur_words >= target:
            segments.append(" ".join(cur))
            cur = []
            cur_words = 0
            remaining_words = sum(len(x.split()) for x in sentences[i+1:])
            target = remaining_words / remaining_shots if remaining_shots > 0 else 0
    if cur:
        segments.append(" ".join(cur))
    while len(segments) < num_shots:
        segments.append("")
    while len(segments) > num_shots:
        last = segments.pop()
        segments[-1] = segments[-1] + " " + last
    return segments[:num_shots]


# === 2. EDGE TTS WITH WORDBOUNDARY ===
def call_edge_tts(text, mp3_path, words_json_path):
    """Use edge-tts with WordBoundary streaming for accurate per-word caption timing.
    Mirrors last-stop-yt-engine's pipeline/tts_all.py approach."""
    if not text.strip():
        # Empty segment — generate tiny silent mp3
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
             "-t", "0.5", "-c:a", "libmp3lame", "-b:a", "192k", str(mp3_path)],
            capture_output=True, timeout=30
        )
        words_json_path.write_text("[]", encoding="utf-8")
        return True

    # Use Python edge-tts API directly (not CLI) to capture WordBoundary events
    code = f"""
import asyncio, json, edge_tts

async def main():
    voice = "{EDGE_VOICE}"
    rate = "{EDGE_RATE}"
    text = {json.dumps(text)}
    words = []
    cm = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    with open({str(mp3_path)!r}, "wb") as f:
        async for chunk in cm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({{"t": chunk["offset"] / 1e7, "d": chunk["duration"] / 1e7, "w": chunk["text"]}})
    with open({str(words_json_path)!r}, "w") as f:
        json.dump(words, f, indent=1)
    print(f"OK: {{len(words)}} words")

asyncio.run(main())
"""
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    return r.returncode == 0 and mp3_path.exists() and mp3_path.stat().st_size > 1000


def get_audio_duration(path):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10
        )
        return float(r.stdout.strip())
    except Exception:
        return 0.0


# === 3. MAIN PIPELINE ===
def load_progress():
    if PROGRESS.exists():
        return json.loads(PROGRESS.read_text(encoding="utf-8"))
    return {"narration_done": [], "images_done": [], "shots_done": [], "final_done": False}


def save_progress(p):
    PROGRESS.write_text(json.dumps(p, indent=2), encoding="utf-8")


def main():
    print("=" * 70)
    print("  DOCUMENTARY ENGINE v3 — Blackpink voice + dramatic music + Ken Burns")
    print("=" * 70)

    print("\n[1/6] Parsing screenplay + splitting narration per shot...")
    sp_text = (SCREENPLAY_DIR / "screenplay.md").read_text(encoding="utf-8")
    scenes = parse_screenplay(sp_text)
    narr_text = (SCREENPLAY_DIR / "narration_script.txt").read_text(encoding="utf-8")
    narrations = parse_narration_script(narr_text)
    for s in scenes:
        sid = s["scene_id"]
        if sid in narrations:
            s["narration"] = narrations[sid]
        s["shot_narrations"] = split_narration_into_shot_segments(
            s.get("narration", ""), len(s["shots"])
        )
    total_shots = sum(len(s["shots"]) for s in scenes)
    print(f"  Parsed {len(scenes)} scenes, {total_shots} shots")

    progress = load_progress()

    # Stage 1: Generate per-shot narration with edge-tts (Blackpink voice)
    if "--stage" not in sys.argv or "narration" in sys.argv:
        print("\n[2/6] Generating per-shot narration with Edge TTS (Blackpink voice)...")
        narration_done = set(progress.get("narration_done", []))
        max_new = int(sys.argv[sys.argv.index("--narration-max")+1]) if "--narration-max" in sys.argv else None
        only = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
        generated = 0
        for s in scenes:
            for i, shot in enumerate(s["shots"]):
                shot_id = shot["shot_id"]
                if only and shot_id != only:
                    continue
                if shot_id in narration_done:
                    continue
                if max_new is not None and generated >= max_new:
                    break
                mp3 = NARRATION_DIR / f"{shot_id}.mp3"
                words_json = NARRATION_DIR / f"{shot_id}.words.json"
                text = s["shot_narrations"][i] if i < len(s["shot_narrations"]) else ""
                ok = call_edge_tts(text, mp3, words_json)
                if ok:
                    narration_done.add(shot_id)
                    progress["narration_done"] = sorted(narration_done)
                    save_progress(progress)
                    generated += 1
                    print(f"  [PASS] {shot_id} ({get_audio_duration(mp3):.2f}s)")
                else:
                    print(f"  [FAIL] {shot_id}")
                time.sleep(0.3)
            if max_new is not None and generated >= max_new:
                break
        print(f"\n  Narration: {len(narration_done)}/{total_shots} done")

    # Stage 2: Build timeline with actual audio durations
    print("\n[3/6] Building timeline with actual audio durations...")
    timeline = {"scenes": [], "voice": EDGE_VOICE, "rate": EDGE_RATE}
    cumulative_t = 0.0
    for s in scenes:
        scene_shots = []
        scene_start = cumulative_t
        for i, shot in enumerate(s["shots"]):
            shot_id = shot["shot_id"]
            mp3 = NARRATION_DIR / f"{shot_id}.mp3"
            audio_dur = get_audio_duration(mp3) if mp3.exists() else 3.0
            shot_duration = audio_dur + SILENCE_BETWEEN_SHOTS
            scene_shots.append({
                "shot_id": shot_id,
                "duration": shot_duration,
                "audio_duration": audio_dur,
                "start_time": cumulative_t,
                "image_path": str(IMAGES_DIR / f"{shot_id}.png"),
                "audio_path": str(mp3),
                "words_path": str(NARRATION_DIR / f"{shot_id}.words.json"),
                "narration": s["shot_narrations"][i] if i < len(s["shot_narrations"]) else "",
                "image_prompt": shot["image_prompt"],
                "motion": shot.get("motion", "static"),
            })
            cumulative_t += shot_duration
        timeline["scenes"].append({
            "scene_id": s["scene_id"],
            "scene_number": s["scene_number"],
            "title": s["title"],
            "start_time": scene_start,
            "end_time": cumulative_t,
            "shots": scene_shots,
        })
    timeline["total_duration_seconds"] = cumulative_t
    (SCREENPLAY_DIR / "timeline_v3.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    print(f"  Total duration: {cumulative_t:.1f}s ({cumulative_t/60:.1f} min)")

    # Stage 3: Build cumulative word-level subtitles from edge-tts WordBoundary
    print("\n[4/6] Building word-level subtitles from edge-tts WordBoundary...")
    all_subs = []
    sub_index = 1
    time_offset = 0.0
    for s in scenes:
        for i, shot in enumerate(s["shots"]):
            shot_id = shot["shot_id"]
            words_path = NARRATION_DIR / f"{shot_id}.words.json"
            mp3 = NARRATION_DIR / f"{shot_id}.mp3"
            audio_dur = get_audio_duration(mp3) if mp3.exists() else 0.0
            if not words_path.exists():
                time_offset += audio_dur + SILENCE_BETWEEN_SHOTS
                continue
            try:
                words = json.loads(words_path.read_text(encoding="utf-8"))
            except Exception:
                words = []
            # Group words into subtitle chunks of 5-8 words each
            chunk_size = 6
            for j in range(0, len(words), chunk_size):
                chunk = words[j:j+chunk_size]
                if not chunk:
                    continue
                start = chunk[0]["t"] + time_offset
                end = chunk[-1]["t"] + chunk[-1]["d"] + time_offset
                text = " ".join(w["w"] for w in chunk)
                all_subs.append({
                    "index": sub_index,
                    "start": start,
                    "end": end,
                    "text": text,
                })
                sub_index += 1
            time_offset += audio_dur + SILENCE_BETWEEN_SHOTS

    srt_content = format_srt(all_subs)
    (SCREENPLAY_DIR / "subtitles_v3.srt").write_text(srt_content, encoding="utf-8")
    (SCREENPLAY_DIR / "subtitles_v3.ass").write_text(srt_to_ass(all_subs), encoding="utf-8")
    print(f"  Wrote subtitles_v3.srt + .ass ({len(all_subs)} entries)")

    # Stage 4: Generate images (if needed)
    if "--stage" not in sys.argv or "images" in sys.argv:
        print("\n[5/6] Generating scene images (this is the slow part)...")
        print("  (Use scripts/06_generate_images.py separately to control batch size)")

    # Stage 5: Render final video (this happens in render_final.py)
    if "--stage" not in sys.argv or "render" in sys.argv:
        print("\n[6/6] Render final video — use scripts/render_final.py")
        print("  This will:")
        print("  - Render each shot with Ken Burns motion + audio")
        print("  - Concat with crossfades")
        print("  - Generate dramatic music score")
        print("  - Mix music + narration with sidechain ducking")
        print("  - Master to -14 LUFS")
        print("  - Burn word-level subtitles")
        print("  - Export 1920x1080 CRF16")

    print("\n" + "=" * 70)
    print("  Pipeline setup complete. Run scripts in this order:")
    print("  1. python3 scripts/rebuild_pipeline.py --stage narration")
    print("  2. python3 scripts/06_generate_images.py")
    print("  3. python3 scripts/render_final.py")
    print("=" * 70)


def format_srt(entries):
    def fmt(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []
    for e in entries:
        lines.append(str(e["index"]))
        lines.append(f"{fmt(e['start'])} --> {fmt(e['end'])}")
        lines.append(e["text"])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def srt_to_ass(entries):
    """Convert SRT entries to ASS format with cinematic styling."""
    def fmt_ass(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        cs = int((t - int(t)) * 100)
        return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "WrapStyle: 2",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Noto Sans,52,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,1,0,0,0,100,100,0,0,1,3,1,2,80,80,60,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for e in entries:
        # Escape text for ASS
        text = e["text"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        lines.append(
            f"Dialogue: 0,{fmt_ass(e['start'])},{fmt_ass(e['end'])},Default,,0,0,0,,{text}"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
