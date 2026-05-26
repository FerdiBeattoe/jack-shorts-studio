# Belt r1 — assessment notes

**Status:** STAGING ONLY. No promotion. Stop after notes.

## Artifacts

- `jack_belt_r1.png` — bbox-cropped RGBA (174×44), **byte-identical** to source `layer_77.png`
- `jack_belt_r1_full_canvas_test.png` — belt placed on See-through 768×768 canvas at derived waist anchor
- `jack_belt_r1_visual_qc.png` — 5-panel QC (zoom + topwear + legwear + full body + before/after + notes)
- `jack_belt_r1_composite_qc.png` — full-body composite (See-through layers + belt)
- `belt_r1_manifest.json` — source SHA, scale, anchor, alpha stats, do-not list
- Script: `tools/puppet/stage_belt_r1.py`

## TL;DR

**✅ Belt fits Jack cleanly.** The full-body composite reads as a coherent character — belt sits at the waist, buckle centers under the tie, scale matches See-through. **Recommend promotion** in a separate task. **No Krita cleanup required.**

## Anchor derivation (no origin metadata in CoPainter ZIP)

| Item | Value |
|---|---|
| See-through canvas | 768 × 768 |
| Topwear bbox (jacket bottom = y=423) | (314, 152, 505, 423) |
| Legwear bbox (pants top = y=364) | (310, 364, 504, 641) |
| Topwear / legwear overlap (waist band) | y = 364–423 |
| Waist centerline x (body mid) | **408** |
| Waist centerline y (overlap midpoint) | **394** |
| Belt scale (CoPainter → See-through) | **0.7100** (basis: CoPainter jacket 269 px ↔ See-through topwear 191 px) |
| Belt size on See-through canvas | 123 × 31 |
| Belt top-left on See-through canvas | (347, 379) |

## QC against criteria

| Criterion | Verdict | Notes |
|---|---|---|
| Visually fits Jack's waist? | ✅ Yes | Composite reads as a coherent character; belt sits in the topwear/legwear seam |
| Buckle aligned with shirt/tie centerline? | ✅ Yes | Buckle lands at x ≈ 408, directly under tie centre |
| Scale correct? | ✅ Yes | 0.71 scale derived from jacket-width ratio; result looks neither narrow nor stretched |
| Style match (CoPainter ↔ See-through ↔ character sheet)? | ✅ Yes | Belt linework + buckle silhouette match the character sheet's belt; no stylistic clash with See-through's jacket/pants |
| Edge alpha acceptable despite max ≈ 254? | ✅ Yes | Composite shows no visible halo or seam at the belt edges. Anti-aliased edges blend with topwear/legwear naturally. The "no alpha=255" CoPainter quirk does NOT manifest visually here. |

## Specific assessments

- **Belt scale:** 0.71 ratio from CoPainter jacket-width → See-through topwear-width is the cleanest available scaling reference. The result is visually correct — belt spans roughly the body width, narrower than the jacket bottom, wider than the pants top, which is what the character-sheet belt shows.
- **Vertical position:** y=394 (overlap midpoint) puts the belt slightly above the geometric waist but matches where the character sheet's belt sits (just below the jacket button line). Looks right.
- **Buckle centring:** the buckle in `layer_77.png` is at x ≈ 92 of 174 (53% from left). When centred on canvas x=408, the buckle lands at x ≈ 408 + (92 - 87) ≈ 413 — within 5 px of the body centerline. Visually centred.
- **Alpha quality:** despite the max-≈254 CoPainter quirk, the belt composites cleanly. The semi-transparent rim blends with the topwear/legwear behind, which is actually the correct behaviour for anti-aliased linework. No halo, no white fringe.
- **Style consistency:** belt is a flat black band with a silver-toned rectangular buckle — matches the character-sheet belt exactly. Not anime, not realistic-photo, just the right cartoon flatness.

## Krita cleanup needed?

**No.** The bbox crop is byte-identical to the CoPainter source (sha256 verified), pixel content is preserved, and the composite passes visual QC at 600 px render. If a future render targets a much higher resolution (e.g., 2K+ poster output), a thin manual anti-alias polish might marginally improve the buckle edges — but that's a polish-pass, not a blocker.

## Should this belt be promoted later?

**Yes.** Concrete plan for the separate promotion task:
1. Copy `jack_belt_r1.png` → `assets/puppet/layers/belt/jack_belt.png` (byte-identical).
2. Write a production manifest documenting:
   - Source = CoPainter `layer_77.png` (sha256, original ZIP path).
   - Anchor on See-through 768×768 canvas: top-left (347, 379), scale 0.7100.
   - Naming convention (`jack_belt.png` — one file, no left/right).
   - The do-not list from the staging manifest.
3. Update the cloud audit report's downstream-promotions table to record the belt promotion.

## Comparison to See-through

See-through merges the belt visually into the topwear+legwear overlap with no addressable layer. CoPainter is the **only source we have** for an isolatable belt asset. So this is a clear "CoPainter wins" specifically for the belt category — without replacing any See-through asset.

## What this QC does NOT prove

- That the See-through canvas (768×768) is the final puppet render canvas — if the production rig uses a different canvas size, the belt top-left coords will need to be transformed.
- That `jack_head_front_base.png` (1024×1024) layouts will accept the belt at proportional coordinates — not tested in this task. If a head-canvas-based puppet uses belt placement, an equivalent anchor derivation is required on that canvas.
- That subsequent CoPainter regenerations will preserve the same belt dimensions — `layer_77` may be ZIP-instance-specific. SHA recorded in manifest for change detection.

## Decision

**No promotion in this task.** Belt is staging-ready. Recommend: separate explicit promotion task to copy `jack_belt_r1.png` into `assets/puppet/layers/belt/jack_belt.png` with the production manifest described above.
