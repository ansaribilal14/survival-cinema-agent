#!/usr/bin/env python3
"""Phase 9 — Render final video. 3-pass FFmpeg pipeline."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path.cwd()
TL = json.loads((ROOT/"screenplay"/"timeline.json").read_text(encoding="utf-8"))
SCENES = TL["scenes"]
IMG = ROOT/"assets"/"images"
NAR = ROOT/"assets"/"narration_chunks"
SHOTS = ROOT/"checkpoints"/"shot_clips"; SHOTS.mkdir(parents=True,exist_ok=True)
SCache = ROOT/"checkpoints"/"scene_videos"; SCache.mkdir(parents=True,exist_ok=True)
OUT = ROOT/"output"; OUT.mkdir(parents=True,exist_ok=True)
PROG = ROOT/"checkpoints"/"render_progress.json"
W,H = 1344,768; FW,FH = 1920,1080; FPS = 30; PAD = 1.0
SRT = ROOT/"screenplay"/"subtitles.srt"
FINAL = OUT/"final.mp4"
def run(cmd, t=600):
    try:
        r = subprocess.run(cmd,capture_output=True,text=True,timeout=t)
        return r.returncode==0, (r.stdout or "")+(r.stderr or "")
    except Exception as e: return False, f"EXCEPTION {e}"
def dur(p):
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True,timeout=10)
        return float(r.stdout.strip())
    except: return 0.0
def load_p():
    if PROG.exists(): return json.loads(PROG.read_text(encoding="utf-8"))
    return {"shots_done":[],"scenes_done":[],"final_done":False}
def save_p(p): PROG.write_text(json.dumps(p,indent=2),encoding="utf-8")
def render_shot(shot, d):
    sid = shot["shot_id"]; ip = IMG/f"{sid}.png"; op = SHOTS/f"{sid}.mp4"
    sc = SHOTS/f"{sid}.txt"
    if not ip.exists(): return False
    if op.exists() and sc.exists() and sc.read_text().strip()==f"{d:.3f}": return True
    f = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black"
    cmd = ["ffmpeg","-y","-loop","1","-framerate",str(FPS),"-t",f"{d:.3f}","-i",str(ip),"-vf",f,"-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-r",str(FPS),"-an",str(op)]
    ok,_ = run(cmd,120)
    if ok: sc.write_text(f"{d:.3f}")
    return ok
def render_scene(scene, ds):
    sid = scene["scene_id"]
    cl = SHOTS/f"{sid}_concat.txt"; sv = SCache/f"{sid}_video.mp4"; sf = SCache/f"{sid}_full.mp4"
    nar = NAR/f"{sid}.wav"
    for i,shot in enumerate(scene["shots"]):
        if shot["shot_id"] in load_p()["shots_done"]: continue
        if not render_shot(shot, ds[i]): return False
    with open(cl,"w") as f:
        for shot in scene["shots"]: f.write(f"file '{SHOTS/(shot['shot_id']+'.mp4')}'\n")
    ok,_ = run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cl),"-c","copy",str(sv)],120)
    if not ok: ok,_ = run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cl),"-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-an",str(sv)],180)
    pa = SHOTS/f"{sid}_padded.wav"
    if nar.exists(): run(["ffmpeg","-y","-i",str(nar),"-af",f"apad=pad_dur={PAD}","-c:a","pcm_s16le",str(pa)],60)
    else: run(["ffmpeg","-y","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono","-t",f"{sum(ds):.3f}","-c:a","pcm_s16le",str(pa)],30)
    ok,_ = run(["ffmpeg","-y","-i",str(sv),"-i",str(pa),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(sf)],120)
    return ok
def render_final():
    svs = []
    for s in SCENES:
        p = SCache/f"{s['scene_id']}_full.mp4"
        if not p.exists(): return False
        svs.append(p)
    cl = ROOT/"checkpoints"/"scene_concat_list.txt"
    with open(cl,"w") as f:
        for p in svs: f.write(f"file '{p}'\n")
    inter = OUT/"intermediate.mp4"
    print("  Step 1: concat scenes")
    ok,_ = run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cl),"-c","copy",str(inter)],180)
    if not ok: run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(cl),"-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",str(inter)],600)
    print("  Step 2: upscale to 1920x1080")
    ihd = OUT/"intermediate_hd.mp4"
    ok,_ = run(["ffmpeg","-y","-i",str(inter),"-vf",f"scale={FW}:{FH}:flags=fast_bilinear","-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-c:a","copy",str(ihd)],600)
    if not ok: ihd = inter
    print("  Step 3: burn subtitles")
    ok,_ = run(["ffmpeg","-y","-i",str(ihd),"-vf",f"subtitles='{SRT}':force_style='FontName=Noto Sans,FontSize=20,PrimaryColour=&HFFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=40'","-c:v","libx264","-preset","ultrafast","-crf","23","-pix_fmt","yuv420p","-c:a","copy",str(FINAL)],900)
    return ok
def main():
    prog = load_p()
    stage = sys.argv[1] if len(sys.argv)>1 else "all"
    if stage in ("shots","all"):
        print("=== Stage 1: render shot clips ===")
        for scene in SCENES:
            nar = NAR/f"{scene['scene_id']}.wav"
            nd = dur(nar) if nar.exists() else 0
            st = nd+PAD; ns = len(scene["shots"]); ps = st/ns
            ds = [ps]*ns; ds[-1] += st-sum(ds)
            for i,shot in enumerate(scene["shots"]):
                if shot["shot_id"] in prog["shots_done"]: continue
                if render_shot(shot, ds[i]):
                    prog["shots_done"].append(shot["shot_id"]); save_p(prog)
                    print(f"  [PASS] {shot['shot_id']}")
    if stage in ("scenes","all"):
        print("\n=== Stage 2: render scene videos ===")
        prog = load_p()
        for scene in SCENES:
            sid = scene["scene_id"]
            if sid in prog["scenes_done"]: continue
            nar = NAR/f"{sid}.wav"; nd = dur(nar) if nar.exists() else 0
            st = nd+PAD; ns = len(scene["shots"]); ps = st/ns
            ds = [ps]*ns; ds[-1] += st-sum(ds)
            if not all(sh["shot_id"] in prog["shots_done"] for sh in scene["shots"]): continue
            if render_scene(scene, ds):
                prog["scenes_done"].append(sid); save_p(prog)
                print(f"  [PASS] {sid}")
    if stage in ("final","all"):
        print("\n=== Stage 3: final concat + subtitles ===")
        if render_final():
            print(f"\n✓ Final: {FINAL} ({dur(FINAL):.2f}s)")
            prog["final_done"]=True; save_p(prog)
        else: print("\n✗ Final render failed")
if __name__=="__main__": main()
