# Remotion Animation Integration Plan

**Version:** 1.0  
**Date:** 2026-05-19  
**Status:** Spec — implementation pending Character Animator exports

---

## Overview

When Character Animator shot exports are ready, they replace the still images in the Remotion composition. The change is surgical: `JackScene.tsx` is the only component that changes. Everything else — captions, audio, timing, Ken Burns — either stays or is retired cleanly.

---

## Current State (V1 — stills)

```tsx
// src/components/JackScene.tsx
<Img
  src={imageSrc}
  style={{ ...kenBurns }}
/>
```

`JackScene` receives an `imageSrc` string and applies Ken Burns via `interpolate()`. This is the entire rendering surface for Jack's visuals.

---

## Target State (V2 — animated clips)

```tsx
// src/components/JackScene.tsx (after integration)
<Video
  src={clipSrc}
  muted={true}        // audio lives in master <Audio> in Composition.tsx
  style={{
    width: "100%",
    height: "100%",
    objectFit: "cover",
  }}
/>
```

`Video` is a Remotion built-in. No new dependencies. `muted={true}` is critical — the Character Animator export contains the voiceover audio baked in; we do not want it. The master `<Audio>` track in `Composition.tsx` drives all audio.

---

## Changes Required

### 1. `src/compositions/doug-ep02/timing.ts`

Add a `clip` field to the `Beat` interface and each beat entry:

```typescript
// Add to Beat interface:
clip?: string;   // path to animation clip relative to public/, if available

// Example beat entry:
{
  id: "beat_01",
  startSeconds: 0.0,
  endSeconds: 2.8,
  image: "images/jack_01_forward_calculating.png",    // fallback still (keep forever)
  clip: "animation/shot_exports/shot_01.mp4",          // animated clip when available
  caption: "Update on the Doug situation.",
  kenBurns: { ... },
}
```

The `clip` field is optional. When undefined, `JackScene` renders the still image. When present and the file exists, it renders the video clip.

### 2. `src/components/JackScene.tsx`

Add a `clipSrc` prop. When provided, render `<Video>` instead of `<Img>`. Ken Burns is disabled for animated clips.

```tsx
import { Img, Video, interpolate, useCurrentFrame } from "remotion";

interface JackSceneProps {
  imageSrc: string;
  durationInFrames: number;
  clipSrc?: string;             // NEW: optional animated clip
  kenBurns?: Partial<KenBurnsParams>;
}

export const JackScene: React.FC<JackSceneProps> = ({
  imageSrc,
  durationInFrames,
  clipSrc,
  kenBurns = {},
}) => {
  // If animated clip available, render Video
  if (clipSrc) {
    return (
      <div style={{ position: "absolute", inset: 0, backgroundColor: "#1a1a1a" }}>
        <Video
          src={clipSrc}
          muted
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>
    );
  }

  // Fallback: render still image with Ken Burns
  // ... existing Ken Burns <Img> code unchanged ...
};
```

### 3. `src/compositions/doug-ep02/Composition.tsx`

Pass `clipSrc={staticFile(beat.clip)}` to `JackScene` when `beat.clip` is defined:

```tsx
<JackScene
  imageSrc={staticFile(beat.image)}
  clipSrc={beat.clip ? staticFile(beat.clip) : undefined}
  durationInFrames={durationInFrames}
  kenBurns={beat.kenBurns}
/>
```

No other changes to `Composition.tsx`. The `<Audio>` master track stays. Captions stay. Series timing stays.

---

## Audio Strategy

| Source | Role | Action |
|--------|------|--------|
| `public/audio/doug_episode_02_voice_current.mp3` | Master voiceover | **Keep in Remotion `<Audio>`** — this is the single audio source |
| Character Animator export audio | Baked-in duplicate of the same voiceover | **Muted** via `muted={true}` on `<Video>` — not used |

Do not remove the master `<Audio>` from `Composition.tsx`. Do not rely on the clip audio. This keeps audio control centralised in Remotion.

---

## Clip Format Requirements

Character Animator exports must match these specs for Remotion compatibility:

| Property | Required Value |
|---------|---------------|
| Container | `.mp4` (H.264) preferred. `.mov` (ProRes) requires transcoding first. |
| Resolution | 1080 × 1920 (same as Remotion canvas) |
| Frame rate | 30fps (must match Remotion FPS) |
| Duration | Must be ≥ beat duration (extra tail frames are fine; Remotion clips at Series boundary) |
| Codec | H.264 for direct Remotion use. ProRes 4444 for intermediate quality. |
| Audio | Included but muted by Remotion. |

**FFmpeg transcoding command** (for converting ProRes exports from Character Animator):
```
ffmpeg -i shot_01_prores.mov -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -r 30 public/animation/shot_exports/shot_01.mp4
```

---

## Rollout Strategy

Shot integration can be done one shot at a time. The `clip` field is optional — any beat without a `clip` value continues rendering the still image. This means:

1. Generate shot_04 (tie-fix, most iconic). Test in Remotion.
2. If clean, add shot_05, shot_06 (smug sequence).
3. Add shot_01, shot_02, shot_03 (opening sequence).
4. Add shot_07 (closing turn).
5. Final full-animation render.

At no point does the episode break — stills are always the fallback.

---

## Validation

After adding a clip, verify with `pnpm run dev` (Remotion Studio) before full render:
- Scrub through the beat — does the animation play?
- Check for audio bleed (clip audio should be silent)
- Verify caption timing is unchanged
- Check clip/caption alignment at beat boundaries

Run `node scripts/check-episode-assets.mjs` to confirm clip file presence before rendering.
