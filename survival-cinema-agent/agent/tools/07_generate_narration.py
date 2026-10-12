#!/usr/bin/env python3
"""Phase 8 — Generate narration audio. Default: z-ai tts CLI."""
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path.cwd()
MAN = ROOT/"screenplay"/"scene_manifest.json"
CH = ROOT/"assets"/"narration_chunks"; CH.mkdir(parents=True,exist_ok=True)
NAR = ROOT/"assets"/"narration"; NAR.mkdir(parents=True,exist_ok=True)
AMAN = ROOT/"assets"/"audio_manifest.json"
VOICE = "tongtong"; SPEED = 1.0; RETRIES = 3
def call_tts(text, out, voice=VOICE, speed=SPEED):
    cmd = ["z-ai","tts","--input",text,"--output",str(out),"--voice",voice,"--speed",str(speed),"--format","wav"]
    try:
        r = subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        return r.returncode==0 and out.exists() and out.stat().st_size>5000, (r.stdout or "")+(r.stderr or "")
    except Exception as e: return False, f"EXCEPTION {e}"
def dur(p):
    try:
        r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(p)],capture_output=True,text=True,timeout=10)
        return float(r.stdout.strip())
    except: return 0.0
def load_scenes(): return json.loads(MAN.read_text(encoding="utf-8"))["scenes"]
def main():
    scenes = load_scenes()
    if "--scene-id" in sys.argv:
        only = sys.argv[sys.argv.index("--scene-id")+1]
        scenes = [s for s in scenes if s["scene_id"]==only]
    p=f=s=0
    for sc in scenes:
        out = CH/f"{sc['scene_id']}.wav"
        if out.exists() and out.stat().st_size>5000: s+=1; continue
        msg=""
        for a in range(1,RETRIES+1):
            ok, m = call_tts(sc["narration"], out)
            if ok: p+=1; print(f"  [PASS] {sc['scene_id']}"); break
            msg=m; time.sleep(2*a)
        else: f+=1; print(f"  [FAIL] {sc['scene_id']}")
        time.sleep(0.5)
    all_scenes = load_scenes()
    chunks = [CH/f"{s['scene_id']}.wav" for s in all_scenes if (CH/f"{s['scene_id']}.wav").exists()]
    lf = CH/"_concat_list.txt"
    with open(lf,"w") as f:
        for c in chunks: f.write(f"file '{c}'\n")
    out = NAR/"narration.wav"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lf),"-ar","44100","-ac","1","-c:a","pcm_s16le",str(out)],capture_output=True,timeout=120)
    meta = [{"scene_id":s["scene_id"],"duration_seconds":dur(CH/f"{s['scene_id']}.wav")} for s in all_scenes if (CH/f"{s['scene_id']}.wav").exists()]
    am = {"voice":VOICE,"speed":SPEED,"chunks":meta,"narration_wav":str(out),"narration_duration_seconds":dur(out)}
    AMAN.write_text(json.dumps(am,indent=2),encoding="utf-8")
    print(f"\n{p} PASS, {f} FAIL, {s} SKIP. Total: {dur(out):.2f}s")
if __name__=="__main__": main()
