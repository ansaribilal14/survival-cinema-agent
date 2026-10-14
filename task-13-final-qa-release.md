# Task 13 — Final QA: verify the v3 film meets all user requirements, publish release

**Issue title:** T13 — QA + release: final verification and publication

**Source:** The final "I expect better videos from you take your time" directive.

## What needs to happen

After Tasks 01-11 are complete:

1. **Watch the v3 film and the 4 shorts** (or sample frames + audio clips) and verify against the user's complaints:
   - ✅ Voiceover is the Blackpink-reference voice (not the soft tongtong)
   - ✅ Backgrounds fill the frame (no out-of-frame content)
   - ✅ Visuals feel alive (Ken Burns motion, not dead static)
   - ✅ Narration is tight (not too detailed, not boring)
   - ✅ Music is dramatic and volumetric (not soft)
   - ✅ SFX present (lamp tick, foghorn, fog signal, rain, etc.)
   - ✅ More images per scene (150-180 shots, not 74)
   - ✅ Editing is dynamic (varied shot durations, crossfades, hard cuts at scene boundaries)
   - ✅ Real archival/clipboard-style images mixed in (15-25 plates)
2. **Run technical QA**:
   - Resolution: 1920x1080 (film), 1080x1920 (shorts)
   - Frame rate: 30 fps
   - Codec: h264 + AAC
   - Duration: matches expected
   - Subtitles: burned in + match audio (word-level from edge-tts)
   - Audio peaks: -6dB, no clipping
   - File size: reasonable (50-200 MB)
3. **Create the v3.0.0 GitHub Release**:
   - Tag: `v3.0.0`
   - Title: `v3.0.0 — The Documentary Engine + Keeper of Cape Vespers v3`
   - Body: full changelog (what changed vs v1), asset inventory, storage.to URLs, AI disclosure
   - Assets: final.mp4, shorts A-D (4 files), thumbnail.png, subtitles.srt, video_metadata.json, manifest.json
4. **Update the landing page** to feature v3.
5. **Push the final commit** with all task-NN.md status updates + verification results.

## Acceptance

- v3 film passes all 9 user-requirement checks.
- v3.0.0 release exists with all assets attached.
- Landing page features v3.
- All task-NN.md files updated to "Status: ✅ Completed" with commit SHAs.
- All 11 GitHub issues closed with substantive comments.

## Status

- [ ] Not started
