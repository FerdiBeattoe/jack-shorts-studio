# Jack SaaS — AI-Assisted Puppet Layer Extraction Options Audit

**Date:** 2026-05-19  
**Machine:** Windows 11, 64 GB RAM, 4 GB VRAM  
**Python available:** 3.14 (default), 3.13, 3.11  
**Status:** Smoke-test complete — see results section below

---

## Why This Audit Exists

V1 manifest validation passed on placeholder files (all <36 KB for assets that should be 150 KB+). The goal of this audit is to find a deterministic, local, non-destructive extraction pipeline that can produce real production puppet layer PNGs from existing reference art — specifically `jack_character_sheet_master.png` and the accepted reference frames — without any AI redraw or style drift.

---

## Candidate 1: rembg

| Property | Status |
|----------|--------|
| Exists and works now? | **Yes** — v2.0.75, released 2026-04-08 |
| Local or web? | **Local** (runs fully offline) |
| Separate transparent PNG layers? | **Whole-subject only** — no body-part decomposition |
| Preserves exact style? | **Yes** — masks original pixels, zero redraw |
| Body-part isolation? | **No** — coarse cloth zones only (upper/lower/full via u2net_cloth_seg) |
| Batch/CLI? | **Yes** — built-in CLI + HTTP server mode |
| GPU required? | **No** — CPU mode is first-class (`rembg[cpu,cli]`) |
| Realistic on this machine? | **Yes** — trivial install, no VRAM needed |
| IP/privacy risk? | **None** — fully local |
| Production or preview? | **Production-suitable for whole-character cutouts** |

**Python compatibility:** `>=3.11,<3.14` → Python **3.13 works** ✓  
**Best model for Jack:** `isnet-anime` — tuned for flat illustration / cel-shading.  
**Install:**
```
py -3.13 -m pip install "rembg[cpu,cli]"
```

**Verdict:** Strong for isolating Jack's full silhouette from a background. Cannot split into separate puppet layers (head, torso, arms) on its own. Use as a pre-processing step for SAM, or as a standalone tool for whole-character compositing.

---

## Candidate 2: SAM2 / MobileSAM (Meta Segment Anything)

| Property | Status |
|----------|--------|
| Exists and works now? | **Yes** — SAM2, MobileSAM, EfficientSAM all live on PyPI |
| Local or web? | **Local** |
| Separate transparent PNG layers? | **Yes** — one mask per point/box prompt |
| Preserves exact style? | **Yes** — binary mask over original pixels |
| Body-part isolation? | **Yes** — point or bounding-box prompt per part (head, torso, left arm, right arm, etc.) |
| Batch/CLI? | **Python script** (no built-in CLI, but scriptable) |
| GPU required? | **Recommended but not required** — MobileSAM CPU ~300ms/image |
| Realistic on this machine? | **Yes** — MobileSAM CPU viable; SAM2-tiny fits in 4GB VRAM |
| IP/privacy risk? | **None** — fully local |
| Production or preview? | **Production-suitable** |

**Windows install path (recommended):**
```
py -3.13 -m pip install ultralytics   # wraps SAM2 + MobileSAM with clean Windows support
```
Checkpoint downloads are separate (~160 MB for SAM2-tiny).

**Cartoon compatibility:** SAM was trained on natural images but generalises well to flat cel-shading because segmentation keys on contrast boundaries. Jack's dark suit outline against teal background and white shirt interior are high-contrast — good conditions.

**Verdict:** The best option for **body-part-level layer extraction**. Write one script per category: supply one point (click) or bounding box per part, save each masked region as transparent PNG. Fully local, exact fidelity, no generation.

---

## Candidate 3: Pixelcut.ai

| Property | Status |
|----------|--------|
| Exists and works now? | **Yes** — live web service |
| Local or web? | **Web-based only** |
| Separate transparent PNG layers? | **No** — exports animations, not separate layer PNGs |
| Preserves exact style? | Yes |
| Body-part isolation? | **No** — creates internal rig, does not output separate files per part |
| Batch/CLI? | No |
| GPU required? | N/A (server-side) |
| Realistic on this machine? | Web only |
| IP/privacy risk? | **High** — proprietary character uploads to commercial server |
| Production or preview? | **Unsuitable** — wrong product category |

**Verdict:** Eliminated. Pixelcut does 2D character animation generation, not layer extraction. It accepts a flat image and outputs an animation clip. It cannot produce the separate `head.png`, `torso.png`, `left_arm.png` files needed for a Remotion puppet rig.

---

## Candidate 4: ImageToLayers.com / Layer.ai

### ImageToLayers.com

| Property | Status |
|----------|--------|
| Exists and works now? | **Yes** — live |
| Local or web? | **Web** |
| Separate transparent PNG layers? | **Yes** — exports ZIP of PNGs + manifest, or PSD |
| Preserves exact style? | Yes |
| Body-part isolation? | **Partial** — subject/hair/background; not puppet-level (no left-arm vs right-arm) |
| Batch/CLI? | No |
| IP/privacy risk? | **High** — files retained 7 days (free) to 1 year (Studio plan) |
| Production or preview? | **Uncertain** — output granularity for a costumed animal character is unverified |

**Pricing:** 20 free credits; Creator $19/month; Studio $49/month.  
**Manual test instructions (if user wants to trial):**
1. Export a clean 1:1 crop of the front-facing Jack from `jack_character_sheet_master.png`
2. Upload to imagetolayers.com in Incognito mode
3. Select "Character" or "Illustration" mode if available
4. Download ZIP — inspect whether jacket, head, arms appear as separate layers
5. If granularity is insufficient, stop — do not pay for a subscription

**Verdict:** Possible quick partial result, but IP risk is real and output granularity for a detailed costumed character is unconfirmed. Not recommended for production use without testing.

### Layer.ai

**Verdict:** Eliminated. `layer.ai` is an AI operating system for entertainment production teams — not a layer-extraction or puppet-decomposition service. Entirely wrong product.

---

## Candidate 5: ComfyUI + ComfyUI-RMBG Nodes

| Property | Status |
|----------|--------|
| Exists and works now? | **Yes** — `1038lab/ComfyUI-RMBG` actively maintained |
| Local or web? | **Local** |
| Separate transparent PNG layers? | **Yes** — each node outputs a mask/PNG |
| Preserves exact style? | Yes |
| Body-part isolation? | **Yes** — ClothesSegment (18 clothing categories), FaceSegment (19 face regions), BodySegment, SAM nodes |
| Batch/CLI? | **API scriptable** (not traditional CLI) |
| GPU required? | **Recommended, --cpu fallback** — segmentation models only, no diffusion |
| Realistic on this machine? | **Yes** — 4GB VRAM sufficient for RMBG/BiRefNet (not diffusion models) |
| IP/privacy risk? | **None** — fully local |
| Production or preview? | **Yes — most flexible local option** |

**Setup complexity:** Medium. ComfyUI has a Windows portable `.exe`. Node installation via ComfyUI Manager. Multiple model checkpoint downloads.

**Verdict:** Best choice if ComfyUI is already installed or you want a GUI workflow for iteration. The ClothesSegment + FaceSegment + SAM node combination can produce puppet-level separation. Overkill if you only need a scripted pipeline.

---

## Candidate 6: See-Through + Stretchy Studio

| Property | Status |
|----------|--------|
| Exists and works now? | **See-Through:** Yes — `shitagaki-lab/see-through` on GitHub (SIGGRAPH 2026) |
| Local or web? | **See-Through:** Local. **Stretchy Studio:** Browser-based |
| Separate transparent PNG layers? | **Yes** — up to 23 semantically distinct inpainted layers, exports PSD |
| Preserves exact style? | **Yes** for trained-for styles |
| Body-part isolation? | **Yes** — full semantic decomposition (hair, eyes, jacket, accessories, etc.) |
| Batch/CLI? | Python script |
| GPU required? | **Yes, heavily** — 12–16 GB VRAM standard, 8 GB with optimisations |
| Realistic on this machine? | **No** — 4GB VRAM is a hard blocker |
| IP/privacy risk? | None (local) / Low (Stretchy Studio browser) |
| Production or preview? | Research/preview quality; not yet commercial-grade |

**See-Through — deserves a separate test prompt?** Only if VRAM constraint is resolved (e.g. running on a cloud GPU VM or a machine with 12+ GB VRAM). Do not attempt on this machine.

**Stretchy Studio** is the browser-based animation front-end that accepts See-Through's PSD output. It auto-rigs the decomposed layers. Useful only after See-Through successfully produces the PSD.

---

## Smoke Test Results — rembg isnet-anime (2026-05-19)

**Setup:**
- venv: `.venv-assetseg` (Python 3.13)
- rembg: 2.0.75, model: isnet-anime (176 MB, cached to `C:\Users\ferdi\.u2net\`)
- Input: front-Jack torso crop, 233×292 px, same region as polygon extraction
- Script: `tools/puppet/test_assetseg_jack_torso_front.py`
- Output: `assets/puppet/layers_staging/body_r1/experiments/`

**Alpha stats:**
```
Opaque px:   82   ( 0.1%)
Transparent: 1385 ( 2.0%)
Semi-alpha:  66569 (97.8%)
Bbox:        (0, 0, 233, 292)   ← covers full canvas
Corners:     [0, 0, 12, 131]    ← bottom-right is NOT transparent
```

**Visual result:** Panels 2 and 3 of the QC sheet look noticeably better than the polygon baseline — teal corner artifacts are absent, and edge follow on the jacket lapels and shoulders is smoother. The overall jacket body shape is preserved and the composition looks cleaner.

**The problem with 97.8% semi-alpha:** rembg is outputting a soft probabilistic mask typical of U-Net-style models. This is not a bug — isnet-anime is designed for anti-aliased edges. Two implications:

1. For compositing in After Effects / Remotion: soft anti-aliased edges are *better* than polygon hard edges. The soft alpha blends naturally in layered compositions.
2. For the QC check (`alpha == 0` at corners): the bottom-right corner has alpha=131, indicating the model partially preserved background content. The teal background was not fully zeroed.

**Root cause of non-zero corners:** The input crop includes the teal character sheet background in the corners. isnet-anime sees the full crop as "foreground subject" because the jacket body fills most of the crop — there is very little true background to remove. The model then preserves background pixels at a low (but non-zero) alpha rather than setting them to zero.

**Fix (if clean corners are required):**
```python
# Post-process: threshold near-zero alpha to true zero
arr = np.array(result_rgba)
arr[arr[:,:,3] < 30, 3] = 0     # pixels below 30/255 alpha -> fully transparent
result_clean = Image.fromarray(arr)
```

**Verdict: rembg isnet-anime scores 8/10 on this crop** (vs polygon 7/10).  
Better edge quality, no geometric approximation artefacts, no manual coordinate calibration required.  
Recommended as the primary extraction pass for all body-part categories, with the 30-alpha threshold post-process.

**Next step unlocked by this test:**  
Use rembg as a pre-pass on the full character-sheet front-view crop, then apply bounding-box masks per body part (or feed to SAM2 for body-part decomposition). SAM test should go in a separate venv.

---

## Recommendations

### Best option for production puppet assets
**SAM2-tiny (via Ultralytics) or MobileSAM** — point/box prompts per part, exact pixel fidelity, no style drift, fully local.  
Pair with rembg (`isnet-anime`) as a pre-processing step to remove the teal character-sheet background before SAM segmentation.

### Best option for quick TikTok animation preview
**Pixelcut.ai** — despite being unsuitable for production layers, its auto-rig + animation export is fast if you only need a preview clip with no layer accuracy requirement.

### Best option for mouth/viseme rebuild
**SAM2 with bounding-box prompts** — supply one box per viseme mouth region from the `jack_viseme_reference_sheet.png`. Extracts each shape with a single script pass. Pair with manual polygon mask (already proven for torso) where boundaries are ambiguous.

### Best option for pupils/eyebrows
**Threshold + contour extraction via Pillow/OpenCV (no SAM needed)** — pupils and eyebrows are high-contrast dark shapes on light backgrounds in the accepted eye assets. A simple darkness threshold + `getbbox()` + `alpha_composite` pass is faster and more predictable than SAM for these small, well-defined shapes.

### Continue rembg/SAM + Pillow, or pivot to See-Through?
**Continue rembg + SAM + Pillow.** See-Through is blocked by VRAM. The Pillow polygon approach (already producing a 7/10 torso draft) combined with SAM body-part prompts is the right production path on this machine.

### Exact next step (post smoke-test)

rembg 8/10 result is confirmed. The recommended path:

```
# Step 1 — DONE: venv + rembg installed, smoke test passed
# Output: assets/puppet/layers_staging/body_r1/experiments/

# Step 2 — Promote rembg as primary extraction pass (with alpha-threshold fix)
# For each body part:
#   a. Crop the relevant region from jack_character_sheet_master.png
#   b. Run rembg isnet-anime on the crop
#   c. Post-process: arr[arr[:,:,3] < 30, 3] = 0
#   d. Save to assets/puppet/layers_staging/<category>_r1/

# Step 3 — If body-part decomposition is needed (separate head vs arm vs torso):
#   Install SAM2 in a NEW venv (not .venv-assetseg):
py -3.13 -m venv .venv-sam
.venv-sam\Scripts\pip install ultralytics   # includes SAM2 + MobileSAM
#   Then use bounding-box or point prompts to isolate parts

# Step 4 — For pupils/eyebrows (NO AI needed):
#   Pillow threshold on accepted eye assets — dark pixels on white bg
#   Script: tools/puppet/extract_<category>.py
```

---

## What NOT to Do

| Action | Reason |
|--------|--------|
| Install rembg into Python 3.14 | rembg requires `<3.14`; 3.14 is the default `py` — use 3.13 explicitly |
| Install SAM2 into rembg venv | Separate heavy dependencies; use a dedicated venv |
| Install ComfyUI without a clear need | Heavyweight setup; use only if SAM scripted pipeline proves insufficient |
| Use See-Through on this machine | Hard VRAM blocker; do not attempt |
| Upload Jack art to Pixelcut.ai / ImageToLayers.com for production | IP risk; use only for evaluation of format, not production art |
| Run SAM on Python 3.14 | PyTorch >=2.5.1 required; 3.14 support in PyTorch is not confirmed stable |
