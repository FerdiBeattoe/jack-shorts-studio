# Jack SaaS Design Asset Pack v0.1

Purpose: controlled asset pack for a deterministic Jack SaaS short-video pipeline.

This pack separates **source references**, **approved production keyframes**, **missing assets still needed**, and **pipeline specs** so Claude Code/Codex can build a Remotion/FFmpeg renderer without guessing.

## Current approved production anchors

- `01_character/master_refs/jack_character_sheet_master.png` — master character identity reference.
- `01_character/keyframes/jack_01_forward_calculating.png` — start pose: leaning/concerned/calculating.
- `01_character/keyframes/jack_02_tie_fix_confident_smirk.png` — middle pose: leaning back with hand on tie.
- `01_character/keyframes/jack_03_turning_to_monitor.png` — end pose: turning attention back to PC.
- `06_audio/doug_episode_02_voice_current.mp3` — current voiceover file.

## Production rule

For V1, do **not** depend on Hedra/Kling/Runway/Luma. Use stills, controlled cuts, subtle camera moves, captions, and FFmpeg/Remotion rendering.

## Missing assets to generate before the pipeline becomes robust

See:
- `09_pipeline_specs/asset_manifest.json`
- `08_prompts/image_generation/missing_asset_generation_prompts.md`
- `09_pipeline_specs/production_asset_checklist.md`

## Naming rule

Use lowercase snake_case. Keep role prefixes:
- `jack_` for character frames.
- `office_` for backgrounds.
- `crm_` for screen inserts.
- `prop_` for objects.
- `caption_` for templates.
