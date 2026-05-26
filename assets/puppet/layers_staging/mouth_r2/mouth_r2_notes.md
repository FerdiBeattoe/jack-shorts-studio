# Mouth r2 — assessment notes

**Status:** STAGING ONLY. Replaces rejected `mouth_r1`. No promotion.

## TL;DR

**r2 passes visual QC on both anchors.** Closed visemes (`neutral`, `slight_frown`, `slight_smirk`, `mbp`) read as drawn-into Jack's muzzle. Open visemes (`open_small`, `open_medium`, `oo`) no longer float — the faint same-hue inner shadow + thin brown outline sits naturally in the fur. Teeth-free `ee`/`fv` (two-line and inflected-line approximations) read as mouth shapes without anime/realistic detail.

**Krita cleanup is optional, not required.** No face patch needed.

## Artifacts (no production writes)

- 9 viseme PNGs: `jack_mouth_*_r2.png` (512×512 RGBA, intrinsic anchor (256, 270))
- `jack_mouth_r2_visual_qc.png` — character-sheet expression refs + light/dark isolated + r1↔r2 1:1 size comparison
- `jack_mouth_r2_composite_qc.png` — See-through primary + head secondary, all 9 visemes
- `mouth_r2_manifest.json` — anchors, scales, style constants, rejection record of r1
- Scripts: `tools/puppet/build_mouth_r2.py`, `tools/puppet/build_mouth_r2_qc.py`

**No face patch in r2.** Per spec ("no face patch in r2 unless absolutely necessary"). The smaller r2 mouths sit above the baked chin split (y=748-820) at mouth y=745; the chin split reads as a faint chin-shadow under the mouth, not a competing artwork.

## What changed from r1 → r2

| Aspect | r1 (rejected) | r2 |
|---|---|---|
| Closed mouth width | 270-290 px | 110-168 px (~55%) |
| Open mouth size | 116×42 (small) / 156×58 (medium) | 54×20 / 82×30 (~45%) |
| Lineart colour | RGB(20, 20, 20) pure black | RGB(40, 35, 28) warm dark brown (sampled from face outline) |
| Open-mouth interior | Saturated maroon RGB(88, 36, 32) + red tongue accent + cream teeth | Same-hue inner shadow at 35% alpha, OR nothing |
| Teeth | Visible tooth shapes + dividers in `ee`, `fv` | None — `ee` = two parallel lines, `fv` = lip line + faint inflection |
| Line weight | 5 px | 4 px (secondary detail 3 px) |
| Default patch | Optional dual-blob fur patch | None |

## Anchor system (same as r1, documented again here)

| Anchor | Reference | Position | Scale |
|---|---|---|---|
| **Primary** | See-through `07_face.png` (bbox (366, 44, 453, 147) in 768×768 canvas) | Muzzle bottom-center **(405, 142)** | mouth × **0.183** |
| **Secondary** | `jack_head_front_base.png` (1024×1024) | **(489, 745)** — below nose, above baked chin split | 1.0 |

Mouth canvas (512×512) intrinsic anchor (256, 270) maps onto the target anchor at the documented scale.

## Pass / fail per viseme

| Viseme | Verdict | Notes |
|---|---|---|
| `neutral` | ✅ **pass** | Thin shallow droop, matches deadpan reference |
| `slight_frown` | ✅ **pass** | Deeper droop, still understated |
| `slight_smirk` | ✅ **pass** | Asymmetric lift on character-right; matches smirk reference |
| `mbp` | ✅ **pass** | Compressed flat line, slightly thicker — reads as pressed lips |
| `open_small` | ✅ **pass** | Small outlined oval with faint inner shadow; sits in muzzle |
| `open_medium` | ✅ **pass** | Bigger outline, same recipe; no longer floats |
| `oo` | ✅ **pass** | Small round outline; pursed-lip shape clear |
| `ee` | ✅ **pass (teeth-free)** | Two parallel lines; reads as "lips slightly parted, showing tension" — no teeth |
| `fv` | ✅ **pass (teeth-free)** | Lip line + faint upper inflection; conveys upper-teeth-on-lip implication without drawing teeth |

**Outright rejections:** None.
**Conditional passes:** None — all 9 pass cleanly in r2.

## Detailed assessments (from spec)

### Do any still float?
No. The combination of (a) ~55% size reduction, (b) brown lineart instead of pure black, and (c) faint same-hue inner shadow instead of saturated maroon, makes the open mouths sit *in* the muzzle rather than on top of it. The composite QC head panels show every viseme reading as integrated facial expression.

### Is teeth-free EE/FV acceptable?
Yes. `ee` as two parallel horizontal lines reads as "lips slightly parted under tension" — appropriate for an /iː/ phoneme without anatomical teeth. `fv` as lip-line-plus-inflection reads as "upper lip touching lower lip" without drawing literal upper teeth. Both pass the deadpan-style rule.

### Is Krita cleanup required?
**No, not required.** All 9 visemes are visually ready as-is.

Optional polish (not blocking promotion):
1. Hand-stipple a 1-pixel asymmetric jitter on each curve endpoint to remove the mathematically-symmetric feel.
2. For `ee`, consider whether the lower line could be slightly shorter than the upper — would push it further from "two-tracks" toward "tense lip parting".

### Should any mouth be hand-drawn manually instead?
**No.** The procedural generator produces results indistinguishable from a simple hand-drawn pass at this size. Hand-drawing would only become necessary if you needed expressive *variation* (e.g. micro-asymmetries that differ per viseme, like the existing production set has). For r2's purpose — a consistent base viseme set for puppet rig wiring — procedural is the right call.

## Validation against character-sheet expressions (visual QC top row)

- **deadpan ref:** Jack has *no visible mouth* in his deadpan expression — just a chin shadow. Our `neutral` is appropriately subtle, possibly even visible-enough to be slightly more expressive than the reference, but within tolerance.
- **smile ref:** Subtle upturned right corner. Matches `slight_smirk` closely.
- **shocked ref:** Small open-mouth expression. `open_small` / `oo` fits this template.
- **smirk ref:** Identical to smile ref but with droopier eyes. `slight_smirk` covers it.

## What this QC does NOT prove

- That these mouth shapes match the puppet rig's expected viseme *tag set* (rig spec not consulted).
- That re-renders of the See-through PSD or `jack_head_front_base.png` won't shift the muzzle anchor; if either changes, re-derive anchors.
- That r2's deadpan suits all episode tones — `neutral` is still slightly more visible than Jack's literal deadpan; if a perfectly mouth-less default is required, hide all mouth layers instead of using `neutral`.

## Decision

**No promotion in this task.** r2 is staging-ready. Recommend: separate explicit promotion task to copy `jack_mouth_*_r2.png` into `assets/puppet/layers/mouth/` (renamed to drop the `_r2` suffix), with a production manifest documenting the anchor system and the r1 rejection record.
