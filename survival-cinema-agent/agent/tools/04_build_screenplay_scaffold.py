#!/usr/bin/env python3
"""Phase 5 — Build screenplay scaffold."""
from pathlib import Path
ROOT = Path.cwd(); SP = ROOT/"screenplay"; SP.mkdir(parents=True,exist_ok=True)
SC = ROOT/"scripts"; SC.mkdir(parents=True,exist_ok=True)
def main():
    print("[Phase 5] Scaffolding screenplay/...")
    stub = '''#!/usr/bin/env python3
"""SCHEMA GENERATOR — copy from examples/keeper_of_cape_vespers/scripts/build_screenplay.py
The agent defines SCENES (list of 22 scene dicts) here, then runs this script
to generate: screenplay.md, scene_manifest.json, narration_script.txt, subtitles.srt,
chapter_markers.json, timeline.json.
"""
SCENES = []
'''
    (SC/"build_screenplay.py").write_text(stub, encoding="utf-8")
    print(f"  Created scripts/build_screenplay.py (agent must fill SCENES)")
if __name__=="__main__": main()
