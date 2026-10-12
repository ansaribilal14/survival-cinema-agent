# The 11 Phases

Each phase has a single script in `agent/tools/`. The master runner is `agent/pipeline.sh`.

## Phase 1 — Discover three complete reference works
**Script:** `01_acquire_references.py` (combined with Phase 2)
**Type:** Deterministic
**Output:** `reference_library/manifest.json`

Searches for three substantial, complete, lawfully-accessible works in three categories: wilderness, apocalyptic, psychological. Default uses curated public-domain Project Gutenberg works (Poe, London, Wells).

## Phase 2 — Download, extract, verify full text
**Script:** `01_acquire_references.py` (combined)
**Type:** Deterministic
**Output:** cleaned text files, `reports/acquisition_report.md`

Download via `curl`, strip boilerplate, compute word count, verify opening and ending. Replace any candidate that fails.

## Phase 3 — Read and analyze all three stories
**Script:** `02_analyze_references.py` (scaffold)
**Type:** Creative (LLM-driven)
**Output:** 8 files in `reference_analysis/`

Extract narrative architecture, survival mechanics, character design, suspense, scene craft, adaptation potential. Do NOT copy prose, dialogue, scenes, characters, settings, or distinctive plot elements.

## Phase 4 — Create the original female-centric survival story
**Script:** `03_develop_story_scaffold.py` (scaffold)
**Type:** Creative (LLM-driven)
**Output:** 7 files in `story_development/`

3 concept candidates → pick strongest → write full story (~3-5k words) → character bible → world bible → continuity rules → originality audit. Protagonist must be a young adult woman (20-25) with substantial agency.

## Phase 5 — Adapt the story into a production-ready screenplay
**Script:** `04_build_screenplay_scaffold.py` (scaffold)
**Type:** Creative + Deterministic
**Output:** 6 files in `screenplay/`

22 scenes, 60-80 shots. Each scene: shot list with image prompts, narration, dialogue, music/SFX cues, continuity requirements.

## Phase 6 — Visual development
**Script:** `05_visual_development_scaffold.py`
**Type:** Creative
**Output:** `visual_development/style_bible.md`

Style bible: palette, lighting, lens language, visual motifs, forbidden elements, continuity anchors, style-anchor text.

## Phase 7 — Generate scene-by-scene AI images
**Script:** `06_generate_images.py`
**Type:** Deterministic
**Output:** `assets/images/*.png`, `assets/asset_manifest.json`

One image per shot. Retry up to 3× on failure. Resumable.

## Phase 8 — Narration and audio production
**Script:** `07_generate_narration.py`
**Type:** Deterministic
**Output:** `assets/narration_chunks/*.wav`, `assets/narration/narration.wav`, `assets/audio_manifest.json`

22 TTS chunks in a single consistent voice. Concatenate into one narration WAV.

## Phase 9 — Cinematic editing and video render
**Script:** `08_render_video.py`
**Type:** Deterministic
**Output:** `output/final.mp4` (1920×1080, 30fps, h264+AAC, subtitles burned in)

Three-pass FFmpeg: shots → scenes → film, upscale to 1920×1080, burn subtitles.

## Phase 10 — Thumbnail + YouTube packaging
**Script:** `09_thumbnail_packaging.py`
**Type:** Mixed (deterministic for thumbnail, creative for metadata text)
**Output:** `output/thumbnail.png`, `output/video_metadata.json`, `output/final_subtitles.srt`

One cinematic thumbnail. Title, description, chapters, keywords, AI disclosure.

## Phase 11 — Multi-layer QA
**Script:** `10_qa_reports.py` (scaffold)
**Type:** Creative (LLM-driven findings)
**Output:** 5 reports in `reports/`

Narrative, continuity, visual, audio, render, rights & provenance. All failures explicit.
