# Customization

## Swapping the image provider
Edit `call_image_provider` in `agent/tools/06_generate_images.py`:

```python
def call_image_provider(prompt, output_path, size="1344x768"):
    # Example: OpenAI DALL-E 3
    # from openai import OpenAI
    # client = OpenAI()
    # response = client.images.generate(model="dall-e-3", prompt=prompt, size="1792x1024")
    # subprocess.run(["curl", "-sSL", response.data[0].url, "-o", str(output_path)])
    # return output_path.exists(), "ok"

    # Default: z-ai image CLI
    cmd = ["z-ai", "image", "--prompt", prompt, "--output", str(output_path), "--size", size]
    # ...
```

## Swapping the TTS provider
Edit `call_tts_provider` in `agent/tools/07_generate_narration.py`.

## Swapping the reference texts
Edit `DEFAULT_REFERENCES` in `agent/tools/01_acquire_references.py`.

## Changing the visual style
Edit `agent/tools/05_visual_development_scaffold.py` (default style bible) OR have the agent write a fresh `visual_development/style_bible.md` per run. The style anchor text (appended to every image prompt) is in `agent/tools/06_generate_images.py` as `ANCHOR`.

## Changing the runtime
Edit `target_runtime_minutes` in `story_idea.md`. The agent scales scene count and narration budget accordingly. Default 15 min → ~22 scenes, ~74 shots. For 25 min → ~36 scenes, ~120 shots.

## Adding music, ambience, SFX
In `agent/tools/08_render_video.py`, add a second audio input to the per-scene mux:
```python
cmd = ["ffmpeg", "-y", "-i", str(scene_video), "-i", str(narration_audio),
       "-i", str(ambience_audio),
       "-filter_complex", "[1:a][2:a]amix=inputs=2:duration=first:weights=1.0 0.3[a]",
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       str(scene_full)]
```

## Adding image-to-video animation
Use `z-ai video --image-url <url> --prompt "<motion>" --poll` per shot. Replace the static-image render in `agent/tools/08_render_video.py` with the animated clip.

## Adding multi-voice dialogue
For each dialogue line, call `z-ai tts` with a different voice per speaker. Concatenate dialogue chunks and interleave with scene narration.

## Changing the YouTube metadata format
Edit `agent/tools/09_thumbnail_packaging.py` to write a different metadata format.
