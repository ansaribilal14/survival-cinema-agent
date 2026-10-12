#!/usr/bin/env python3
"""Phase 4 — Story development scaffold."""
import json, re, sys
from pathlib import Path
ROOT = Path.cwd(); SD = ROOT / "story_development"; SD.mkdir(parents=True, exist_ok=True)
def parse_idea(path):
    if not path.exists(): return {}
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\*\*([^*:]+):\*\*\s*(.*)$", line)
        if m: fields[m.group(1).strip().lower().replace(" ","_")] = m.group(2).strip()
    return fields
def main():
    idea_path = Path(sys.argv[1]) if len(sys.argv)>1 else Path("story_idea.md")
    idea = parse_idea(idea_path)
    print(f"[Phase 4] Story idea: {len(idea)} fields")
    (SD/"story_idea_parsed.json").write_text(json.dumps(idea,indent=2),encoding="utf-8")
    files = [("concept_candidates.md","3 concept candidates, 8-dim evaluation"),
             ("story_bible.md","Full story design"),
             ("complete_story.md","Full story ~3-5k words"),
             ("character_bible.json","JSON: 5+ characters"),
             ("world_bible.md","Geography, climate, history"),
             ("continuity_rules.md","Per-scene continuity"),
             ("originality_audit.md","Per-dimension audit")]
    for fn, desc in files:
        p = SD / fn
        if p.exists() and p.stat().st_size > 200: print(f"  SKIP {fn}"); continue
        p.write_text(f"# TODO: {fn}\n\n> {desc}\n\nAgent fills this in.\n", encoding="utf-8")
        print(f"  CREATED {fn}")
if __name__=="__main__": main()
