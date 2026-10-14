# Task 03 — Tighten the voiceover pacing so viewers don't bore out

**Issue title:** T03 — Narration: trim and tighten pacing

**Source:** task-main.md — "The voiceover is too detailed to keep the pace right which can cause watcher too bore out."

## Root cause

The v1 narration is 1,950 words across 12.21 minutes — that's ~160 words/min, which is fine for audiobook pacing but too slow for a cinematic short film (cinematic pacing is 180-220 wpm with strategic pauses).

More critically: the narration is written in full literary prose ("The way a person touches a bruise to see if it still hurts") which sounds beautiful on the page but reads slow when spoken. A film narration needs shorter, punchier sentences.

## What needs to happen

1. Rewrite the narration script in cinematic short-form:
   - Cut literary flourishes by ~30%
   - Break long sentences into short ones
   - Keep the key plot beats and emotional moments
   - Target 1,400-1,600 words for a 10-12 minute film (180-200 wpm)
2. Keep the same story, characters, plot, and ending — just tighter prose.
3. Test the rewritten narration with edge-tts and verify the duration is ~10-11 minutes.
4. The new narration must still hit the same emotional beats: arrival, discovery, midpoint reveal, climax, resolution.

## Acceptance

- New `narration_script_v2.txt` written in cinematic short-form.
- Word count 1,400-1,600.
- Edge-tts render is 10-12 minutes.
- Word-level subtitles still align perfectly with audio.

## Status

- [x] ✅ COMPLETED — see v3.0.0 release (https://github.com/ansaribilal14/survival-cinema-agent/releases/tag/v3.0.0)
