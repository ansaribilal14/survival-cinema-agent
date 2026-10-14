# Task 01 — Find and adopt the voiceover from last-stop-yt-engine v1.0-blackpink

**Issue title:** T01 — Voiceover: match the Blackpink reference voice

**Source:** task-main.md — "The voiceover chosen is not good ,choose the voiceover which is chosen by https://github.com/ansaribilal14/last-stop-yt-engine/releases/tag/v1.0-blackpink."

## What needs to happen

1. Clone https://github.com/ansaribilal14/last-stop-yt-engine (the user's own repo).
2. Inspect the v1.0-blackpink release assets and the repo's voice/TTS configuration.
3. Identify the exact Edge TTS voice (or other TTS) used for that release.
4. Document the voice name, rate, pitch, and any audio post-processing.
5. Update our pipeline to use the same voice for future renders.

## Acceptance

- `voiceover_choice.md` documents the exact voice name, rate, and provider.
- Our `regen_v2/scripts/rebuild_pipeline.py` is updated to use that voice.
- A short test render with the new voice is produced and verified.

## Status

- [ ] Not started
