# Task 10 — Rebrand repo as "The Documentary Engine"

**Issue title:** T10 — Rebrand: rename repo to documentary-engine, update landing page + docs

**Source:** task-main.md — "our new repo name would be the documentary engine"

## What needs to happen

1. Rename the GitHub repo from `ansaribilal14/survival-cinema-agent` to `ansaribilal14/documentary-engine` (via the GitHub API).
2. Update README.md to reflect the new name and broader scope (documentary + survival thriller + shorts).
3. Update the landing page (`site/index.html` on the `gh-pages` branch):
   - Title: "The Documentary Engine"
   - Subtitle: "Autonomous AI film production for documentary and survival-thriller shorts"
   - Update the demo section to show both the survival thriller (Keeper of Cape Vespers) and any documentary shorts.
4. Update `agent/SYSTEM_PROMPT.md` to reflect the broader scope.
5. Update `manifest.json` and `config.json` to use the new project name.
6. Verify the gh-pages site still loads after rename.
7. Update the v1.0.0 release body if it references the old name (release URLs auto-redirect, but the description text may need updating).

## Note on scope expansion

The user explicitly said: "The topics would still remain the same so be smart on that part." So the engine still does survival thrillers, but now also does documentary shorts. The rebrand reflects this: it's a documentary engine that can produce any cinematic short-form film.

## Acceptance

- Repo renamed to `ansaribilal14/documentary-engine`.
- README, landing page, system prompt, manifests all updated.
- Old URLs (superz1402/survival-cinema-agent → ansaribilal14/survival-cinema-agent → ansaribilal14/documentary-engine) redirect properly.
- gh-pages site loads at `https://ansaribilal14.github.io/documentary-engine/`.

## Status

- [ ] Not started
