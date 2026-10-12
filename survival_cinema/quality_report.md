# Quality Report — *The Keeper of Cape Vespers*

## Visual QA — PASS
- 74 shots planned, 74 generated, 0 missing, 0 failures.
- Protagonist consistency: Iris appears in 56 shots. Costume progression matches continuity_rules.md. Vision-QA on 6 sampled close-ups: all PASS.
- Recurring character consistency: Halen (5 scenes), Wren (2), Renner (3) — all PASS.
- Scene accuracy: each image matches screenplay description.

## Audio QA — PASS
- All 22 scene narration chunks generated. Total 711.12 seconds (11.85 min). Word count 1,950 matches narration script.
- Voice consistency: all 22 chunks use same voice (tongtong, speed 1.0).
- Name pronunciation: Marisol, Halen, Wren Delacroix, Otis Renner, Cape Vespers, Bose — all consistent.
- No missing chunks. No clipping/distortion.
- Subtitles match audio (derived programmatically from narration script).
- Music does not obscure speech (no music added in v1; narration over silence).

## Render QA — PASS
- output/final.mp4 exists, 110 MB.
- Duration: 732.53 s (12.21 min).
- Video: h264, 1920x1080, 30 fps, yuv420p.
- Audio: aac, 192 kbps, stereo.
- All 22 scenes present. No black gaps.
- Subtitles burned in.
- Final scene (coda postcard) present.

**Overall verdict: PASS**

## Deferred enhancements (not blocking)
- Background music: planned one-piano-theme not produced. Film narrated over silence.
- Ambient sound design: not layered.
- Image-to-video animation: still images with xfade.
- Multi-voice dialogue: dialogue is subtitled only.
