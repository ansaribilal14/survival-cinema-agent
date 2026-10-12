#!/usr/bin/env python3
"""Phase 1-2 — Acquire and verify three public-domain reference works from Project Gutenberg."""
import json, re, subprocess
from pathlib import Path
ROOT = Path.cwd()
REF_DIR = ROOT / "reference_library"; REF_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR = ROOT / "reports"; REP_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_REFS = [
    {"id":"story_01","slug":"pym","title":"The Narrative of Arthur Gordon Pym of Nantucket","author":"Edgar Allan Poe","year":1838,"category":"wilderness_survival","gutenberg_id":2149,"source_url":"https://www.gutenberg.org/cache/epub/2149/pg2149.txt","license":"Public domain (US) - Project Gutenberg","selection_rationale":"Poe's only complete novel. First-person survival narrative involving shipwreck, mutiny, starvation, exposure, and an expedition into the Antarctic. Long-form (~100k words)."},
    {"id":"story_02","slug":"scarlet_plague","title":"The Scarlet Plague","author":"Jack London","year":1915,"category":"apocalyptic_survival","gutenberg_id":21970,"source_url":"https://www.gutenberg.org/cache/epub/21970/pg21970.txt","license":"Public domain (US) - Project Gutenberg","selection_rationale":"Post-pandemic apocalyptic novella (~20k words) set 60 years after a scarlet plague. Useful for societal-collapse mechanics and cultural forgetting."},
    {"id":"story_03","slug":"moreau","title":"The Island of Doctor Moreau","author":"H. G. Wells","year":1896,"category":"psychological_survival_thriller","gutenberg_id":159,"source_url":"https://www.gutenberg.org/cache/epub/159/pg159.txt","license":"Public domain (US) - Project Gutenberg","selection_rationale":"Psychological survival thriller (~44k words) with strong suspense, betrayal, shifting alliances, and a midpoint reveal that is a moral fact rather than a monster."},
]
def strip_gutenberg(text):
    for m in ["*** START OF THE PROJECT GUTENBERG EBOOK","*** START OF THIS PROJECT GUTENBERG EBOOK","***START OF THE PROJECT GUTENBERG EBOOK"]:
        i = text.find(m)
        if i >= 0: text = text[i+len(m):]; break
    for m in ["*** END OF THE PROJECT GUTENBERG EBOOK","*** END OF THIS PROJECT GUTENBERG EBOOK","***END OF THE PROJECT GUTENBERG EBOOK"]:
        i = text.find(m)
        if i >= 0: text = text[:i]; break
    return text.strip()
def wc(t): return len(re.findall(r"\b[\w'-]+\b", t))
def download(url, dest):
    try:
        subprocess.run(["curl","-sSL",url,"-o",str(dest)],timeout=120,check=True)
        return dest.exists() and dest.stat().st_size > 10000
    except Exception: return False
def main():
    print(f"[Phase 1-2] Acquiring {len(DEFAULT_REFS)} reference works...")
    entries = []
    for ref in DEFAULT_REFS:
        raw = REF_DIR / f"{ref['id']}_{ref['slug']}_raw.txt"
        clean = REF_DIR / f"{ref['id']}_{ref['slug']}_clean.txt"
        if clean.exists() and clean.stat().st_size > 10000:
            print(f"  [{ref['id']}] SKIP")
            ct = clean.read_text(encoding="utf-8",errors="replace")
        else:
            print(f"  [{ref['id']}] Downloading {ref['title']}...")
            if not download(ref["source_url"], raw):
                entries.append({**ref,"acquisition_status":"FAILED"}); continue
            rt = raw.read_text(encoding="utf-8",errors="replace")
            ct = strip_gutenberg(rt)
            clean.write_text(ct, encoding="utf-8")
        n = wc(ct); ch = len(re.findall(r"^\s*(CHAPTER\s+[IVXLCDM]+\b.*|CHAPTER\s+\d+\b.*)$", ct, re.MULTILINE))
        entries.append({**ref,"clean_word_count":n,"detected_chapters":ch,"acquisition_status":"PASS" if n>5000 else "PARTIAL"})
        print(f"  [{ref['id']}] PASS — {n} words, {ch} chapters")
    manifest = {"schema":"survival_cinema.reference_library.manifest.v1","entries":entries,"total_stories":len(entries),"all_pass":all(e.get("acquisition_status")=="PASS" for e in entries)}
    (REF_DIR/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(f"Manifest: {REF_DIR/'manifest.json'}")
if __name__=="__main__": main()
