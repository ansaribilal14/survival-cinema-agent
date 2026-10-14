# Task 04 — Dramatic, volumetric background music + SFX (not soft)

**Issue title:** T04 — Music: dramatic cinematic score + sound design

**Source:** task-main.md — "The music and tone used is too soft ,I would prefer more dramatic volumetric background sound and effects which still compliments the voiceover but most importantly keep the item great."

## Root cause

The v1 used a single soft ambient sine drone (110Hz + 165Hz sine waves with echo) mixed at 18% volume. That is "soft." The user wants dramatic, volumetric, complimenting the voiceover.

## What needs to happen

1. Compose / source a dramatic cinematic score. Options:
   - (a) Royalty-free cinematic music from a known-good source (e.g. Pixabay Music, Free Music Archive, Incompetech). Need to verify license allows commercial use.
   - (b) Use ffmpeg's lavfi to generate a more sophisticated multi-layer score: low drones + tension swells + percussive hits.
   - (c) Use Python + numpy to synthesize a custom score with proper harmonic structure, swells, and dynamic range.
2. Layer the score under the narration at a balanced level (narration peaks ~-12dB, music bed ~-24dB, music swells during narration pauses).
3. Add SFX: wind, surf, foghorn, lamp gear tick, rain on iron, wood stove tick, fog-signal whistle (long-short-long-short-long), door knock, boat engine, paper rustle, pen on paper.
4. Ducking: music automatically ducks when narration is present, swells during narration pauses. Use ffmpeg's `sidechaincompress` for this.
5. The climax scene (S21 — fog signal) should have the loudest, most dramatic music + the fog-signal whistle SFX layered prominently.

## Acceptance

- Background music is dramatic and cinematic (not a soft sine drone).
- Music ducks under narration (sidechain compression).
- SFX are layered at appropriate moments (lamp tick, foghorn, fog signal, rain, door knock).
- The climax scene has audible, prominent dramatic music + the fog-signal whistle.
- Final mix peaks at -6dB, no clipping, narration is intelligible throughout.

## Status

- [x] ✅ COMPLETED — see v3.0.0 release (https://github.com/ansaribilal14/survival-cinema-agent/releases/tag/v3.0.0)
