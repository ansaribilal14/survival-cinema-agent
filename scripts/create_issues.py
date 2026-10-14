#!/usr/bin/env python3
"""Create GitHub issues for each task-NN.md file in the repo."""
import json
import os
import subprocess
import time
from pathlib import Path

REPO = "ansaribilal14/survival-cinema-agent"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    print("ERROR: set GH_TOKEN or GITHUB_TOKEN env var before running")
    raise SystemExit(1)

TASKS = [
    ("01", "voiceover", "T01 — Voiceover: match the Blackpink reference voice", ["task", "enhancement"]),
    ("02", "visuals-framing", "T02 — Visuals: fix framing + add life to static backgrounds", ["task", "bug"]),
    ("03", "narration-pacing", "T03 — Narration: trim and tighten pacing", ["task", "enhancement"]),
    ("04", "music-dramatic", "T04 — Music: dramatic cinematic score + sound design", ["task", "enhancement"]),
    ("05", "editing-richer", "T05 — Editing: more shots per scene, dynamic cutting", ["task", "enhancement"]),
    ("06", "study-5-refs", "T06 — Research: clone and study 5 reference repos", ["task", "research"]),
    ("07", "video-engine-audit", "T07 — VIDEO_ENGINE audit: 5 video engine repos (7-phase)", ["task", "research"]),
    ("08", "persistence-storage-to", "T08 — Persistence: storage.to + git manifest + recovery", ["task", "enhancement"]),
    ("09", "stills-clipboard-images", "T09 — Stills: real archival/clipboard-style images", ["task", "enhancement"]),
    ("10", "rebrand-documentary-engine", "T10 — Rebrand: rename repo to documentary-engine", ["task", "enhancement"]),
    ("11", "regenerate-v3", "T11 — Regenerate: Keeper of Cape Vespers v3 + 4 shorts", ["task", "enhancement"]),
    ("12", "git-issues", "T12 — Git issues: create + track all task issues", ["task", "meta"]),
    ("13", "final-qa-release", "T13 — QA + release: final verification and publication", ["task", "release"]),
]


def create_issue(title, body, labels):
    payload = {"title": title, "body": body, "labels": labels}
    cmd = [
        "curl", "-sS", "-X", "POST",
        f"https://api.github.com/repos/{REPO}/issues",
        "-H", f"Authorization: token {TOKEN}",
        "-H", "Accept: application/vnd.github+json",
        "-d", json.dumps(payload),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        data = json.loads(result.stdout)
        return data.get("number"), data.get("html_url"), data.get("message", "none")
    except Exception as e:
        return None, None, f"parse error: {e}; raw: {result.stdout[:200]}"


def main():
    summary = []
    for num, slug, title, labels in TASKS:
        task_file = Path(f"task-{num}-{slug}.md")
        if not task_file.exists():
            print(f"  [SKIP] {task_file} not found")
            continue
        body = task_file.read_text(encoding="utf-8")
        if len(body) > 60000:
            body = body[:60000] + "\n\n[truncated — see full file in repo]"
        print(f"  Creating issue: {title}")
        number, url, error = create_issue(title, body, labels)
        if number:
            print(f"    ✓ #{number}: {url}")
            summary.append((num, number, url))
        else:
            print(f"    ✗ Error: {error}")
        time.sleep(1)

    summary_file = Path("TASK_ISSUE_MAP.md")
    lines = ["# Task → GitHub Issue Map", "", "| Task | Issue | URL |", "|---|---|---|"]
    for num, number, url in summary:
        lines.append(f"| task-{num} | #{number} | {url} |")
    summary_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSummary written to {summary_file}")
    print(f"Created {len(summary)} issues.")


if __name__ == "__main__":
    main()
