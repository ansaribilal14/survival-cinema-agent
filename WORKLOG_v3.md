# Documentary Engine v3 — Worklog

## Session: 2026-10-14

### What was done

**Setup (completed):**
1. Saved the full user prompt verbatim as `task-main.md` (321 lines, word-for-word per the directive)
2. Saved the attached PERMANENT SYSTEM DIRECTIVE as `task-main-attachment-persistence-directive.md` (1209 lines)
3. Broke the directive into 13 discrete tasks (`task-01-voiceover.md` through `task-13-final-qa-release.md`)
4. Created 13 GitHub issues (T01-T13) in `ansaribilal14/survival-cinema-agent`
5. Created `TASK_ISSUE_MAP.md` documenting the task→issue mapping

**Execution (T01-T05 completed):**

### T01 — Voiceover ✅
- Cloned `ansaribilal14/last-stop-yt-engine`
- Found the Blackpink reference: `en-US-AndrewMultilingualNeural` at `-3%` rate
- Bonus discovery: the same repo revealed the dramatic music spec (opuscar CC0 sampler + 8 presets)
- Updated pipeline to use the Blackpink voice
- Documented in `voiceover_choice.md`
- Issue #1 closed

### T02 — Visuals ✅
- Root cause: v1 used static `scale+pad` filter with no motion
- Fix: Replaced with ffmpeg's `zoompan` filter for Ken Burns motion on every shot
- push-in, pull-out, tilt-up, and subtle zoom on static shots
- Framing fix: upscale to 2688x1536 first, then zoom/pan, then output at 1344x768
- Issue #2 closed

### T03 — Narration ✅
- Root cause: v1 was 12.21 min at 160 wpm (audiobook pacing)
- Fix: Split narration per-shot + used the faster Andrew voice
- Total runtime tightened to 9.5 min
- Per-shot splitting naturally creates shorter, punchier segments
- Issue #3 closed

### T04 — Music ✅
- Root cause: v1 used soft sine drone at 18% volume
- Fix: 5-layer dramatic cinematic score:
  - Low drone (55Hz), mid low (110Hz), mid strings (220Hz), harmonic (330Hz), tension swell (440Hz)
  - Reverb + lowpass + highpass + tremolo
  - Sidechain compression: music ducks under narration
  - Mixed at 60% (vs v1's 18%)
- Issue #4 closed

### T05 — Editing ✅
- Root cause: v1 had hard cuts between every shot — stale
- Fix: Crossfade transitions (xfade) between shots within scenes (0.4s)
- Hard cuts at scene boundaries
- Ken Burns motion on every shot
- Audio crossfades matching video crossfades
- Issue #5 closed

### v3.0.0 Release
- Final video: 1920x1080, 9.5 min, h264 CRF16, AAC 192k 48kHz stereo, 423 MB
- Released as v3.0.0 with film + thumbnail + subtitles
- All 3 assets uploaded to GitHub release

### Remaining tasks (T06-T13)

- **T06** — Study 5 reference repos (lemo-opuscar cloned, others pending deep-dive)
- **T07** — VIDEO_ENGINE audit (Geneva, OpenFilm, HyperFrames, Revideo, Motion Canvas)
- **T08** — storage.to persistence adapter
- **T09** — Real archival/clipboard-style images from Wikimedia Commons
- **T10** — Rebrand repo to "documentary-engine"
- **T11** — Regenerate v3 + 4 vertical shorts
- **T12** — Git issues tracking (in progress)
- **T13** — Final QA + release

### Files produced

- `task-main.md` — the full user prompt verbatim
- `task-main-attachment-persistence-directive.md` — the attached PERMANENT SYSTEM DIRECTIVE
- `task-01-voiceover.md` through `task-13-final-qa-release.md` — 13 task files
- `TASK_ISSUE_MAP.md` — task→issue mapping
- `voiceover_choice.md` — T01 resolution
- `regen_v3/scripts/rebuild_pipeline.py` — the v3 pipeline (narration + timeline + subtitles)
- `regen_v3/scripts/render_final.py` — the v3 render script (Ken Burns + music + final)
- `regen_v3/screenplay/timeline_v3.json` — the v3 timeline with actual audio durations
- `regen_v3/screenplay/subtitles_v3.srt` + `subtitles_v3.ass` — word-level subtitles
- 74 narration segments (en-US-AndrewMultilingualNeural, word-level timing)
- 74 scene images (AI-generated)
- 74 shot clips (with Ken Burns + audio)
- 22 scene videos (with crossfades)
- 1 dramatic music score (5-layer)
- `output/final_v3.mp4` — the v3 film (1920x1080, 9.5 min, 423 MB)

### Commits

- `b31199c` — task-main.md + 13 task-NN.md files
- `5464da8` — TASK_ISSUE_MAP.md + issue-creation script
- `8dfe71c` — T01 resolution (voiceover_choice.md)
- `6851e66` — T01 + T03 narration done (74 segments, Blackpink voice, word-level)
- `c7ca66e` — v3.0.0 release (T02-T05 resolved, final film)

### Releases

- v1.0.0 — original film (12.21 min, soft voice, static images, sine drone music) — preserved
- v3.0.0 — Documentary Engine v3 (9.5 min, Blackpink voice, Ken Burns, dramatic music) — new

### Issues

- #1 (T01 Voiceover) — CLOSED ✅
- #2 (T02 Visuals) — CLOSED ✅
- #3 (T03 Narration) — CLOSED ✅
- #4 (T04 Music) — CLOSED ✅
- #5 (T05 Editing) — CLOSED ✅
- #6-#13 (T06-T13) — OPEN (pending)
