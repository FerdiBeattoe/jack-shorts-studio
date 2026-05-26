# Jack Engine Capability Audit

Date: 2026-05-26

## Summary

The current engine can render a finished Remotion short from fallback still images, captions, and master audio. It cannot yet generate or animate 15-20 unique visual frames per second from audio.

The right free-stack path is not AI-generating 525-800 individual images for a 35-40 second clip. The right path is to use approved transparent PNG puppet parts, Rhubarb mouth cues, local pose/animation rules, and Remotion's normal 30 fps renderer. Remotion then creates every video frame deterministically.

## Current Capability

| Area | Status | Notes |
| --- | --- | --- |
| Remotion render shell | Present | `DougEp02` composition registered in `src/Root.tsx`. |
| FPS / resolution | Present | `Portrait-1080p` is 1080x1920 at 30 fps. |
| Audio playback | Present | `public/audio/doug_episode_02_voice_current.mp3` is wired into the composition. |
| Still-image scene rendering | Present | `JackScene.tsx` renders `<Img>` with Ken Burns pan/zoom. |
| Captions | Present | `JackCaption.tsx` is used per timing beat. |
| Episode 02 fallback readiness | Present | `node scripts/check-episode-assets.mjs` reports ready for stills render. |
| Animation clip ingestion | Planned | Docs describe `<Video>` replacement, but `JackScene.tsx` currently only renders `<Img>`. |
| Puppet-layer Remotion rig | Missing | No `JackPuppet` component yet for layering head/body/mouth/eyes/brows. |
| Rhubarb lip sync | Missing | `rhubarb` is not on PATH. No cue JSON generation script yet. |
| FFmpeg CLI | Missing | `ffmpeg` is not on PATH. Remotion can still render, but direct FFmpeg assembly/post is not currently available from shell. |
| AI still generator | Present but limited | `scripts/generate-stills.mjs` drives Codex to generate one still per beat, not per-frame animation. |

## Stills-per-Second Feasibility

Requested target:

- 15 stills/sec for 35 sec = 525 stills.
- 15 stills/sec for 40 sec = 600 stills.
- 20 stills/sec for 35 sec = 700 stills.
- 20 stills/sec for 40 sec = 800 stills.

That is not a good AI-image-generation target. It will be slow, expensive, visually inconsistent, and hard to lip-sync. The current `scripts/generate-stills.mjs` is designed for one still per story beat from `assets/cut_1a/timing_map.json` (currently 23 beats), not hundreds of frames.

Recommended interpretation:

- Use Remotion at 30 fps for the final render.
- Update puppet pose and mouth state at 12-20 fps if a held-frame/limited-animation feel is desired.
- Let Remotion render the actual 30 fps output frames.
- Use Rhubarb cues to swap mouth PNGs at phoneme boundaries.
- Use lightweight procedural motion for eyes, brows, head bob, body lean, tie motion, and hand gestures.

## Best Free-Stack Architecture

1. Approved transparent PNG puppet assets.
2. Rhubarb converts voiceover audio to mouth cue JSON.
3. A local cue mapper converts Rhubarb mouth labels to Jack mouth assets.
4. A `JackPuppet.tsx` Remotion component composites body, topwear, head, eyes, brows, mouth, hands, tie, and environment.
5. Animation rules drive small movements from frame number and shot timing.
6. Remotion renders final H.264 MP4 at 1080x1920, 30 fps.
7. FFmpeg is optional for post-processing once installed.

## Needed Engine Work

### Priority 1: Local Puppet Renderer

Create a Remotion puppet component:

- `src/components/JackPuppet.tsx`
- Use transparent PNG layers from `assets/puppet/layers/`.
- Support per-shot pose states: front, 3/4, tie-fix, side-eye.
- Support mouth swaps by current Rhubarb cue.
- Support blink, brow, pupil, tie sway, and hand/arm transforms.

### Priority 2: Rhubarb Cue Pipeline

Add scripts:

- `scripts/run-rhubarb-lipsync.mjs`
- `scripts/map-rhubarb-to-jack-mouths.mjs`

Expected output:

- `assets/lipsync/doug_episode_02_rhubarb.json`
- `assets/lipsync/doug_episode_02_jack_mouth_cues.json`

Blocked until `rhubarb` is installed or vendored.

### Priority 3: Replace Still Scene With Puppet Scene

Update the episode composition so each beat can choose:

- fallback still image,
- puppet-driven local animation,
- or exported video clip.

This keeps the current stills pipeline working while the puppet path matures.

### Priority 4: Cap Runtime to 35-40 Seconds

Current Episode 02 is 49.8s because it matches the full MP3. For Shorts/TikTok testing, make a new cutdown composition:

- `DougEp02ShortTest`
- target 35-40 seconds,
- tightened caption map,
- fewer dead-air holds,
- keep the master audio trimmed or use a shortened voiceover file.

### Priority 5: FFmpeg

Install or vendor FFmpeg when we need:

- manual image-sequence assembly,
- audio trimming,
- probe reports,
- compression variants,
- platform export tests.

Right now `where ffmpeg` fails.

## Current Render State

`node scripts/check-episode-assets.mjs` result:

- Master audio: present.
- Animation clips: 0 / 7 present.
- Fallback stills: 7 / 7 present.
- Render readiness: ready for stills render, not animated render.
- Timeline: 49.8 seconds at 30 fps = 1494 frames.

## Design Decision

Do not build a 15-20 AI-generated-stills-per-second engine. Build a 30 fps Remotion puppet renderer whose *pose/mouth state changes* can be quantized to 12-20 fps when we want a snappy limited-animation look.

That gives us:

- fast iteration,
- consistent Jack identity,
- Rhubarb-driven lip sync,
- reusable puppet assets,
- cheaper renders,
- and a clean migration path to the paid stack later.
