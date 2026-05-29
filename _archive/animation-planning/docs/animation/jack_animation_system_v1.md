# Jack Animation System v1

**Version:** 1.0  
**Date:** 2026-05-19  
**Status:** Scaffolding — production not yet started

---

## Hard Rule

> **Remotion edits and renders. Adobe Character Animator performs Jack.**

These two tools have non-overlapping jobs and must never be substituted for each other:

| Tool | Role | Does NOT do |
|------|------|-------------|
| Adobe Character Animator | Jack's facial animation, lip sync, expression triggers, body physics | Video editing, captions, final export format |
| Remotion (React) | Caption timing, hard cuts, Ken Burns on stills, audio sync, final H.264 MP4 | Character animation, lip sync |
| FFmpeg | File conversion, format QC, probe | Either of the above |
| Claude / Codex | Spec authoring, prompt generation, manifest validation, workflow scripts | Rendering video |

Violating this rule means duplicating effort or introducing undeletable complexity.

---

## System Overview

The Jack Animation System converts a script into a finished TikTok short following this chain:

```
Script (TXT)
  └─▶ Voiceover MP3 (recorded externally)
        └─▶ Adobe Character Animator
              ├─ Puppet PSD (layered Jack puppet)
              ├─ Lip sync from MP3
              ├─ Expression triggers per beat
              └─▶ Exported shot clips (MP4 per shot)
                    └─▶ Remotion Composition
                          ├─ <Video> per shot clip (replaces <Img>)
                          ├─ <Audio> master voiceover
                          ├─ <JackCaption> beat-driven captions
                          └─▶ Final 1080×1920 H.264 MP4
```

---

## Production Workflow (Step by Step)

### Step 1 — Script Lock
- Script is finalized and approved in `assets/.../07_scripts/`.
- No changes to script after voiceover is recorded.

### Step 2 — Voiceover Recording
- Voiceover MP3 is recorded and placed in `public/audio/`.
- `ffprobe` confirms exact duration (currently: 49.791610s for Episode 02).
- Timing map JSON is updated to match MP3 duration.

### Step 3 — Puppet Asset Generation
- Layered PNG assets are generated using prompts in `prompts/animation/`.
- Assets are named per `jack_puppet_asset_spec_v1.md` and stored in `assets/puppet/layers/`.
- `scripts/validate-jack-puppet-pack.mjs` confirms all V1-required layers are present.

### Step 4 — Puppet Assembly in Photoshop
- PNG layers are assembled into a layered PSD per `character_animator_layer_naming_v1.md`.
- PSD is saved to `assets/puppet/psd/jack_puppet_v1.psd`.
- Mouth group contains all viseme layers per `jack_viseme_system_v1.md`.
- Expression swap sets built per `jack_expression_system_v1.md`.

### Step 5 — Character Animator Rigging
- PSD is opened in Adobe Character Animator.
- Auto-tagging is verified; manual tags applied where needed.
- Face tracking and lip sync are tested against the voiceover MP3.
- Triggers assigned to expression states in the Triggers panel.

### Step 6 — Shot Performance
- Each shot from `episode_02_animation_shotlist.md` is performed in a Character Animator Take.
- Expression triggers are fired on the correct beats.
- Lip sync is driven by the voiceover MP3 directly in Character Animator.
- Takes are reviewed, trimmed, and approved.

### Step 7 — Shot Export
- Each approved take is exported as an MP4 (ProRes or H.264 at 30fps, 1080×1920).
- Exported clips are saved to `public/animation/shot_exports/shot_NN.mp4`.
- `scripts/check-episode-assets.mjs` confirms all clips are present.

### Step 8 — Remotion Final Assembly
- `JackScene.tsx` is updated to use `<Video>` instead of `<Img>` per `remotion_animation_integration_plan.md`.
- Clip audio is muted; master voiceover MP3 remains in `<Audio>` in Composition.tsx.
- `pnpm run render` produces the final 1080×1920 H.264 MP4.

---

## V1 vs V2 Scope

### V1 (current — stills renderer)
- Still images only (`<Img>` in JackScene.tsx)
- No lip sync
- Ken Burns camera moves
- Beat-driven captions
- Master voiceover MP3

### V1.5 (animation system — this document)
- All scaffold, specs, and prompts are written (this task)
- Assets are generated using prompt book
- Puppet PSD is assembled
- Character Animator rig is built and tested

### V2 (animation renderer)
- Character Animator shot exports replace stills
- `<Video>` replaces `<Img>` in JackScene.tsx
- Lip sync is driven by Character Animator
- Full episode renders from animated clips

### V3+ (future)
- Multi-character scenes
- Motion backgrounds
- AI-generated background clip inserts (Kling/Runway/LTX-2)
- Automated social export (TikTok upload API)

---

## Directory Structure

```
jack-shorts-studio/
├── assets/
│   └── puppet/
│       ├── layers/          ← PNG source layers for PSD assembly
│       │   ├── head/        ← Head, face, neck layers
│       │   ├── mouth/       ← Viseme mouth layers
│       │   ├── eyes/        ← Eye layers (open/half/closed/pupils)
│       │   ├── eyebrows/    ← Eyebrow expression layers
│       │   ├── body/        ← Torso, arms, hands, tie layers
│       │   └── environment/ ← Background, desk, chair, monitor layers
│       ├── psd/             ← Assembled PSDs for Character Animator
│       └── refs/            ← Reference sheets (expressions, visemes)
├── public/
│   └── animation/
│       └── shot_exports/    ← Character Animator exports (served by Remotion)
│           ├── shot_01.mp4
│           ├── shot_02.mp4
│           └── ...
├── docs/animation/          ← All system specs (this directory)
├── prompts/animation/       ← Image generation prompt books
├── manifests/               ← JSON asset manifests for validation
└── scripts/                 ← Validation and check scripts
```

---

## File Format Standards

| Asset type | Format | Resolution | Notes |
|-----------|--------|-----------|-------|
| Puppet layers | PNG-32 (RGBA) | Min 1080px on longest axis | Transparent background mandatory |
| Reference sheets | PNG-32 or JPEG | Min 2000px wide | No transparency needed |
| Assembled puppet PSD | .psd | Canvas: 1920×1920 or larger | Layer order per naming spec |
| Character Animator project | .puppet | — | Adobe proprietary format |
| Exported shot clips | .mp4 (H.264) or .mov (ProRes 4444) | 1080×1920, 30fps | ProRes for intermediate; H.264 for Remotion |
| Final render | .mp4 (H.264) | 1080×1920, 30fps | Produced by Remotion |
