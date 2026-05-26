# Claude Code / Codex Audit Prompt

Enable auto mode.

You are working inside `jack-shorts-studio/`.

Goal: create a deterministic local short-video renderer from this asset pack.

V1 must use Remotion + FFmpeg only. No cloud video generation, no lip-sync, no paid APIs.

First inspect this asset pack:
- `00_README/README.md`
- `09_pipeline_specs/asset_manifest.json`
- `09_pipeline_specs/production_asset_checklist.md`
- `09_pipeline_specs/doug_episode_02_timing_map.json`
- `05_brand/captions/caption_style_guide.md`

Then audit these repos by cloning into `research/` only:
1. https://github.com/jhartquist/claude-remotion-kickstart
2. https://github.com/digitalsamba/claude-code-video-toolkit
3. https://github.com/browser-use/video-use
4. https://github.com/kevinwatt/ffmpeg-mcp-lite
5. https://github.com/jordanrendric/claude-video-vision

Do not install dependencies yet. Do not run remote scripts. Do not execute repo scripts.

Output:
1. Recommended base repo or direct Remotion setup.
2. Dependency list.
3. Security risks.
4. Implementation plan for Doug Episode 02.
5. Exact next commands for Windows.
