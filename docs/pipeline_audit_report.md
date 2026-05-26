# Jack Shorts Studio — Pipeline Audit Report

**Date:** 2026-05-19  
**Purpose:** Repo audit, architecture decision, and implementation plan for Doug Episode 02 V1 render.

---

## 1. Recommended Base Approach

**Use Remotion 4 + React/TypeScript + pnpm + FFmpeg directly.**

- Renderer: Remotion renders frames, outputs H.264 MP4.
- Timing: JSON-driven beats (`doug_episode_02_timing_map.json`) map image/caption switches to seconds.
- Camera: Ken Burns zooms/pans via Remotion's `interpolate()` — no external library needed.
- Captions: Beat-driven text overlay component, styled to Jack brand spec.
- Audio: Remotion `<Audio>` tag loads the MP3; sync is automatic via frame count.
- No MCP server needed for V1.
- No cloud API needed for V1.

---

## 2. Repo-by-Repo Audit

---

### Repo 1: `claude-remotion-kickstart` — jhartquist
**URL:** https://github.com/jhartquist/claude-remotion-kickstart

| Item | Finding |
|------|---------|
| What it does | Remotion + React/TS video starter kit with pre-built components: TitleSlide, Caption, Music, BRollVideo, ZoomableVideo, Diagram. Includes `Portrait-1080p` (1080×1920) preset, `secondsToFrames()` utility, and transcript-timing pattern. |
| Suitable for Jack Shorts? | YES. Directly matches the V1 need: vertical 9:16, timed captions, audio sync, still image rendering. |
| Too broad or risky? | No. Scope is exactly right. The "vibe coding" warning is honest but the core code is clean and minimal. |
| Runtime/deps | Node.js 20+, pnpm, TypeScript 5.8, React 19, Remotion 4.0.382, Tailwind v4, Zod |
| FFmpeg / Remotion / MCP / APIs | Remotion (core). FFmpeg required for render output. Optional MCPs for Playwright, ElevenLabs, Replicate — all deferred. |
| Secrets required? | Not for V1. Replicate/Deepgram/ElevenLabs are optional and only used by slash commands. |
| Risky install scripts? | None. `package.json` scripts: `dev`, `build`, `upgrade`, `lint` only. No postinstall, no preinstall. pnpm lockfile confirmed clean. |
| License | MIT (John Hartquist, 2025) ✅ |
| **Verdict** | **USE AS BASE. Copy structure and key utilities. Do not use it as-is — adapt for Jack's portrait format and JSON timing.** |

---

### Repo 2: `claude-code-video-toolkit` — digitalsamba
**URL:** https://github.com/digitalsamba/claude-code-video-toolkit

| Item | Finding |
|------|---------|
| What it does | Full AI-native video production workspace: Remotion, ElevenLabs, ACE-Step music AI, LTX-2 video generation, Playwright browser recording, RunPod/Modal cloud GPU, Cloudflare R2 storage, MoviePy, Qwen3-TTS. Designed for sprint-review and product-demo style content. |
| Suitable for Jack Shorts? | Too broad for V1. Contains a lot of what V2 will need (voice, AI clips, brand profiles) but the cloud GPU setup adds significant friction and cost. |
| Too broad or risky? | YES — too broad. Cloud GPU, cloud storage, AI video generation are all explicitly deferred from Jack V1 scope. |
| Runtime/deps | Node.js 18+, Python 3.9+, pnpm. Python: elevenlabs, boto3, Pillow, moviepy, matplotlib. |
| FFmpeg / Remotion / MCP / APIs | Remotion (core renderer). FFmpeg (asset processing). No MCP server of its own. ElevenLabs API, RunPod/Modal cloud GPU, Cloudflare R2. |
| Secrets required? | Yes — ElevenLabs, RunPod, Cloudflare R2 for full feature use. Basic Remotion render works without them. |
| Risky install scripts? | `python3 scripts/migrate_to_codex.py --force` writes to `~/.codex/skills`. Not harmful but intrusive. Don't run this. |
| License | MIT (Digital Samba, 2024) ✅ |
| **Verdict** | **MINE FOR IDEAS only. The Remotion skill patterns, brand profile concept, and FFmpeg skill design are good V2 references. Do not use as V1 base — too many moving parts.** |

---

### Repo 3: `video-use` — browser-use
**URL:** https://github.com/browser-use/video-use

| Item | Finding |
|------|---------|
| What it does | Conversation-driven video editor for raw footage. Transcribes with ElevenLabs Scribe, cuts filler words, color grades, burns subtitles. Designed for talking-head footage editing, not synthesis from still images. |
| Suitable for Jack Shorts? | NO. Wrong tool entirely. Jack has no raw footage — it uses still images and a pre-recorded MP3. This tool's core loop (transcribe → cut → grade → subtitle) assumes video footage as input. |
| Too broad or risky? | Wrong scope. ElevenLabs required for transcription (costs money). Python deps: librosa, matplotlib, Pillow, numpy. Optional: Manim. |
| Runtime/deps | Python 3.10+, FFmpeg required, ElevenLabs API key required. |
| FFmpeg / Remotion / MCP / APIs | FFmpeg (core). ElevenLabs Scribe (required). Remotion/Manim/HyperFrames optional animation engines. |
| Secrets required? | YES — ElevenLabs API key hard-required for transcription. |
| Risky install scripts? | `uv sync` or `pip install -e .` — standard Python install. No dangerous scripts. |
| License | MIT ✅ |
| **Verdict** | **IGNORE for V1 and V2. Not relevant to Jack's still-image synthesis pipeline.** |

---

### Repo 4: `ffmpeg-mcp-lite` — kevinwatt
**URL:** https://github.com/kevinwatt/ffmpeg-mcp-lite

| Item | Finding |
|------|---------|
| What it does | MCP server exposing 8 FFmpeg tools: `ffmpeg_get_info`, `ffmpeg_convert`, `ffmpeg_compress`, `ffmpeg_trim`, `ffmpeg_extract_audio`, `ffmpeg_merge`, `ffmpeg_extract_frames`, `ffmpeg_add_subtitles`. Clean one-file-per-tool architecture. Published on PyPI. |
| Suitable for Jack Shorts? | Potentially useful for V2 interactive work (e.g., letting Claude burn-in subtitles or inspect renders). For V1, Remotion handles rendering end-to-end and FFmpeg can be called directly from shell — no MCP layer needed. |
| Too broad or risky? | No — minimal scope. Only dependency is `mcp>=1.0.0` (the MCP Python SDK). |
| Runtime/deps | Python 3.10+, uv, FFmpeg/FFprobe binaries. Zero cloud deps. |
| FFmpeg / Remotion / MCP / APIs | FFmpeg (core). MCP protocol. No APIs, no secrets. |
| Secrets required? | None. |
| Risky install scripts? | None. `pyproject.toml` is clean: hatchling build, single dep. |
| License | MIT ✅ |
| **Verdict** | **DEFER to V2. When we want interactive FFmpeg operations from within Claude Code sessions (e.g., probing renders, burning subtitles ad-hoc), this is the cleanest option. Can be added with `claude mcp add ffmpeg uvx ffmpeg-mcp-lite` — zero setup friction. Skip for V1.** |

---

### Repo 5: `claude-video-vision` — jordanrendric
**URL:** https://github.com/jordanrendric/claude-video-vision

| Item | Finding |
|------|---------|
| What it does | Claude Code plugin that lets Claude "watch" existing videos by extracting frames (FFmpeg) and transcribing audio (Gemini, Whisper, or OpenAI). A perception/analysis tool, not a creation tool. |
| Suitable for Jack Shorts? | NO. This is for video understanding/analysis. Jack Shorts needs video creation from still images + audio. |
| Too broad or risky? | Wrong scope. The auto-install via `/plugin marketplace add` + `npx` is a mild surface concern — inspect before running. |
| Runtime/deps | Node.js 20+, FFmpeg, optional yt-dlp. Gemini, OpenAI, or local Whisper for audio. |
| FFmpeg / Remotion / MCP / APIs | FFmpeg (frame extraction). MCP server (Node.js). Optional Gemini API key or OpenAI API key. |
| Secrets required? | API key needed for audio backend (Gemini/OpenAI), or local Whisper (free but requires model download). |
| Risky install scripts? | `prepublishOnly: npm run build && npm test` — not risky for users. The `/plugin marketplace add` mechanism deserves caution (inspect before running). |
| License | MIT ✅ |
| **Verdict** | **IGNORE. Not relevant to creation pipeline. Potentially useful if we ever need to QC/review rendered outputs in a future V3, but not now.** |

---

## 3. Which Repo to Use as Base

**`claude-remotion-kickstart`** — copy the following files/patterns, then adapt:

- `src/presets.ts` — change `Portrait-1080p` fps to 30 (TikTok, not 60)
- `src/config.ts` — `secondsToFrames()` utility (keep as-is)
- `src/utils/createComposition.tsx` — keep as-is
- `src/components/Caption.tsx` — adapt for Jack's caption style (larger font, punchline-beat mode)
- `remotion.config.ts` — keep structure, configure JPEG output

Do not copy: `asciinema`, `Diagram`, `Code`, `Screenshot`, `BRollVideo` components — not needed for V1.

---

## 4. Repos to Ignore for Now

| Repo | Reason |
|------|--------|
| `video-use` | Footage-cutting tool, wrong input type for Jack |
| `claude-video-vision` | Video analysis/perception, not creation |
| `claude-code-video-toolkit` | Too broad (cloud GPU, AI video), V2 ideas only |
| `ffmpeg-mcp-lite` | Useful V2 MCP addition, no value in V1 |

---

## 5. Tooling Decision

| Tool | V1 Decision | Reason |
|------|-------------|--------|
| Remotion MCP (`@remotion/mcp`) | Defer | Remotion Studio + `pnpm exec remotion render` covers V1 needs directly |
| FFmpeg MCP (`ffmpeg-mcp-lite`) | Defer | Remotion renders H.264 directly; no interactive FFmpeg needed in V1 |
| GitHub MCP | Skip entirely | No remote repo; working locally |
| Filesystem MCP | Not needed | Claude Code has direct file access via Read/Write/Glob/Grep tools |
| ElevenLabs MCP | Defer to V2 | Voiceover already recorded for Ep02 |
| Replicate/Veo/LTX-2 | Deferred to V2 | Explicitly out of V1 scope per project rules |
| Claude Code skills | Not needed for V1 | The composition is hand-coded, not generated |

**Conclusion: No MCP servers needed for V1. Direct shell + pnpm + Remotion render is sufficient.**

---

## 6. Minimal Architecture for Jack Shorts Studio

```
jack-shorts-studio/
├── public/
│   ├── images/          ← copy/symlink Jack keyframe PNGs here
│   └── audio/           ← copy/symlink MP3 here
├── src/
│   ├── components/
│   │   ├── JackScene.tsx        ← <Img> + Ken Burns via interpolate()
│   │   └── JackCaption.tsx      ← beat-driven TikTok caption overlay
│   ├── compositions/
│   │   └── doug-ep02/
│   │       ├── Composition.tsx  ← <Series> of JackScene + JackCaption + Audio
│   │       ├── timing.ts        ← imports doug_episode_02_timing_map.json
│   │       └── segments/        ← one file per beat (optional, can be inline)
│   ├── utils/
│   │   └── createComposition.tsx
│   ├── config.ts         ← secondsToFrames, DEFAULT_FPS = 30
│   ├── presets.ts        ← Portrait-1080p at 30fps
│   └── Root.tsx          ← registers DougEp02 composition
├── package.json
├── pnpm-lock.yaml
├── remotion.config.ts
└── tsconfig.json
```

Assets path: `public/` is Remotion's static directory. Files are referenced via `staticFile("images/jack_01_forward_calculating.png")`.

---

## 7. Exact Windows Setup Commands (next step)

Run these in order, one block at a time, and confirm each succeeds before continuing.

```powershell
# Step 1: Verify Node.js (need 20+)
node --version

# Step 2: If Node < 20, install it
winget install OpenJS.NodeJS.LTS

# Step 3: Install pnpm globally
npm install -g pnpm
pnpm --version

# Step 4: Install FFmpeg (needed by Remotion renderer)
winget install FFmpeg
ffmpeg -version

# Step 5: Verify FFmpeg is on PATH (may need to restart terminal)
where ffmpeg

# Step 6: From inside jack-shorts-studio/, init the project
pnpm init

# Step 7: Install Remotion and React
pnpm add remotion @remotion/cli react react-dom
pnpm add -D typescript @types/react tsx

# Step 8: Verify Remotion installed
pnpm exec remotion --version
```

> Note: Remotion is free for solo/small personal use. Companies with 3+ full-time employees must purchase a license. Verify this applies to your situation at https://www.remotion.dev/docs/license

---

## 8. Exact Package/Dependency List

### `package.json` (production deps)
```json
{
  "dependencies": {
    "remotion": "^4.0.382",
    "@remotion/cli": "^4.0.382",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "typescript": "^5.8.2",
    "@types/react": "^19.0.0",
    "tsx": "^4.21.0"
  },
  "scripts": {
    "dev": "remotion studio",
    "render": "remotion render DougEp02 --output renders/draft/doug_ep02_draft.mp4"
  }
}
```

**Intentionally excluded (no need for V1):**
- `@remotion/tailwind-v4` — Jack captions can use inline styles; no Tailwind needed
- `zod` — timing config is a simple JSON import, no validation schema needed
- `mermaid`, `shiki`, `asciinema-player`, `@terrastruct/d2` — not needed

---

## 9. Proposed Folder Structure (full V1)

```
jack-shorts-studio/
├── assets/                     ← original asset pack (do not modify)
│   └── jack_saas_design_asset_pack_v0_1/...
├── docs/
│   └── pipeline_audit_report.md  ← this file
├── public/
│   ├── images/
│   │   ├── jack_01_forward_calculating.png
│   │   ├── jack_02_tie_fix_confident_smirk.png
│   │   └── jack_03_turning_to_monitor.png
│   └── audio/
│       └── doug_episode_02_voice_current.mp3
├── renders/
│   ├── draft/
│   └── final/
├── research/                   ← cloned audit repos (read-only)
│   ├── claude-remotion-kickstart/
│   ├── claude-code-video-toolkit/
│   ├── video-use/
│   ├── ffmpeg-mcp-lite/
│   └── claude-video-vision/
├── src/
│   ├── components/
│   │   ├── JackScene.tsx
│   │   └── JackCaption.tsx
│   ├── compositions/
│   │   └── doug-ep02/
│   │       ├── Composition.tsx
│   │       ├── timing.ts
│   │       └── segments/
│   ├── utils/
│   │   └── createComposition.tsx
│   ├── config.ts
│   ├── presets.ts
│   └── Root.tsx
├── package.json
├── pnpm-lock.yaml
├── remotion.config.ts
└── tsconfig.json
```

---

## 10. First Implementation Plan: Doug Episode 02

### Beat map (from `doug_episode_02_timing_map.json`)

| Beat | Start | End | Asset | Caption |
|------|-------|-----|-------|---------|
| 1 | 0.0s | 2.8s | jack_01_forward_calculating | "Update on the Doug situation." |
| 2 | 2.8s | 6.8s | jack_01_forward_calculating | "Very normal. Very ethical." |
| 3 | 6.8s | 11.5s | **MISSING** crm_monitor | "Email opened. Link clicked. Reply received." |
| 4 | 11.5s | 17.0s | jack_02_tie_fix_confident_smirk | "Either Doug is interested..." |
| 5 | 17.0s | 21.0s | jack_02_tie_fix_confident_smirk | "or Doug is tracking me back." |
| 6 | 21.0s | 28.5s | jack_02_tie_fix_confident_smirk | "Spiritually? The evidence is overwhelming." |
| 7 | 28.5s | 38.0s | jack_03_turning_to_monitor | "Quietly panicking in business clothes." |

**V1 fallback for beat 3:** Use `jack_01_forward_calculating` (same as beat 1/2). The missing CRM asset is logged in asset_manifest.json for generation later.

### Implementation steps

1. **Windows setup** — Install Node 20+, pnpm, FFmpeg (see section 7).
2. **Init project** — `pnpm init`, install remotion deps (see section 8).
3. **Config files** — Write `remotion.config.ts`, `tsconfig.json`, `src/config.ts` (30fps), `src/presets.ts` (Portrait-1080p at 30fps).
4. **Copy assets** — Copy 3 keyframe PNGs and MP3 into `public/images/` and `public/audio/`.
5. **Write `JackScene.tsx`** — `<Img>` fullscreen + Ken Burns pan/zoom via `interpolate()`. Scale 1.0→1.06 over beat duration; translate X/Y ±15px depending on beat.
6. **Write `JackCaption.tsx`** — Beat-driven text overlay. White text, black semi-transparent backing, centered in safe zone (x: 100–980, y: 220–1450, avoid bottom 300px).
7. **Write `doug-ep02/timing.ts`** — Import and type the 7-beat JSON array.
8. **Write `doug-ep02/Composition.tsx`** — `<Series>` of 7 `<Series.Sequence>` blocks, each containing `<JackScene>` + `<JackCaption>`. Add `<Audio src={staticFile("audio/doug_episode_02_voice_current.mp3")} />` at root.
9. **Write `Root.tsx`** — Register `DougEp02` composition.
10. **Dev preview** — `pnpm run dev` → open localhost:3000, review each beat.
11. **Render** — `pnpm exec remotion render DougEp02 --output renders/draft/doug_ep02_draft.mp4 --codec h264`.
12. **QC checklist** — Verify: 1080×1920, ~38s, audio synced, captions in safe zone, hard cuts on beat boundaries, no cloud dependencies.

---

## 11. Risks and Blockers

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Remotion license applies to company use | Medium | Confirm solo/personal use applies free tier before commercializing |
| FFmpeg not on Windows PATH after install | Low | `winget install FFmpeg` + restart terminal; fallback: manual download from ffmpeg.org |
| Jack keyframe images are large (~2MB each) | Low | Remotion handles large images; for render speed, pre-resize to 1080px width |
| Missing CRM asset (beat 3) | Low | V1 fallback: reuse jack_01 still. Does not block render. |
| pnpm-lock.yaml version drift | Low | Pin Remotion at `4.0.382` exactly; Remotion has strict version-matching requirements across `@remotion/*` packages |
| Ken Burns effect shows compression artifacts | Low | Use PNG instead of JPEG for `setVideoImageFormat` if quality is poor |
| Audio/caption sync drift | Low | Use `frame / fps` for current time in caption component (matches how the kickstart Caption.tsx works) |
| `@remotion/tailwind-v4` not included | None | Caption styled with inline styles only — Tailwind is optional |

---

## 12. Do This Next

**In order. Do not skip steps.**

1. **Confirm Windows setup:**
   ```powershell
   node --version   # must be 20+
   pnpm --version   # must exist
   ffmpeg -version  # must exist
   ```

2. **Say "build the V1 renderer"** — I will write all the source files (`src/`, `public/`, `package.json`, `remotion.config.ts`, `tsconfig.json`) using the architecture above.

3. **Run `pnpm install`** — First install after I write the files.

4. **Run `pnpm run dev`** — Preview in browser.

5. **Run `pnpm exec remotion render DougEp02 --output renders/draft/doug_ep02_draft.mp4`** — First render.

6. **Review the draft MP4** — Check timing, captions, audio sync.

7. **Iterate** — Adjust Ken Burns parameters, caption timing, safe-zone positioning.

8. **Final render to `renders/final/`.**

---

*Report generated 2026-05-19. Research repos in `./research/` — read-only, do not modify.*
