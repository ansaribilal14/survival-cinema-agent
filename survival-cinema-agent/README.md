# Survival Cinema Agent

> **One paragraph in. A finished film out.**
>
> An autonomous AI agent that takes a single story idea and produces a complete cinematic short film — original IP, 60+ AI-generated scene images, AI-synthesized narration, burned-in subtitles, a thumbnail, and a YouTube-ready metadata package.

**Live site:** https://superz1402.github.io/survival-cinema-agent/

---

## What this is

Survival Cinema Agent is an **agentic framework** — not a single app, but a system you give to an AI agent (Claude, GPT-4, Gemini, Super Z, etc.) along with a one-paragraph story idea. The agent reads the master system prompt, runs 11 phases, and produces a finished cinematic short film.

The framework handles the deterministic parts (downloading references, generating images, synthesizing narration, rendering video) with scripts. The agent handles the creative parts (writing the story, building the screenplay, defining the visual style, writing QA findings) guided by the system prompt.

## Quickstart

```bash
# 1. Clone
git clone https://github.com/superz1402/survival-cinema-agent.git
cd survival-cinema-agent

# 2. Write your story idea
cp STORY_IDEA_TEMPLATE.md story_idea.md
$EDITOR story_idea.md

# 3. Hand the repo + your story_idea.md to an LLM agent with this prompt:
#    "Run the Survival Cinema Agent pipeline on story_idea.md.
#     Use the system prompt at agent/SYSTEM_PROMPT.md.
#     Execute every phase and produce all outputs.
#     Do not stop at planning. Persist all artifacts to disk."

# 4. Your film is ready
open output_run/output/final.mp4
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

See `docs/INPUT_SPEC.md` for the full input format and field defaults.

## The 11 phases

| # | Phase | Type | Key output |
|---|---|---|---|
| 1 | Discover references | Deterministic | `reference_library/manifest.json` |
| 2 | Acquire & verify | Deterministic | cleaned texts |
| 3 | Analyze narratives | Creative | `reference_analysis/*.md` |
| 4 | Write the story | Creative | `story_development/complete_story.md` |
| 5 | Build screenplay | Creative + Deterministic | `screenplay/timeline.json` |
| 6 | Visual development | Creative | `visual_development/style_bible.md` |
| 7 | Generate images | Deterministic | `assets/images/*.png` |
| 8 | Synthesize narration | Deterministic | `assets/narration/narration.wav` |
| 9 | Render video | Deterministic | `output/final.mp4` |
| 10 | Thumbnail + YouTube | Mixed | `output/thumbnail.png` + metadata |
| 11 | QA reports | Creative | `reports/*.md` |

The master runner is `agent/pipeline.sh`. Each phase is resumable via `checkpoints/` JSON files.

## What you get

- **`output/final.mp4`** — the film (1920×1080, 30 fps, h264+AAC, subtitles burned in)
- **`output/thumbnail.png`** — cinematic YouTube thumbnail
- **`output/video_metadata.json`** — title, description, chapter timestamps, search keywords, AI disclosure
- **`story_development/`** — the complete original IP
- **`screenplay/`** — production-ready screenplay with shot list and image prompts
- **`assets/images/`** — 60-80 AI-generated scene images
- **`assets/narration/`** — concatenated narration audio
- **`reports/`** — 5 QA reports
- A local git commit with all source files

## The demo film

`examples/keeper_of_cape_vespers/` contains a complete reference run: *The Keeper of Cape Vespers*, a 12.21-minute YA survival thriller.

- **Protagonist:** Iris Vaughn, 22, mixed Filipina-American, photographer/lighthouse-keeper
- **Setting:** Cape Vespers Island, Salish Sea, Pacific Northwest
- **Plot:** A grieving niece discovers her aunt's coded journal; the aunt was murdered by a smuggler; the lighthouse inspector is complicit; Iris rigs a fog-signal whistle to broadcast an SOS in a storm
- **Stats:** 22 scenes, 74 shots, 74 AI-generated images, 22 narration chunks (~12 min), 5 QA reports, all PASS

## Why this design

**Female-centric by default.** Protagonist is a young adult woman (20-25) with substantial agency, a specific practical skill, a credible weakness, and a believable arc. Female supporting characters have independent motives.

**The midpoint reveal is a moral fact, not a monster.** The strongest thriller structure reveals a fact at midpoint that retroactively re-reads the first half as sinister.

**The escalation ladder.** Each new act replaces the previous threat with a strictly worse one.

**Frame-narrative voice.** Narrate from a survivor who has lost someone.

**Single-exit geography.** Closed islands, single docks, single roads.

**Antagonist logic the audience can almost follow.** The villain's rationale should be coherent for at least three seconds before rejection.

**Public-domain references.** Project Gutenberg works (Poe 1838, London 1915, Wells 1896) are used for narrative-technique research only. No content from them is reproduced. Originality audit is mandatory.

**Provider-agnostic.** Swap image generator, TTS engine, or LLM orchestrator with a single function edit. See `docs/CUSTOMIZATION.md`.

## Documentation

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the 3-layer system design
- **[docs/INPUT_SPEC.md](docs/INPUT_SPEC.md)** — the `story_idea.md` format
- **[docs/PHASES.md](docs/PHASES.md)** — the 11 phases in detail
- **[docs/OUTPUTS.md](docs/OUTPUTS.md)** — the full output directory tree
- **[docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md)** — swapping providers, adding music, image-to-video
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** — step-by-step walkthrough
- **[agent/SYSTEM_PROMPT.md](agent/SYSTEM_PROMPT.md)** — the master directive
- **[STORY_IDEA_TEMPLATE.md](STORY_IDEA_TEMPLATE.md)** — copy to `story_idea.md` and fill in

## Environment expectations

- bash shell with `python3` (3.10+), `ffmpeg` (libx264 + subtitles filter), `curl`, `git`
- An image-generation CLI (default: `z-ai image`)
- A TTS CLI (default: `z-ai tts`)
- An LLM agent (Claude, GPT-4, Gemini, Super Z, etc.) for the creative phases

## License

MIT — see [LICENSE](LICENSE).

The framework code is MIT-licensed. Each produced film is the original IP of the user who supplied the story idea. Reference texts used during analysis are public-domain works from Project Gutenberg.

## Acknowledgements

Reference analysis uses three public-domain works from Project Gutenberg:
- Edgar Allan Poe, *The Narrative of Arthur Gordon Pym of Nantucket* (1838)
- Jack London, *The Scarlet Plague* (1915)
- H. G. Wells, *The Island of Doctor Moreau* (1896)

These works are used for narrative-technique research only. No content from them is reproduced in the films produced by this system.

## Built by

**Super Z** — an autonomous production run. The framework, the demo film, the documentation, and the landing page were all produced by an AI agent executing the system prompt on itself.
