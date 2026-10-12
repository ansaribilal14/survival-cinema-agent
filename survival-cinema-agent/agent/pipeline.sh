#!/usr/bin/env bash
# Survival Cinema Agent — Master Pipeline Runner
# Usage: ./agent/pipeline.sh [story_idea_file] [output_dir]
set -euo pipefail
STORY_IDEA="${1:-./story_idea.md}"
OUTPUT_DIR="${2:-./output_run}"
if [[ ! -f "$STORY_IDEA" ]]; then echo "ERROR: story idea file not found: $STORY_IDEA"; exit 1; fi
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"
echo "============================================================"
echo "  SURVIVAL CINEMA AGENT — PIPELINE START"
echo "  Story idea: $STORY_IDEA"
echo "  Output dir: $(pwd)"
echo "============================================================"
python3 "$OLDPWD/agent/tools/01_acquire_references.py"
python3 "$OLDPWD/agent/tools/02_analyze_references.py"
python3 "$OLDPWD/agent/tools/03_develop_story_scaffold.py" "$STORY_IDEA"
python3 "$OLDPWD/agent/tools/04_build_screenplay_scaffold.py"
python3 "$OLDPWD/agent/tools/05_visual_development_scaffold.py"
python3 "$OLDPWD/agent/tools/06_generate_images.py"
python3 "$OLDPWD/agent/tools/07_generate_narration.py"
python3 "$OLDPWD/agent/tools/08_render_video.py"
python3 "$OLDPWD/agent/tools/09_thumbnail_packaging.py"
python3 "$OLDPWD/agent/tools/10_qa_reports.py"
git init -b main 2>/dev/null || true
git add -A
git commit -m "Survival Cinema Agent run complete: $(date)" 2>/dev/null || true
echo "============================================================"
echo "  PIPELINE COMPLETE"
echo "  Final video: $(pwd)/output/final.mp4"
echo "============================================================"
