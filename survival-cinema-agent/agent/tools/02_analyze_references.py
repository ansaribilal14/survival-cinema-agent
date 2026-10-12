#!/usr/bin/env python3
"""Phase 3 — Analyze references (scaffold). The agent (LLM) fills the analysis files."""
from pathlib import Path
ROOT = Path.cwd(); AD = ROOT / "reference_analysis"; AD.mkdir(parents=True, exist_ok=True)
FILES = ["reference_analysis_01.md","reference_analysis_02.md","reference_analysis_03.md",
         "narrative_techniques.json","survival_mechanics.json","character_arc_patterns.json",
         "pacing_and_scene_patterns.json","comparative_analysis.md"]
def main():
    print("[Phase 3] Scaffolding reference_analysis/...")
    for f in FILES:
        p = AD / f
        if p.exists() and p.stat().size > 200: print(f"  SKIP {f}"); continue
        p.write_text(f"# TODO: {f}\n\n<The agent fills this in by reading the reference texts.>\n", encoding="utf-8")
        print(f"  CREATED {f}")
if __name__=="__main__": main()
