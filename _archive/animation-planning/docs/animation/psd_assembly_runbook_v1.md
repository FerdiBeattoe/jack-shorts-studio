# PSD Assembly Runbook v1

**Primary script:** `scripts/build-jack-character-animator-psd-v1.mjs`  
**Fallback script:** `scripts/assemble-jack-character-animator-v1.jsx` (Photoshop only)  
**Outputs:**
- `assets/puppet/jack_character_animator_v1.psd` — layered PSD with first-pass positioning
- `assets/puppet/jack_character_animator_v1_layout_preview.png` — flat composite for visual QC  
**Status:** Node builder operational — PSD and layout preview generated

---

## Overview

The PSD is assembled by a local Node.js script using [ag-psd](https://github.com/Agamnentzar/ag-psd) for PSD writing and [@napi-rs/canvas](https://github.com/nicolo-ribaudo/napi-rs) for PNG loading. No Adobe Photoshop is required for the main build path.

| Path | Tool required | Cost |
|------|--------------|------|
| **Primary (recommended)** | Node.js + ag-psd + @napi-rs/canvas | Free |
| Fallback | Adobe Photoshop CC 2022+ | Paid licence |

---

## Primary Workflow — Free Node.js Build

### Step 1 — Confirm assets are present

```
node scripts/validate-jack-puppet-pack.mjs
```

Must report `V1 READY`. If it reports `BLOCKED`, generate the missing assets first.

### Step 2 — Install dependencies (once)

```
pnpm add ag-psd @napi-rs/canvas
```

`@napi-rs/canvas` ships prebuilt Windows binaries — no C++ compilation required.

### Step 3 — Run the builder

```
node scripts/build-jack-character-animator-psd-v1.mjs
```

Runtime: 5–15 seconds. The script:
1. Reads all 44 V1-required PNGs from disk
2. Loads each PNG into a canvas via `@napi-rs/canvas`
3. Builds the full group hierarchy per `character_animator_layer_naming_v1.md`
4. **Applies a deterministic first-pass layout** from the `LAYOUT` map in the script — layers are no longer all at (0, 0)
5. Writes the layered PSD with `ag-psd`
6. Writes a flat composite PNG preview for visual QC

The script is idempotent — re-running overwrites both outputs. Source PNGs are never modified.

**Adjusting positions:** Edit the `LAYOUT` map (top-level constant in the script) and re-run. Each entry is `[left, top]` in pixels on the 1920×1920 canvas.

### Step 4 — Validate

```
node scripts/validate-jack-psd-assembly.mjs
```

Confirms: builder exists, dependencies installed, PNGs intact, PSD present and non-empty, layout preview present and non-empty.

### Step 5 — Review the layout preview

Open the flat preview PNG to quickly check automated positions before opening the full PSD:

```
assets/puppet/jack_character_animator_v1_layout_preview.png
```

The preview shows all default-visible layers composited on a dark background with faint centre guides. It is a **QC artefact only** — not production art. If positions look wrong, edit the `LAYOUT` map and re-run the builder.

### Step 6 — Inspect in Photopea (optional, for layer-name verification)

1. Go to **https://www.photopea.com**
2. File → Open → select `assets/puppet/jack_character_animator_v1.psd`
3. Open the **Layers panel** (Window → Layers)
4. Verify the group hierarchy matches the tree below
5. Make small position adjustments if the automated layout needs fine-tuning

---

## Expected PSD Output

| Property | Value |
|---------|-------|
| PSD path | `assets/puppet/jack_character_animator_v1.psd` |
| Preview path | `assets/puppet/jack_character_animator_v1_layout_preview.png` |
| Canvas size | 1920 × 1920 px |
| Colour mode | RGB / 8-bit |
| Layers imported | 35 (all V1-required assets) |
| Approximate PSD size | 25–30 MB |
| Layer positioning | First-pass automated layout (LAYOUT map in builder script) |

### First-Pass Layer Positions

| Layer / Group | left | top | Notes |
|--------------|------|-----|-------|
| Office Background | 0 | 420 | 1920×1080 image, centred vertically |
| Chair | 360 | 680 | 1200×1200, centred horizontally behind body |
| Torso + Tie | 448 | 750 | 1024×1024, centred at x=960 |
| Left Arm | 0 | 750 | 1024×1024, left edge of canvas |
| Right Arm | 896 | 750 | 1024×1024, right edge of canvas |
| Head Base | 448 | 150 | 1024×1024, centred at x=960 |
| Eyes (L/R) | 824 / 584 | 274 | 512×512, ±120px from centre |
| Pupils (L/R) | 824 / 584 | 274 | same as eyes |
| Eyebrows (L/R) | 333 | 35 | 1254×1254, centred on head centre |
| Mouth (all) | 704 | 494 | 512×512, centred at x=960 |

---

## PSD Layer Structure

```
[doc root]
├── Jack                               ← puppet root group
│   ├── Head
│   │   ├── Face
│   │   │   ├── Mouth
│   │   │   │   ├── Neutral  [VISIBLE] ← CA Auto Mouth default/silence
│   │   │   │   ├── Smile    [hidden]
│   │   │   │   ├── Smirk    [hidden]  ← trigger-only, NOT Auto Mouth
│   │   │   │   ├── Open     [hidden]
│   │   │   │   ├── Ee       [hidden]
│   │   │   │   ├── Oh       [hidden]
│   │   │   │   ├── Ooh      [hidden]
│   │   │   │   ├── M B P    [hidden]
│   │   │   │   ├── F V      [hidden]
│   │   │   │   ├── L        [hidden]
│   │   │   │   └── S        [hidden]
│   │   │   ├── Left Eye
│   │   │   │   ├── Left Upper Lid
│   │   │   │   │   └── Left Eye Open  [VISIBLE] ← CA blink warp
│   │   │   │   ├── Left Lower Lid     (empty — CA blink warp)
│   │   │   │   ├── Left Eye Half      [hidden]
│   │   │   │   ├── Left Eye Closed    [hidden]
│   │   │   │   └── Left Pupil         [VISIBLE] ← CA gaze warp
│   │   │   ├── Right Eye
│   │   │   │   ├── Right Upper Lid
│   │   │   │   │   └── Right Eye Open [VISIBLE]
│   │   │   │   ├── Right Lower Lid    (empty)
│   │   │   │   ├── Right Eye Half     [hidden]
│   │   │   │   ├── Right Eye Closed   [hidden]
│   │   │   │   └── Right Pupil        [VISIBLE]
│   │   │   ├── Left Eyebrow
│   │   │   │   ├── LB Neutral   [VISIBLE]
│   │   │   │   ├── LB Concerned [hidden]
│   │   │   │   ├── LB Thinking  [hidden]
│   │   │   │   └── LB Smug      [hidden]
│   │   │   └── Right Eyebrow
│   │   │       ├── RB Neutral   [VISIBLE]
│   │   │       ├── RB Concerned [hidden]
│   │   │       ├── RB Thinking  [hidden]
│   │   │       └── RB Smug      [hidden]
│   │   └── Head Base              [VISIBLE]
│   └── Body
│       ├── Right Arm
│       │   ├── Arm Resting    [VISIBLE group]
│       │   │   └── Right Arm Resting
│       │   └── Arm Tie Fix    [hidden group] ← trigger swap
│       │       └── Right Arm Raised
│       ├── Left Arm
│       │   └── Left Arm Resting
│       ├── Tie
│       │   └── Tie Straight
│       └── Torso
└── Environment                        ← NOT part of the Jack puppet
    ├── Chair
    └── Office Background
```

---

## What Not to Edit Manually

| What | Why |
|------|-----|
| Group names (`Jack`, `Head`, `Face`, `Mouth`, `Left Eye`, etc.) | Character Animator reads these exact strings for auto-tagging. Renaming breaks CA behaviour detection. |
| Mouth sublayer names (`Neutral`, `Open`, `Ee`, `Oh`, `Ooh`, `M B P`, `F V`, `L`, `S`, `Smile`) | CA's Auto Mouth maps phonemes to these exact strings. A typo means that phoneme falls back to Neutral. |
| Lid group names (`Left Upper Lid`, `Left Lower Lid`, `Right Upper Lid`, `Right Lower Lid`) | CA uses these exact names for blink warp handles. |
| Eyebrow sublayer names (`LB Neutral`, `LB Concerned`, etc.) | Referenced in the CA Triggers panel. |

**Safe to edit after assembly:**
- Layer positions (x/y on canvas) — manual rigging step
- Layer opacity
- Adding optional layers when generated (e.g. `jack_nose.png`)

---

## After Reviewing the Preview and Photopea

The V1 PSD has correct names, structure, and automated first-pass positions. Most layers should be in approximately the right region of the canvas. Before importing into Character Animator, fine-tune any layers that look misaligned:

**If a layer position is wrong:**
1. Edit the `LAYOUT` map in `scripts/build-jack-character-animator-psd-v1.mjs`
2. Re-run the builder — both PSD and preview regenerate
3. This is the preferred workflow; keep position changes in source control

**If only minor tweaks are needed (1–2 layers):**
1. In Photopea, find the layer in the Layers panel
2. Use the Move tool (V) to drag it to the correct position
3. File → Save as PSD (overwrite the existing file)
4. Note: manual changes in Photopea will be overwritten next time the builder runs

**Typical fine-tuning needed on first pass:**
- Eyebrow images (1254×1254) may extend slightly off the top edge — this is expected; fine-tune `LAYOUT.browLeft/browRight` top value
- Mouth position may need vertical adjustment to align with the muzzle region
- Eye positions may need slight left/right offset to match exact eye socket location

---

## Importing into Adobe Character Animator

**This step requires Adobe Character Animator (CC 2022+).**

> ⚠️  The rig correctness has NOT been verified in Character Animator. This runbook documents the intended workflow. Manual testing is required before any claim of CA compatibility.

### Steps

1. In Character Animator: **File → New → Puppet from Photoshop File**
2. Select `assets/puppet/jack_character_animator_v1.psd`
3. Run: **Character → Rigging → Auto-tag puppet**
4. Review auto-detected behaviours:
   - `Mouth` → Auto Mouth (lip sync)
   - `Left Upper Lid` / `Right Upper Lid` → Blink warp
   - `Left Pupil` / `Right Pupil` → Eye direction warp
   - `Left Eyebrow` / `Right Eyebrow` → Brow movement
   - `Head` → Face tracking origin
   - `Body` → Body tracking
5. Add warp mesh handles to: lid groups, pupils, eyebrow layers
6. Configure Triggers panel per `docs/animation/jack_expression_system_v1.md`
7. Test lip sync: drag `public/audio/doug_episode_02_voice_current.mp3` into a Take

---

## Fallback: Photoshop JSX

The original Photoshop ExtendScript is kept at `scripts/assemble-jack-character-animator-v1.jsx`. Use it if you prefer Photoshop-based assembly or if the Node builder produces a PSD that Photoshop cannot open.

To run the JSX:
1. Open Adobe Photoshop
2. File → Scripts → Browse
3. Select `scripts/assemble-jack-character-animator-v1.jsx`
4. Click Open

---

## If the Node Builder Fails

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot find module 'ag-psd'` | ag-psd not installed | `pnpm add ag-psd @napi-rs/canvas` |
| `Cannot find module '@napi-rs/canvas'` | canvas not installed | `pnpm add @napi-rs/canvas` |
| `PREFLIGHT FAILED — X V1-required PNGs missing` | Source assets missing | `node scripts/validate-jack-puppet-pack.mjs` |
| `Canvas not initialized` | initializeCanvas not called | Check import at top of build script |
| PSD opens blank in Photopea | PNG transparency not preserved | Check source PNGs have alpha channels |
| CA doesn't detect Auto Mouth | Mouth sublayer name typo | Verify exact names — case sensitive |
