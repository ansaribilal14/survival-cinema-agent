# Task 06 — Clone and deep-dive 5 user-named reference repos

**Issue title:** T06 — Research: clone and study 5 reference repos (lemo-opuscar, open-generative-ai, reelmimic, brag, MoneyPrinterTurbo)

**Source:** task-main.md — "Clone ,deep dive ,and learn everything to implement in our Enging from below gits.

lemomo-ai/lemo-opuscar
https://github.com/lemomo-ai/lemo-opuscar

anil-matcha/open-generative-ai
https://github.com/anil-matcha/open-generative-ai

edenfunf/reelmimic
https://github.com/edenfunf/reelmimic

latent-spaces/brag
https://github.com/latent-spaces/brag

https://github.com/harry0703/MoneyPrinterTurbo/blob/main/README-en.md"

## What needs to happen

1. Clone all 5 repos to `/home/z/my-project/research_repos/` (already partially done — verify each).
2. For each repo, study:
   - The actual rendering mechanism (FFmpeg pipeline? Browser-based? Canvas? Remotion?)
   - How scenes/timelines are represented (JSON? YAML? TS? HTML?)
   - How narration + subtitles are handled
   - How images and footage are sourced (built-in search? manual upload? Commons API?)
   - How music/SFX are layered
   - The license (commercial-use friendly?)
3. Document findings in `ENGINE-NOTES-REFS.md`.
4. Identify which techniques are safe to adopt without breaking our existing pipeline.

## Specific things to extract from each

- **lemo-opuscar**: Study the OpusCar render core (the user mentioned `/home/z/my-project/opuscar/core/render/` previously). Learn its scene format and rendering approach.
- **open-generative-ai**: Look for AI-agent orchestration patterns, scene planning, asset generation.
- **reelmimic**: Study its skill-locked agent pattern (the user mentioned this).
- **brag**: Look for video composition patterns and any rendering tricks.
- **MoneyPrinterTurbo**: Already cloned. Study its per-asset source ledger pattern, its edge-tts + Whisper subtitle alignment, and its BGM handling.

## Acceptance

- All 5 repos cloned and inspected.
- `ENGINE-NOTES-REFS.md` documents each repo's capabilities, license, and what we can safely adopt.
- A summary table at the top of ENGINE-NOTES-REFS.md lists which techniques we will adopt and which we will skip.

## Status

- [ ] Not started
