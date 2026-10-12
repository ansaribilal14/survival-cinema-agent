#!/usr/bin/env python3
"""Phase 6 — Visual development scaffold."""
from pathlib import Path
ROOT = Path.cwd(); VD = ROOT/"visual_development"; VD.mkdir(parents=True,exist_ok=True)
TEMPLATE = """# Visual Style Bible — *<Story Title>*

## Overall style
<2-3 sentences describing the visual identity.>

**Forbidden:** teal-and-orange color grading; hyperreal plastic skin; flat cartoon style; anime/manga; AI-typical soft-glow portrait; text or watermarks.

## Aspect ratio, resolution, frame
- All scene images: 16:9 at 1344x768.
- Thumbnail: 1344x768.
- Render: 1920x1080, 30 fps, h264, AAC audio, mp4.

## Color palette
<Define palette per the story's tone.>

## Lighting logic
<Per time of day, with the recurring lamp rotation motif.>

## Composition
- Wide shots for geography; medium for interaction; close-ups for hands/eyes/props.
- Slow push-ins for tension; static for grief; slow pull-outs for transitions.

## Visual motifs (must recur)
1. <motif 1> 2. <motif 2> 3. <motif 3> 4. <motif 4>

## Forbidden visual elements
- No text or watermarks. No real actors' faces. <story-specific forbiddens>

## Continuity anchor rules
<Per character, 2-3 visual anchors consistent across all images.>

## Style anchor text (appended to every image prompt)
> Cinematic 16:9, painterly, slight film grain, <palette>. Slight vignette. No text, no watermarks. <style reference>.
"""
def main():
    print("[Phase 6] Scaffolding visual_development/...")
    sb = VD/"style_bible.md"
    if sb.exists() and sb.stat().st_size > 500: print("  SKIP"); return
    sb.write_text(TEMPLATE, encoding="utf-8")
    print(f"  CREATED {sb}")
if __name__=="__main__": main()
