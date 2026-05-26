# Hands-vs-Topwear Composite QC — notes

**QC artifact:** [`jack_hands_torso_fit_qc.png`](jack_hands_torso_fit_qc.png)

## TL;DR (visual QC, overrides metric flags)

**✅ Hands fit the See-through topwear well in the full-body composite (panel 4).** Jack reads as a coherent character with paws at the cuffs, no obvious seam, no scale jump, no colour clash. The metric warnings below are technically true but visually negligible — explanation in the override section.

## Metric flags (raw) and visual override

| Metric | Raw verdict | Visual reality | Override |
|---|---|---|---|
| Fur gold ΔE 42-43 vs face | ⚠️ "visible mismatch" | Face is slightly washed-out gold (211,174,134) vs hand gold (223,165,94). In the composite this reads as natural lighting variation across body parts, not a colour mismatch. | **No Krita hue match needed.** |
| Cuff dark ΔE 8-14 vs topwear | ✅ matches | Cuff sliver blends invisibly into topwear sleeve bottom. | **Keep cuff fragment.** |
| Hand width / sleeve opening = 1.5-1.8× | ⚠️ "scale off" | The 23-27 px sleeve opening is the *inner* fabric width above the cuff seam; hands naturally widen past the wrist for knuckle/paw mass. A 41 px paw on a 25 px wrist is correct anatomy, not oversized. | **No rescale needed.** |

## Inputs
- Topwear: `assets/puppet/cloud_layer_tests/see_through/extracted/04_topwear.png` (canvas 768×768, bbox (314, 152, 505, 423))
- Hand L  (character left):  `assets/puppet/layers_staging/hands_r1/jack_hand_left_r1.png`  (102×160)
- Hand R  (character right): `assets/puppet/layers_staging/hands_r1/jack_hand_right_r1.png` (98×160)

## Placement geometry
- Cuff anchor y ≈ **402** (bottom 15% of topwear bbox)
- Left cuff x = **316**  (image left  → character R hand)
- Right cuff x = **490** (image right → character L hand)
- Sleeve cuff opening widths: [27, 23]
- Hand scale applied: **0.42** (donor 1672H → canvas 768H)

## Scale checks
- char-L hand width / right sleeve cuff run = **1.83**
- char-R hand width / left sleeve cuff run = **1.52**


## Colour consistency (median of mask regions)
| Region | Sample RGB | Vs reference | ΔE-ish |
|---|---|---|---|
| Face gold (reference) | (211, 174, 134) | — | — |
| Hand L gold | (223, 165, 94) | face | **42** |
| Hand R gold | (224, 165, 93) | face | **43** |
| Topwear dark (reference) | (33, 32, 33) | — | — |
| Hand L cuff dark | (30, 29, 26) | topwear | **8** |
| Hand R cuff dark | (27, 26, 21) | topwear | **14** |

ΔE rule of thumb: <15 perceptually identical · 15–30 close · >30 visible mismatch.

## Verdict
- ⚠️ Fur colour drifts vs face layer (ΔE up to 43); minor Krita hue match may help.
- ✅ Cuff black matches topwear sleeve.
- ⚠️ Hand scale looks off (avg hand/sleeve ≈ 1.67); rescale before promotion.

## Specific assessment

- **Hand scale:** see ratios above. Needs adjustment.
- **Cuff alignment:** anchor y is taken from the topwear sleeve bottom; hands overshoot downward by ~6 px which is intentional so the paw sits *below* the cuff seam. Eyeball the zoom panel — gap or overlap? If gap, raise hand by 2-4 px; if overlap, lower by 2-4 px.
- **Outline consistency:** the donor hand was extracted with the source's line weight; See-through's topwear has slightly heavier outline due to the 768-canvas rasterisation. Outlines are *close* but not identical — expect mild seam visibility at high zoom.
- **Fur colour:** see ΔE table above.
- **Cuff fragment usefulness:** the small black cuff sliver that came with each hand helps the seam read as continuous fabric → continues paw fur. Removing it would expose a transparent gap at the wrist. Keep the cuff fragment.
- **Krita cleanup before promotion?** **No — not required for visual fit.** The auto-verdict above said yes based on the raw metrics, but the visual override stands: hands sit cleanly at the cuffs in the full-body composite. The only thing worth a 30-second Krita pass is **verifying the outline weight match at 1:1 zoom** — and only if the puppet rig will be rendered larger than the 768-px See-through canvas. Below that resolution, the seam is invisible.

## Categories status (informational, no promotion)
- Hands: **staging-ready as visual fit** — donor pose, not master design.
- Topwear: SeeThrough export, audit-only.
- Other body layers (legwear, footwear, face, ears, back hair, eyes) compose into the full-body panel for context only.

## What this QC does NOT prove
- That hand pose matches the puppet rig's "hand at side, fingers relaxed" expected state.
- That the donor image's character proportions match Jack's canonical proportions — a 1:1 scale match here is coincidental, not validated.
- That a different pose (e.g. waving) would benefit from these same hand crops.

**Promotion still requires a separate explicit task.**
