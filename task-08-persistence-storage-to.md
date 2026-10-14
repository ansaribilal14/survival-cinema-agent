# Task 08 — Universal asset persistence with storage.to (per the attached PERMANENT SYSTEM DIRECTIVE)

**Issue title:** T08 — Persistence: storage.to upload after every asset, git manifest, recovery

**Source:** task-main-attachment-persistence-directive.md (the full PERMANENT SYSTEM IMPLEMENTATION directive the user attached).

## What needs to happen

This is a system-level feature, not a one-off. Implement permanent storage.to integration:

1. **Inspect** the actual repo and runtime before changes.
2. **Build a reusable storage adapter** that isolates storage.to logic:
   - `upload_asset(file, metadata)` → uploads, returns URL + remote_id
   - `get_asset_location(asset_id)` → returns the URL
   - `download_asset(asset_id, destination)` → downloads to local
   - `verify_asset(asset_id, expected_checksum)` → SHA-256 verify
   - `check_asset_availability(asset_id)` → HTTP HEAD check
   - `get_asset_metadata(asset_id)` → file metadata
   - `delete_asset(asset_id)` → only if officially supported
   - `retry_pending_upload(asset_id)` → bounded retry
3. **Immediate upload after every completed asset** (narration chunk, image, SRT, video, thumbnail). Do NOT wait for session end.
4. **Git-tracked asset manifest** at `storage/ASSET_MANIFEST.json` with full schema:
   - asset_id, project_id, asset_type, filename, mime_type, size_bytes, sha256, provider, remote_id, remote_url, created_at, uploaded_at, last_verified_at, verification_status, availability_status, retention_policy, expiration_at, generation_stage, version, dependencies, retry_status, notes
5. **Naming convention**: `projects/{project_id}/{video|audio|subtitles|images|documents}/{filename}` (logical paths; storage.to returns flat URLs).
6. **Mandatory startup/recovery procedure**:
   1. Read permanent system instructions from canonical Git repo.
   2. Fetch latest committed state.
   3. Read `memory/CURRENT_STATE.md`, `memory/PROJECT_REGISTRY.md`, `memory/SESSION_HANDOFF.md`.
   4. Load relevant project checkpoint + asset manifest.
   5. Determine active project, current task, completed stages, pending stages, next action.
   6. Check availability of assets needed for next stage.
   7. Download required assets.
   8. Verify restored files against recorded checksums.
   9. Resume from latest valid checkpoint.
   10. Update and push Git whenever recovery discovers a material state change.
7. **Files to create** in the repo:
   - `AGENTS.md` (or update existing permanent agent instructions)
   - `memory/CURRENT_STATE.md`
   - `memory/PROJECT_REGISTRY.md`
   - `memory/SESSION_HANDOFF.md`
   - `storage/ASSET_MANIFEST.json`
   - `storage/STORAGE_POLICY.md`
   - `storage/RECOVERY.md`
   - `storage/DELETION_LOG.md`
   - `docs/PERSISTENCE_ARCHITECTURE.md`
8. **Tests**:
   - Successful anonymous upload
   - Response parsing and URL/ID recording
   - Retrieval and checksum verification
   - Immediate persistence of audio, SRT, images, video outputs
   - Git manifest update and push after each asset
   - Restart recovery from an empty runtime
   - Restoration of a previously uploaded asset
   - Interrupted uploads and interrupted Git updates
   - Retry behavior without unnecessary duplication
   - Missing or expired assets
   - Rate limits, network errors, malformed responses, oversized files
   - Concurrent manifest updates
   - User-confirmed cleanup and deletion limitations

9. **Per-project releases** — every completed project ships as its own GitHub Release immediately, with stable tag like `project-<project_id>-v1.0.0`, including project summary, deliverables, asset inventory, checksums, storage.to URLs. Don't wait for other projects.

10. **User-confirmed cleanup** — project completion does NOT mean deletion. Cleanup requires explicit user authorization. Record cleanup in `storage/DELETION_LOG.md`.

## Acceptance

- Storage adapter exists and is unit-tested.
- Every asset the pipeline produces is uploaded to storage.to immediately.
- Asset manifest is committed and pushed after each successful upload.
- A fresh runtime can discover and download a prior asset from the manifest.
- The agent resumes from the correct task checkpoint without regenerating completed assets.
- Missing/expired assets are detected and handled accurately.
- Project cleanup requires explicit user authorization.
- All service limitations are documented.
- Tests are actually executed (not just written).

## Status

- [ ] Not started
