# Task 02 — Fix visuals: backgrounds getting out of frame, "dead meat" feel

**Issue title:** T02 — Visuals: fix framing + add life to static backgrounds

**Source:** task-main.md — "The visuals is toooo dead meat ,the backgrounds keep getting out of frame."

## Root cause analysis (from v1 render)

The v1 pipeline used a naive scale+pad filter for every shot:
```
scale=1344:768:force_original_aspect_ratio=decrease,pad=1344:768:(ow-iw)/2:(oh-ih)/2:color=black
```
AI-generated images at 1344x768 are already 16:9, but the pad is still applied. When the image aspect ratio differs slightly from 1344x768 (e.g. 1344x768 source vs 1920x1080 target), the upscaling step from 1344x768 → 1920x1080 stretches the image, leaving visible black bars or cropping content out of frame on the final 1080p render.

"Dead meat" feel: images are static. No Ken Burns motion. No parallax. Just cuts between static frames.

## What needs to happen

1. Generate images at the EXACT target aspect ratio (16:9 = 1920x1080 directly, or 1344x768 which is exactly 16:9 — verify this is the case).
2. Replace the scale+pad filter with a proper "cover" crop that fills the frame completely (no black bars, no out-of-frame content).
3. Add real Ken Burns motion per shot: slow push-in (1.0 → 1.06), slow pull-out (1.06 → 1.0), slow pan, slow tilt-up. This is the cure for "dead meat."
4. Add subtle film grain + vignette in post for life.
5. Add crossfade transitions between shots (0.4s) so cuts aren't jarring.

## Acceptance

- Every shot fills the 1920x1080 frame edge-to-edge (no black bars).
- Every shot has perceptible motion (Ken Burns).
- Crossfades between shots within a scene.
- A QC script extracts 3 sample frames per scene and verifies via vision-QA that the composition looks alive and the subject is in frame.

## Status

- [ ] Not started
