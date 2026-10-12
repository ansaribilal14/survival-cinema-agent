# Architecture

## The Survival Cinema Agent is a 3-layer system

**Layer 1 — User Input:** `story_idea.md` (one file, plain prose, ~10 fields)

**Layer 2 — Agent Orchestration:**
- `agent/SYSTEM_PROMPT.md` — the master directive
- `agent/pipeline.sh` — the runner
- `agent/tools/01_*.py` through `10_*.py` — one script per phase

**Layer 3 — Outputs:** the film, thumbnail, metadata, story_development/, screenplay/, assets/, reports/

## Two kinds of phases

**Deterministic** (scripted, no LLM creativity):
- Phase 1-2: Acquire references (download, clean, verify)
- Phase 7: Generate images (call image CLI per shot)
- Phase 8: Generate narration (call TTS CLI per scene)
- Phase 9: Render video (ffmpeg pipeline)
- Phase 10: Thumbnail + packaging
- Phase 11: QA scaffolds

**Creative** (require LLM judgement):
- Phase 3: Analyze references
- Phase 4: Develop original story
- Phase 5: Build screenplay
- Phase 6: Visual style
- Phase 11: QA findings

## Provider-agnostic by design

Each external tool call (image, TTS, vision, search) goes through a single function. Swap providers with one edit per phase.

## Resumability

Every expensive phase writes a checkpoint JSON. Re-running skips already-done work.

## The demo is the contract

`examples/keeper_of_cape_vespers/` is a complete reference run. If unsure what an output should look like, look at the demo.

## Why public-domain references?

Project Gutenberg works (Poe 1838, London 1915, Wells 1896) are used for narrative-technique research. Lawful, verifiable, substantive, diverse, less-cited. No copyright risk.

To use different references, edit `DEFAULT_REFERENCES` in `agent/tools/01_acquire_references.py`.
