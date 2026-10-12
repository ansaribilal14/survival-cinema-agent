# Quickstart

## Prerequisites
- bash shell with: `python3` (3.10+), `ffmpeg` (with libx264 + subtitles filter), `curl`, `git`
- An image-generation CLI (default: `z-ai image`)
- A TTS CLI (default: `z-ai tts`)
- An LLM agent (Claude, GPT-4, Gemini, Super Z, etc.) for the creative phases

## Step 1 — Get the framework
```bash
git clone https://github.com/superz1402/survival-cinema-agent.git
cd survival-cinema-agent
```

## Step 2 — Write your story idea
```bash
cp STORY_IDEA_TEMPLATE.md story_idea.md
$EDITOR story_idea.md
```

A minimal `story_idea.md`:
```markdown
# Story Idea

**Working title:** The Last Signal
**Genre:** YA survival thriller
**Protagonist:**
- Age: 22
- Gender: female
- Ethnicity: Korean-American
- Identity: A wildfire-lookout observer on her second summer in a remote Montana tower
- Practical skill: fire-weather observation and radio protocol

**Setting:** A 40-foot fire-lookout tower in the Lolo National Forest, Montana,
accessible only by helicopter or a 14-mile trail.

**Premise:** Iris takes the summer job to grieve her mother's death. Three weeks
in, the radio dispatcher's voice changes — same mannerisms, wrong pauses. She
realizes someone has been recording the dispatcher for weeks and playing back
the recordings. Her own tower is the arsonist's next target.
```

## Step 3 — Run the pipeline
Give the framework + your story idea to an LLM agent. Tell the agent:

> Run the Survival Cinema Agent pipeline on `story_idea.md`. Use the system prompt at `agent/SYSTEM_PROMPT.md`. Execute every phase and produce all outputs. Do not stop at planning. Persist all artifacts to disk.

The agent will:
1. Read `agent/SYSTEM_PROMPT.md`
2. Read your `story_idea.md`
3. Execute `agent/pipeline.sh story_idea.md output_run/`
4. Fill in the creative-phase outputs (story bible, screenplay, style bible, QA findings)
5. Run the deterministic phases (image generation, narration, render)
6. Produce `output_run/output/final.mp4`

## Step 4 — Watch the film
```bash
open output_run/output/final.mp4
```

## Re-running
The pipeline is resumable. If it crashes midway:
```bash
./agent/pipeline.sh story_idea.md output_run/
```
Already-completed phases are skipped. To force a re-run of a specific phase:
```bash
rm output_run/checkpoints/image_progress.json   # forces Phase 7 to re-run
rm output_run/checkpoints/render_progress.json   # forces Phase 9 to re-run
```

## Troubleshooting
- **Agent stops at planning:** Re-prompt: "Execute every phase. Do not stop at planning. Persist all artifacts to disk."
- **Image generation fails:** Check `z-ai image --prompt "test" --output /tmp/test.png --size 1344x768`.
- **TTS fails:** Check `z-ai tts --input "test" --output /tmp/test.wav`.
- **Render fails:** Check `ffmpeg -version` (needs libass for subtitles filter).
- **Video too long/short:** Edit `target_runtime_minutes` in `story_idea.md` and re-run.

For more, see `docs/CUSTOMIZATION.md`.
