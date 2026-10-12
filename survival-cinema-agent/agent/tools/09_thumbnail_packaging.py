#!/usr/bin/env python3
"""Phase 10 — Thumbnail + YouTube packaging."""
import json, shutil, subprocess
from pathlib import Path
ROOT = Path.cwd(); OUT = ROOT/"output"; OUT.mkdir(parents=True,exist_ok=True)
TL = json.loads((ROOT/"screenplay"/"timeline.json").read_text(encoding="utf-8"))
SRT = ROOT/"screenplay"/"subtitles.srt"
def call_image(prompt, out, size="1344x768"):
    cmd = ["z-ai","image","--prompt",prompt,"--output",str(out),"--size",size]
    try:
        r = subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        return r.returncode==0 and out.exists()
    except: return False
def main():
    print("[Phase 10] Generating thumbnail...")
    prompt = ("Cinematic YouTube thumbnail for a survival thriller short film. "
              "A young 22-year-old woman in a too-large navy wool lighthouse-keeper coat and a red knit cap, "
              "stands on the iron catwalk of a 70-foot white-and-black lighthouse at night in a storm. "
              "She holds a brass crank handle. Behind her, the rotating Fresnel lens emits a warm amber light "
              "that sweeps through heavy rain and fog. Cold blue-grey night palette with warm amber lamp accents. "
              "Slight film grain, painterly, atmospheric, 16:9. No text, no watermarks.")
    tp = OUT/"thumbnail.png"
    if not call_image(prompt, tp):
        fb = ROOT/"assets"/"images"/"S21_SH02.png"
        if fb.exists(): shutil.copy(fb, tp)
    if SRT.exists(): shutil.copy(SRT, OUT/"final_subtitles.srt")
    td = sum(sh["duration"] for s in TL["scenes"] for sh in s["shots"])
    meta = {
        "schema":"survival_cinema.video_metadata.v1",
        "primary_title":"<Story Title> — A Survival Thriller Short Film",
        "title_alternatives":["<Story Title> (Original Survival Thriller Short Film)","<hook variant>","<Story Title>: An Original YA Survival Thriller"],
        "short_description":"An original 12-minute YA survival thriller short film. <One-sentence hook.>",
        "long_description":"<Full description with chapters, AI disclosure, rights summary.>",
        "chapter_timestamps":[],
        "search_keywords":["survival thriller","young adult survival","short film","female protagonist thriller"],
        "category":"Film & Animation","visibility":"private","language":"en",
        "ai_generated_content_disclosure":{"imagery":"AI-generated","audio":"AI-generated TTS","screenplay":"original human-authored work","disclosure_required":True,"disclosure_label":"Some scenes were generated with AI tools. The screenplay, story, and characters are entirely original human work."},
        "production_metadata":{"total_runtime_seconds":td,"scene_count":len(TL["scenes"]),"shot_count":sum(len(s["shots"]) for s in TL["scenes"]),"image_resolution":"1920x1080","fps":30,"video_codec":"h264","audio_codec":"aac 192k"}
    }
    (OUT/"video_metadata.json").write_text(json.dumps(meta,indent=2),encoding="utf-8")
    print(f"  Thumbnail: {tp}")
    print(f"  Metadata: {OUT/'video_metadata.json'}")
    print(f"  Agent must edit video_metadata.json to fill in actual title/description/keywords.")
if __name__=="__main__": main()
