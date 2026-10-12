#!/usr/bin/env python3
"""Phase 7 — Generate scene-by-scene AI images. Default: z-ai image CLI. Edit call_image_provider to swap."""
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path.cwd()
TIMELINE = ROOT/"screenplay"/"timeline.json"
IMAGES = ROOT/"assets"/"images"; IMAGES.mkdir(parents=True,exist_ok=True)
PROG = ROOT/"checkpoints"/"image_progress.json"; PROG.parent.mkdir(parents=True,exist_ok=True)
MANIFEST = ROOT/"assets"/"asset_manifest.json"
ANCHOR = " Cinematic 16:9, painterly, slight film grain, cold blue-grey Pacific Northwest palette with warm amber lamp accents. Slight vignette. No text, no watermarks. Andrew Wyeth tempera feel crossed with cold-climate drama film. Photoreal but not plastic; skin has texture; wood has grain."
RETRIES = 3; SLEEP = 1.5
def call_image(prompt, out, size="1344x768"):
    cmd = ["z-ai","image","--prompt",prompt,"--output",str(out),"--size",size]
    try:
        r = subprocess.run(cmd,capture_output=True,text=True,timeout=180)
        return r.returncode==0 and out.exists() and out.stat().st_size>5000, (r.stdout or "")+(r.stderr or "")
    except Exception as e: return False, f"EXCEPTION {e}"
def load_tl(): return json.loads(TIMELINE.read_text(encoding="utf-8"))
def load_p():
    if PROG.exists(): return json.loads(PROG.read_text(encoding="utf-8"))
    return {"shots":{}}
def save_p(p): PROG.write_text(json.dumps(p,indent=2),encoding="utf-8")
def gen(shot, scene, prog):
    sid = shot["shot_id"]; out = IMAGES/f"{sid}.png"
    if sid in prog["shots"] and prog["shots"][sid].get("status")=="PASS": return "SKIP"
    prompt = shot.get("image_prompt","")+ANCHOR; msg=""
    for a in range(1,RETRIES+1):
        ok, m = call_image(prompt, out)
        if ok:
            prog["shots"][sid] = {"status":"PASS","path":str(out),"size_bytes":out.stat().st_size,"scene_id":scene["scene_id"],"attempts":a}
            save_p(prog); return "PASS"
        msg = m; time.sleep(2*a)
    prog["shots"][sid] = {"status":"FAIL","scene_id":scene["scene_id"],"attempts":RETRIES,"last_error":msg[:500]}
    save_p(prog); return "FAIL"
def main():
    tl = load_tl(); prog = load_p()
    mx = int(sys.argv[sys.argv.index("--max")+1]) if "--max" in sys.argv else None
    osid = sys.argv[sys.argv.index("--scene-id")+1] if "--scene-id" in sys.argv else None
    t=p=f=s=0
    for scene in tl["scenes"]:
        if osid and scene["scene_id"]!=osid: continue
        for shot in scene["shots"]:
            t+=1
            if mx is not None and (p+f)>=mx: continue
            st = gen(shot, scene, prog)
            if st=="PASS": p+=1; print(f"  [PASS] {shot['shot_id']}")
            elif st=="SKIP": s+=1
            else: f+=1; print(f"  [FAIL] {shot['shot_id']}")
            time.sleep(SLEEP)
    m = {"schema":"survival_cinema.asset_manifest.v1","total":t,"passed":p,"failed":f,"skipped":s,"shots":list(prog["shots"].values())}
    MANIFEST.write_text(json.dumps(m,indent=2),encoding="utf-8")
    print(f"\n{p} PASS, {f} FAIL, {s} SKIP")
if __name__=="__main__": main()
