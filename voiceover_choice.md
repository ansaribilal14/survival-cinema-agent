# Voiceover Choice — T01 Resolution

## Source

The user asked us to match the voiceover from `ansaribilal14/last-stop-yt-engine` v1.0-blackpink release.

## Discovery

Cloned the repo and inspected `pipeline/tts_all.py`. The voiceover config is:

```python
VOICE = "en-US-AndrewMultilingualNeural"
RATE = "-3%"
```

Plus, the pipeline uses **edge-tts's WordBoundary stream events** to capture per-word timing for caption alignment. This is the gold standard — captions are built from the actual TTS audio timing, not estimated.

## Why this voice

`en-US-AndrewMultilingualNeural` is a male multilingual neural voice from Microsoft Edge TTS. It's:
- Professional and documentary-grade (not the soft "tongtong" we used before)
- Expressive enough for dramatic narration
- Multilingual (handles foreign names like "Marisol" / "Renner" / "Vespers" correctly)
- Clean and clear at -3% rate (slightly slower for cinematic pacing)

## Adjacent discoveries from the same repo

### Music: composed documentary score via opuscar CC0 sampler

`pipeline/music/score_build.py` composes a score from CC0/CC-BY instrument samples using `lemo-opuscar`'s sampler (which we'll study in T06). 8 presets matched to the film's act structure:

| Preset | Mood | Use |
|---|---|---|
| overture | strings pad + piano motif + low strings, builds | Act 1 opening |
| trainee | sparse piano + soft strings (hopeful, restrained) | Quiet moments |
| tension | tremolo strings + timpani swells + low drone bass | Suspense build |
| dark | low strings only, slow, heavy (hiatus) | Dark revelation |
| dawn | piano + glockenspiel + strings opening up | Hope after dark |
| triumph | full strings + horns + tubular bells | Climax |
| warm | vibraphone + piano + strings, major, gentle | Quiet warm beat |
| resolve | piano + slow strings, final cadence | Resolution |

Each preset has roman-numeral chord progressions. Piano = Salamander (CC BY 3.0).

### Audio mix spec (the "dramatic volumetric" the user asked for)

- Narration: high-pass filtered + normalized
- Music: ducked under voice with opuscar-style ducking (dilate 160ms + smooth 250ms, -9dB under voice)
- Master: chunked lookahead limiter, two-pass LINEAR loudnorm to **-14 LUFS**
- Format: AAC 192k 48kHz stereo

This is the opposite of our v1's "soft sine drone at 18% volume." This is a real composed score with proper ducking and mastering.

### Render spec

- 1920x1080, 30fps, H.264 CRF16, profile high, level 4.0
- Captions: word-timed ASS burned per segment (using edge-tts WordBoundary data, not estimated)

## Action items for our engine

1. Update `regen_v2/scripts/rebuild_pipeline.py`:
   - `EDGE_VOICE = "en-US-AndrewMultilingualNeural"` (was `en-US-AvaMultilingualNeural`)
   - `EDGE_RATE = "-3%"` (was `-8%`)
   - Use edge-tts WordBoundary stream events (already using `--write-subtitles` which captures word timing — equivalent)
2. Build a real score: copy `score_build.py` patterns from last-stop-yt-engine. Use opuscar CC0 sampler (need to clone `lemomo-ai/lemo-opuscar` — see T06).
3. Master the final audio to -14 LUFS with two-pass LINEAR loudnorm.
4. Render at CRF16 (was CRF23 — higher quality).

## T01 status

✅ **RESOLVED** — Voiceover identified: `en-US-AndrewMultilingualNeural` at `-3%` rate, with edge-tts WordBoundary for captions. Plus discovered the music + audio mastering spec which directly addresses T04 (dramatic music).

Commit: pending (will be committed with T03 narration rewrite + T04 music upgrade)
