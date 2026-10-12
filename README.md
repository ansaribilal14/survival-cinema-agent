# Emergency Backup — Survival Cinema Project

This directory contains the recovered text source files for the Survival Cinema project, recovered from conversation memory after the local filesystem was wiped and the GitHub account was suspended.

## What's in this backup

### survival_cinema/ — The original film project (text source files)
- `complete_story.md` — the full story (~4500 words)
- `story_bible.md` — story design document
- `concept_candidates.md` — 3 concept candidates with evaluation
- `character_bible.json` — 5+ characters with full descriptions
- `world_bible.md` — geography, climate, history, the secret
- `continuity_rules.md` — per-scene continuity rules
- `originality_audit.md` — originality audit vs references
- `screenplay.md` — full 22-scene screenplay with 74 shots
- `narration_script.txt` — the narration text (1950 words)
- `style_bible.md` — visual style guide
- `reference_analysis_01/02/03.md` — analyses of Poe, London, Wells
- `narrative_techniques.json`, `survival_mechanics.json`, `character_arc_patterns.json`, `pacing_and_scene_patterns.json`, `comparative_analysis.md`
- `narrative_analysis.md`, `continuity_report.md`, `quality_report.md`, `rights_and_provenance.md`, `production_failures.md`, `acquisition_report.md` — 6 QA reports
- `video_metadata.json` — YouTube metadata package
- `manifest.json`, `config.json`, `PROJECT_STATUS.md`, `WORKLOG.md`

### survival-cinema-agent/ — The agentic framework
- `README.md`, `LICENSE` (MIT), `.gitignore`, `STORY_IDEA_TEMPLATE.md`
- `agent/SYSTEM_PROMPT.md` — the master directive
- `agent/pipeline.sh` — the 11-phase runner
- `agent/tools/01-10_*.py` — one script per phase
- `docs/ARCHITECTURE.md`, `INPUT_SPEC.md`, `PHASES.md`, `OUTPUTS.md`, `CUSTOMIZATION.md`, `QUICKSTART.md`
- `examples/keeper_of_cape_vespers/story_idea.md` — the demo input
- `site/index.html` — the GitHub Pages landing page

## What's NOT in this backup (binaries lost)

The following binary artifacts were AI-generated during the original session and cannot be recovered from conversation memory:
- `output/final.mp4` (110 MB, the finished film)
- `output/thumbnail.png`
- `assets/images/*.png` (74 scene images, 7.3 MB total)
- `assets/narration_chunks/*.wav` (22 narration audio chunks)
- `assets/narration/narration.wav`
- `site/assets/demo-thumbnail.jpg`

## How to regenerate the binaries

1. Restore this backup to a working directory.
2. Ensure `z-ai` CLI, `python3`, `ffmpeg`, and `git` are installed.
3. Run the pipeline scripts in order:
   ```bash
   python3 survival-cinema-agent/agent/tools/06_generate_images.py    # ~50 min, regenerates 74 PNGs
   python3 survival-cinema-agent/agent/tools/07_generate_narration.py  # ~5 min, regenerates 22 WAVs
   python3 survival-cinema-agent/agent/tools/08_render_video.py        # ~10 min, regenerates final.mp4
   python3 survival-cinema-agent/agent/tools/09_thumbnail_packaging.py # regenerates thumbnail
   ```

## License

The framework code (survival-cinema-agent/) is MIT-licensed. The film "The Keeper of Cape Vespers" (survival_cinema/) is the original IP of the user who commissioned the production.

## Backup info

- Backup created: 2026-10-12
- Backup format: tar.gz
- Backup location: storage.to (link shared separately)
- File expiry: 3 days (anonymous upload)
- Recover ALL files before expiry; re-upload to permanent storage if needed.
