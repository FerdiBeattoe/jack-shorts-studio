# Topwear r1 — assessment notes

**Status:** STAGING ONLY. No promotion. Stop after notes.

## Artifacts

- `jack_jacket_r1.png` — 269×390 RGBA, **byte-identical** to CoPainter `layer_71.png` (sha verified)
- `jack_shirt_tie_r1.png` — 239×311 RGBA, **byte-identical** to CoPainter `layer_75.png` (sha verified)
- `jack_topwear_r1_full_canvas_test.png` — both placed on See-through 768×768 canvas at derived torso anchor (shirt+tie BEHIND jacket)
- `jack_topwear_r1_visual_qc.png` — 7-panel QC (isolated + recomposed + over-See-through + full-body + collar zoom + before/after)
- `jack_topwear_r1_composite_qc.png` — full-body composite (See-through layers + CoPainter topwear + promoted belt)
- `topwear_r1_manifest.json` — anchors, scales, SHA, alpha stats, do-not list
- Script: `tools/puppet/stage_topwear_r1.py`

## TL;DR

**✅ Topwear split passes QC and beats See-through merged on the front silhouette.** The jacket and shirt+tie compose cleanly with the promoted belt — collar V is visible, tie goes under the jacket, belt sits at the waist. Style preserved. CoPainter max-254 alpha quirk **does not manifest visually**.

**⚠️ One caveat:** the new jacket is slightly narrower than the See-through `handwear` layer behind it, so the See-through sleeves poke out on both sides as thin black strips. This is a **downstream rig issue**, not a defect in the topwear split itself — see "Sleeve overhang" section.

**Recommend promotion** in a separate task **after** deciding the sleeve strategy.

## Anchor derivation (no origin metadata in CoPainter ZIP)

| Item | Value |
|---|---|
| See-through canvas | 768 × 768 |
| See-through topwear bbox (reference) | (314, 152, 505, 423) |
| Body centerline x | 410 |
| Topwear top y | 152 |
| Scale (CoPainter → See-through) | **0.7100** (basis: CoPainter jacket 269 ↔ See-through topwear 191) |
| Shirt+tie uses same scale (torso-consistent) | 0.7100 |
| Scaled jacket size on canvas | 191 × 276 |
| Scaled shirt+tie size on canvas | 169 × 220 |
| Jacket top-left | (314, 152) |
| Shirt+tie top-left | (325, 164) — 12 px below jacket top so collar V is visible |
| Draw order back→front | shirt+tie → jacket |

Same `0.71` scale used for the locked belt — torso assets are consistent at this scale.

## QC against criteria

| Criterion | Verdict | Notes |
|---|---|---|
| Jacket fits torso/head proportions? | ✅ Yes | Scaled jacket is 191×276, matches See-through topwear width (191) and is slightly taller (allows collar+tie visibility) |
| Shirt+tie aligns under head + with promoted belt? | ✅ Yes | Collar V visible under chin; tie passes vertically behind jacket; belt at y=394 sits naturally at the bottom of the jacket |
| Preserves Jack's locked design? | ✅ Yes | No redraw — pixel-identical to CoPainter source; clean black jacket, white shirt, black tie |
| Better than See-through merged topwear? | ✅ Yes (front silhouette) | Cleaner collar definition; separable layers allow independent shirt/jacket/belt rigging |
| Edges/alpha acceptable despite max=254 quirk? | ✅ Yes | No halo, no fringe, anti-aliased edges blend naturally with surrounding layers |
| Style drift? | ❌ None | CoPainter preserves linework and colour palette identical to Jack's design |
| Promotion-ready? | ⚠️ Pending sleeve strategy | See "Sleeve overhang" below |
| Krita/Photoshop cleanup needed? | ❌ Not for jacket/shirt assets themselves | The sleeve overhang is a compositing decision, not a pixel fix |

## Sleeve overhang (only issue worth noting)

In panel 5 (full-body) and panel 7 (before/after), thin black strips show on the sides of Jack's torso. These are the **See-through `handwear` layer** (sleeve geometry behind the body) showing past the edge of the new CoPainter jacket.

Cause: See-through's `topwear` bbox is 191 px wide; See-through's `handwear` bbox is 225 px wide. When the CoPainter jacket (191 px scaled, centred on body) replaces See-through topwear, the wider handwear (sleeves) still extends 17 px to each side, creating the strips.

**Three options to resolve downstream — NOT a topwear-staging concern:**
1. **Drop See-through handwear when CoPainter jacket is in play** — simplest, but may lose arm geometry behind sleeves.
2. **Use CoPainter arms (`layer_76`, `layer_78`)** — but those are extended-pose, wrong anatomy.
3. **Hand-cut See-through handwear in Krita** to remove the strips outside the jacket silhouette.

Decision deferred to the promotion task. Staging is honest about the issue.

## Edge alpha sanity (CoPainter max-254 quirk)

| Asset | a_max | a>0 | a≥200 |
|---|---|---|---|
| jacket | 254 | 80.6% | 76.5% |
| shirt+tie | 254 | 72.0% | 68.9% |

Both never reach alpha=255 (CoPainter quirk). Composite QC shows **no visible halo or fringe** — the anti-aliased edges blend naturally with adjacent layers. Same behavior as the locked belt, accepted via visual QC override.

## Should jacket and shirt+tie be promoted later?

**Yes — in a separate task that also addresses the sleeve overhang.** Concrete plan:

1. Decide sleeve strategy (option 1/2/3 above).
2. Copy `jack_jacket_r1.png` → `assets/puppet/layers/topwear/jack_jacket.png` (byte-identical).
3. Copy `jack_shirt_tie_r1.png` → `assets/puppet/layers/topwear/jack_shirt_tie.png` (byte-identical).
4. Write production manifest documenting anchors (same as staging manifest), back-to-front draw order, and the sleeve decision.
5. Update the cloud audit report's downstream-promotions table.

## Comparison to See-through

See-through provides a single merged `topwear` layer (jacket+shirt+tie baked together) at 191×271. **CoPainter is the only source we have for split jacket vs shirt+tie**, with the additional benefit of a separable tie reconstruction (visible in the shirt+tie layer behind the open jacket V). So this is a clean "CoPainter supplements See-through" win — the merged See-through topwear can be deprecated for the front pose once the split is promoted.

## What this QC does NOT prove

- That the puppet rig actually uses the (768×768) See-through canvas as its working canvas — if production rig is at a different canvas size, the topleft coords need transformation.
- That the side/3-quarter poses will benefit from the same split — CoPainter input was the front pose only.
- That `layer_71` and `layer_75` will remain stable across CoPainter re-exports — SHA recorded for drift detection.

## Decision

**No promotion in this task.** Topwear split is staging-ready. Recommend: separate explicit promotion task that (a) decides the sleeve overhang strategy, and (b) copies the two PNGs byte-identically into a new `assets/puppet/layers/topwear/` folder with a production manifest.
