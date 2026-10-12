# Outputs

After a successful run, the system produces:

```
<output_dir>/
├── reference_library/
│   ├── manifest.json
│   ├── story_01_*_raw.txt and _clean.txt
│   ├── story_02_*_raw.txt and _clean.txt
│   └── story_03_*_raw.txt and _clean.txt
├── reference_analysis/
│   ├── reference_analysis_01.md, _02.md, _03.md
│   ├── narrative_techniques.json
│   ├── survival_mechanics.json
│   ├── character_arc_patterns.json
│   ├── pacing_and_scene_patterns.json
│   └── comparative_analysis.md
├── story_development/
│   ├── concept_candidates.md, story_bible.md, complete_story.md
│   ├── character_bible.json, world_bible.md
│   ├── continuity_rules.md, originality_audit.md
│   └── story_idea_parsed.json
├── screenplay/
│   ├── screenplay.md, scene_manifest.json, narration_script.txt
│   ├── subtitles.srt, chapter_markers.json, timeline.json
├── visual_development/
│   └── style_bible.md
├── assets/
│   ├── images/ (60-80 PNGs at 1344x768)
│   ├── narration_chunks/ (22 WAVs)
│   ├── narration/narration.wav
│   ├── asset_manifest.json
│   └── audio_manifest.json
├── output/
│   ├── final.mp4 (THE FILM, 1920x1080, h264+AAC, subs burned in)
│   ├── final_subtitles.srt
│   ├── thumbnail.png
│   └── video_metadata.json
├── reports/
│   ├── acquisition_report.md, narrative_analysis.md
│   ├── continuity_report.md, quality_report.md
│   ├── rights_and_provenance.md, production_failures.md
├── checkpoints/ (gitignored; resumability state)
├── scripts/ (build_screenplay.py)
├── PROJECT_STATUS.md, WORKLOG.md, manifest.json, config.json
└── story_idea.md (the user's input, preserved)
```

## What gets pushed to git

`.gitignore` excludes large binaries (images/, narration_chunks/, narration.wav, final.mp4, intermediate MP4s, reference raw texts). The git commit includes all source files plus the JSON manifests.

To distribute the final video, push to GitHub and create a Release with `output/final.mp4` as the release asset.

## The single most important output

**`output/final.mp4`** — the film. 1920×1080, 30 fps, h264+AAC, subtitles burned in, 12-20 minutes. Ready to upload to YouTube.
