# Task 07 — VIDEO_ENGINE master directive: audit 5 video engine repos (Geneva, OpenFilm, HyperFrames, Revideo, Motion Canvas)

**Issue title:** T07 — VIDEO_ENGINE audit: benchmark Geneva, OpenFilm, HyperFrames, Revideo, Motion Canvas

**Source:** task-main.md — the full "MASTER DIRECTIVE: VIDEO ENGINE RESEARCH, BENCHMARKING & SAFE INTEGRATION" with 7 phases.

## What needs to happen

Follow the 7-phase protocol exactly. Do NOT skip phases.

### Phase 1 — Establish baseline
1. Identify the active project repo (ansaribilal14/survival-cinema-agent), branch (main), current commit, working-tree state, runtime, package manager, dependency versions, deployment environment.
2. Map the existing architecture: orchestrator, research, script generation, scene planning, timeline, image ingestion, video downloaders, narration, audio mixing, subtitles, rendering, encoding, export, output validation, scheduled jobs, API routes, storage, config.
3. Identify the existing production workflow and all working features that must be preserved.
4. Run baseline tests: smallest existing end-to-end render. Record results, output properties, failures.
5. Inspect recent changes and unfinished work. Do not overwrite work in progress.

### Phase 2 — Audit 5 repos
1. Geneva — https://github.com/geneva-render/geneva
2. OpenFilm — https://github.com/openfilm/openfilm
3. HyperFrames — https://github.com/heygen-com/hyperframes
4. Revideo — https://github.com/redotvideo/revideo
5. Motion Canvas — https://github.com/motion-canvas/motion-canvas

For each, document: verified capabilities, rendering mechanism, output formats, project/scene/timeline/animation/transition representation, support for HTML/CSS/SVG/JS/TS/keyframes/text/images/footage/audio/subtitles, headless rendering, AI-agent integration, installation requirements, OS compatibility, GPU requirements, cloud-runtime compatibility, dependency footprint, performance, failure modes, license, commercial use, repo maintenance, releases, known limitations, compatibility risks, whether useful functionality can be adopted through adapter/subprocess/package/isolated service.

Distinguish verified from assumed. Do not claim a feature works without source/doc/test evidence.

### Phase 3 — Benchmark representative capabilities
Create small isolated proof-of-concept for the strongest candidates using a representative documentary scene:
- Full-screen image or video background
- Animated documentary title and subtitle
- Evidence card or timeline graphic
- Lower-third identification
- Fade or transition between scenes
- Existing narration audio
- Accurate subtitle timing
- Final H.264 MP4 at 1920x1080, 30 FPS

Measure actual render time, memory use, output integrity, dependency requirements, visual quality.

Compare on: visual quality, compatibility with current orchestrator, reliable unattended rendering, ease of agent-controlled composition, integration complexity, maintenance burden, runtime cost, licensing.

### Phase 4 — Select best architecture
Choose the smallest combination of tools that materially improves the existing system. Prefer: preserve current orchestrator, keep scene planner independent, introduce a rendering-provider interface, use adapters, keep existing path as fallback, isolate new dependencies, use reusable motion-graphics templates, keep FFmpeg for final encoding, preserve existing narration/subtitles/asset ingestion.

Do NOT migrate the entire project to a new framework just because it's architecturally attractive.

### Phase 5 — Implement safely
1. Work in an isolated branch.
2. Pin dependency versions.
3. Keep new engines optional until acceptance tests pass.
4. Avoid breaking changes.
5. No paid APIs.
6. No removing existing functionality without explicit approval.
7. No exposing credentials.
8. No deploying without authorization.
9. Document new config, install steps, resource requirements, rollback.
10. If integration is too risky, leave production path unchanged and document the blocker.

### Phase 6 — Regression testing
Run existing tests. Run baseline render. Run new renderer POC. Verify output exists, nonempty, decodes. Verify resolution, fps, codec, audio presence, audio duration, subtitle sync. Check transitions render. Verify existing scene inputs still work. Confirm fallback remains usable. Compare baseline vs post-change for regressions.

Do NOT report tests as passing unless actually executed.

### Phase 7 — Deliverables
Create/update:
- VIDEO_ENGINE_AUDIT.md — findings for all 5 repos, licenses, verified capabilities
- VIDEO_ENGINE_BENCHMARK.md — test methodology, results, limitations, chosen engine
- VIDEO_ENGINE_ARCHITECTURE.md — provider interface, adapter design, data flow, fallback behavior
- VIDEO_ENGINE_INTEGRATION.md — implemented changes, config, usage, rollback instructions

Final report: strongest candidate and why; what was implemented and files changed; what remains unchanged; tests actually completed with results; resource requirements; how to run new renderer and switch back; blockers requiring user decision.

## Operating rule

RESEARCH → INSPECT → BENCHMARK → SELECT → IMPLEMENT → TEST → REPORT.

Do NOT stop after a plan. Do NOT rush integration before baseline. Never sacrifice the working system for an unverified improvement.

## Acceptance

- All 4 deliverable docs exist and are populated with real findings (not boilerplate).
- A benchmark POC is actually rendered and verified.
- The chosen engine (if any) is integrated as an optional path, not a replacement.
- Regression tests confirm v1 still works.

## Status

- [ ] Not started
