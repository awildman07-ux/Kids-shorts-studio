# Kids Shorts Studio

## Episode 1 — The Mysterious Footprints

A phone-friendly animated preview with five timed scenes, animated forest elements, character motion, captions, scene controls, and voiceover text.

Open index.html in a browser to preview it.

## Free phone-only cloud renderer

The repository now includes a GitHub Actions workflow named **Render Kids Episode**. It uses Blender, FFmpeg, and an open natural-voice engine on a GitHub-hosted runner, then produces an Android-compatible MP4 as a downloadable workflow artifact.

From an Android phone:

1. Open the repository's **Actions** tab.
2. Select **Render Kids Episode**.
3. Tap **Run workflow**.
4. When the run finishes, download **little-wild-adventures-episode**.

The current renderer is the free production foundation. Character models, rigged acting clips, facial controls, and final environment assets belong in `production/assets/` and can be improved without changing the phone workflow.
