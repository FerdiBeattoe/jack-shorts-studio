# Full-body integration QC r1 — assessment notes

**Status:** QC ONLY. No promotion. No production writes. No PSD assembly.

## Artifacts

- `jack_full_body_locked_stack_qc.png` — 3 full-body composites (no-mouth, neutral, slight_smirk) at 768×768 canvas
- `jack_full_body_locked_stack_zoom_qc.png` — face/waist/left-cuff/right-cuff zooms at 3× (with both neutral and smirk for face)
- `jack_full_body_layer_order_test.png` — 15-panel cumulative back-to-front stack with PROD/ST source tags
- `full_body_integration_qc_r1_manifest.json` — anchors, layer order, asset inventory
- Script: `tools/puppet/qc_full_body_integration_r1.py`

## TL;DR

**Jack reads as the locked design overall**, but the integration exposes **three real issues** that should be addressed before PSD assembly:

1. **Double-hands at the cuffs.** See-through `handwear` (kept per Option B) already includes paws at the wrist openings. Production hands then composite on top of those — visible in layer-order panel #10 (handwear adds full arms+paws) and panel #15 (production hands added). The composite looks acceptable because production hands cover the handwear paws, but it's a redundant render and may cause subtle misalignment at high zoom.
2. **Mouth is too small to read at native canvas scale.** The mouth scale factor (0.183) was derived from See-through face width. At full 768×768 render the mouth artwork shrinks to ~27 px wide and reads as a faint speck — visible in zoom but invisible in the full-body view. The mouth_r2 QC validated readability at 3× zoom; at 1× it disappears.
3. **Sleeve overhang IS visible** in full-body view, contradicting the earlier sleeve_strategy_qc conclusion. The black handwear strips poke past the jacket on both sides. The earlier QC's larger zoom hid this; at full canvas the strips read as artifacts more than as shoulder bulk.

**Recommendation: do NOT start PSD assembly yet.** One more sub-task should re-derive a clean arm/sleeve solution that (a) eliminates the double-hands and (b) reconciles the sleeve overhang against the actual render scale.

## Layer order applied (per topwear Option B + mouth/belt/hand manifests)

| # | Layer | Source |
|---|---|---|
| 1 | back hair | See-through |
| 2 | ears | See-through |
| 3 | face | See-through |
| 4 | eyebrow | See-through |
| 5 | eyewhite | See-through |
| 6 | irides | See-through |
| 7 | mouth | **PROD** |
| 8 | legwear | See-through |
| 9 | footwear | See-through |
| 10 | handwear | See-through (unmodified per Option B) |
| 11 | shirt+tie | **PROD** |
| 12 | jacket | **PROD** |
| 13 | belt | **PROD** |
| 14 | hand R | **PROD** |
| 15 | hand L | **PROD** |

## Per-criterion assessment

### Does Jack still look like the locked character design?
**Mostly yes.** Head + jacket + shirt + tie + pants + shoes + belt all match. Style not regressed. The mouth doesn't visibly contribute at this scale (issue #2) but isn't wrong, just inaudible.

### Do promoted hands fit with promoted topwear?
**Visually yes, but logically there's a double-hand collision.** Production hands sit cleanly at the cuff anchors and cover the See-through handwear paws. But the handwear paws are still rendered underneath — wasted pixels + risk of edge misalignment if the production hand and the handwear paw don't share identical silhouettes at zoom.

### Does promoted belt align with shirt/tie and trousers?
**✅ Yes.** Belt sits cleanly at y≈394, buckle centered, jacket bottom + pants top hidden behind belt — same as the belt promotion composite QC.

### Does promoted mouth sit naturally on the face?
**Position correct, scale too small.** The mouth artwork (warm dark brown lineart on transparent) is rendered at the right *spot* (snout/chin transition) but at See-through face scale it's ~27 px wide — barely perceptible at full canvas. If the final render canvas is larger than See-through's 768×768, the mouth will scale up proportionally and be readable. If the final render IS at 768, the mouth needs re-scaling for visibility.

### Visible seams, halos, black strips, scale jumps?
- **Seams:** none at the belt / collar / cuff boundaries.
- **Halos:** none (CoPainter max-254 alpha quirk continues to be visually invisible).
- **Black strips:** **YES, still visible** as sleeve overhang on both sides of the torso (See-through handwear extending past the CoPainter jacket). The sleeve_strategy_qc Option B verdict claimed these "read as shoulder bulk" — at full canvas without zoom, they read more like artifacts.
- **Scale jumps:** none between PROD assets. Head looks slightly small for the body, but that's See-through baseline geometry, not a PROD asset issue.

### Which remaining categories should be promoted next?
**Best next single category: head.** Specifically, the head/face complex (back hair, ears, face) from a higher-quality source than See-through. The current See-through head is small, geometrically simple, and is the main reason Jack's facial features (eyes, mouth) don't read at canvas scale. CoPainter's `layer_01` (253×284 full head) is a candidate — staged separately, anchor-aligned, then promoted.

After head: **arms/sleeves** as a unified solution to issues #1 and #3 above. This is NOT just "promote handwear" — it's "decide the arm rig" (use the handwear arm minus its baked paws, OR replace with a clean source).

### Which categories are still risky?
- **Arms/sleeves**: handwear includes paws that conflict with promoted hands. Needs handling.
- **Eyes**: currently See-through baseline; works at static QC but if the rig needs blink, the eyes_blink_r1 was rejected for production blink/closed use — need a new blink source.
- **Mouth at small render scale**: only matters if final canvas is ≤ 768×768.
- **Side / 3-quarter poses**: no CoPainter or See-through source for non-front poses. Not in scope for V1 front-only rig, but flagged.

### Photoshop/Krita cleanup required anywhere?
**Yes — one targeted pass:** crop the See-through `handwear` PNG to remove the baked paws at the wrist (so it provides arms/sleeves only, leaving the production hands as the sole paw source). This is a deterministic Pillow mask if the paws can be isolated by colour/region — Krita not strictly required.

### Should PSD assembly begin yet?
**No.** Two blockers:
- Double-hands (issue #1) must be resolved.
- Sleeve overhang (issue #3) needs a second look at render-scale realism.

Mouth scale (issue #2) is render-canvas-dependent and not a strict blocker.

## Anchors used (reference)

| Asset | Anchor / TL on canvas | Scaled size |
|---|---|---|
| jacket | (314, 152) | 191×276 |
| shirt+tie | (325, 164) | 169×220 |
| belt | (347, 379) | 123×31 |
| mouth (centroid → (405, 142)) | TL (359, 93) | 94×94 (canvas), artwork ~27 px wide |
| hand R | (≈294, ≈386) | ~43×67 |
| hand L | (≈482, ≈386) | ~43×67 |

All anchors pulled from the production manifests (locked); no fresh derivation in this QC.

## Decision

**No promotion. No PSD assembly.** Next single-category sub-task should be:

1. **`arms_r1` staging** — crop See-through `handwear` to keep arms/sleeves only, drop the baked paws. Compare to the locked promoted hands; verify no overlap, no gap. Document anchor + crop mask deterministically.

Once arms_r1 passes, re-run this full-body integration QC. Only then consider PSD assembly.
