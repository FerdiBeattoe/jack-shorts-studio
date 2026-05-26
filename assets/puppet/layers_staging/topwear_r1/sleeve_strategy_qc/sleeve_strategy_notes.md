# Sleeve integration strategy — QC notes

**Status:** QC ONLY. No promotion. No production writes. No Krita cleanup attempted.

## Artifacts

- `jack_topwear_sleeve_strategy_qc.png` — full-body comparison A/B/C/D on 768×768 canvas
- `jack_topwear_sleeve_strategy_zoom_qc.png` — 3× zoom of left wrist / right wrist / waist for all four options
- `sleeve_strategy_manifest.json` — anchors, pixel metric per option
- Script: `tools/puppet/qc_topwear_sleeve_strategy.py`

## TL;DR

**Recommendation: Option B — CoPainter topwear split + See-through handwear unmodified.**

The "black strip" failure I worried about during topwear staging **does not manifest visually** when hands and belt are added. The See-through handwear that extends past the CoPainter jacket reads as proper *shoulder/upper-arm bulk*, not as an overhang artifact. Jack looks more anatomically correct with handwear in than without. **No Krita cleanup needed.** **No mask needed.** Promote topwear with the simple draw order documented below.

## Visual findings per option

| Opt | Description | Overhang surv px | Visual reality |
|---|---|---|---|
| A | CoPainter top + hands + belt, **no** See-through handwear | 366 / 8303 | Clean but **shoulders look slightly narrow** — no upper-arm/shoulder bulk to fill the jacket silhouette |
| B | Same + See-through handwear **unmodified** | 8303 / 8303 | **Best.** Handwear adds proper shoulder volume; lateral overhang is minor and reads as natural arm geometry, not as strips |
| C | Same + See-through handwear **masked** to (jacket alpha OR y > jacket_bottom-4) | 366 / 8303 | Visually identical to A; the mask works as designed but the underlying problem is absent in B |
| D | See-through baseline (merged topwear + handwear) + belt + hands | 8303 / 8303 | Also clean and natural. Shirt/tie **more visible** in the open jacket V than CoPainter's. But: single merged layer, no rigging benefit |

## Why my prior "black strip" alarm was overstated

The earlier topwear staging QC didn't include the promoted hands. With hands placed at the wrist cuffs, the eye no longer reads the handwear lateral expansion as "extra strips" — it reads it as "Jack has shoulders inside the jacket." The original topwear_r1 notes flagged a worse problem than actually exists in the full composite.

## Specific assessment

### Does Option A leave wrist gaps?
**No wrist gaps**, but the **shoulder silhouette is undersized**. The jacket is 191 px wide; without handwear, there's nothing inside the jacket to suggest arm volume. Jack looks slightly flat at the shoulders.

### Does Option B show black sleeve strips?
**Technically yes** (8,303 px of handwear extend past the jacket silhouette) but **visually no**. The handwear reads as proper shoulder/upper-arm bulk in the side region; not as offending strips. The hand layer absorbs attention at the cuff, and the eye doesn't read the few-pixel lateral expansion as a defect.

### Is Option C worth Krita cleanup, or unnecessary?
**Unnecessary.** Option C's mask successfully removes the lateral expansion, producing a result visually identical to Option A — which is itself slightly worse than Option B (lacks shoulder volume). Investing Krita time to manually clip handwear has zero upside.

### Does Option D look worse than CoPainter split?
**No, D looks competitive.** D actually shows more shirt/tie through the jacket V (See-through's merged topwear has a more open neckline than CoPainter's). But D loses the per-layer rig addressability. If the rig doesn't need to animate jacket separately from shirt+tie, D is a viable fallback. For V1 of the puppet rig, the rig benefit is the deciding factor.

## Final recommendation

**Promote topwear with Option B layer strategy:**

Layer order (back to front) for the front-facing puppet:
1. See-through `back hair`, `ears`, `face`, `eyebrow`, `eyewhite`, `irides` (head)
2. See-through `legwear`, `footwear` (lower body)
3. **See-through `handwear` (unmodified)** ← keep this — provides shoulder/arm bulk
4. **CoPainter `jack_shirt_tie.png` ← staged as `jack_shirt_tie_r1.png`** (shirt under jacket)
5. **CoPainter `jack_jacket.png` ← staged as `jack_jacket_r1.png`**
6. Production `jack_belt.png` (locked)
7. Production `jack_hand_left.png` and `jack_hand_right.png` (locked)
8. Above-jacket facial overlays if used (mouth viseme, etc.)

No mask, no Krita pass, no recolour. The CoPainter alpha-max-254 quirk continues to be visually invisible.

## What this QC does NOT decide

- Whether the rig will ever need to animate the jacket independently of handwear — assumed yes for V1 (the whole point of promoting the split).
- Whether side / 3-quarter poses will need a different strategy — only the front pose is tested here.
- Whether the slightly-more-closed CoPainter jacket-V (less shirt visible than See-through D) is a stylistic regression — judged acceptable in this QC; revisit if the director disagrees.

## Decision matrix for the promotion task

| If you want… | Pick |
|---|---|
| Rig-addressable jacket + shirt/tie with natural shoulders | **B (recommended)** |
| Maximum jacket V opening (more shirt visible) | D |
| Minimal layer count | D |
| Maximum technical cleanliness (zero overhang pixels) but undersized shoulders | A or C |
| Krita-cleaned variant (not justified by this QC) | — defer |

## Stop

QC complete. No promotion. Topwear_r1 remains in staging. Next step: separate explicit promotion task that copies `jack_jacket_r1.png` → `assets/puppet/layers/topwear/jack_jacket.png` and `jack_shirt_tie_r1.png` → `assets/puppet/layers/topwear/jack_shirt_tie.png`, with a production manifest recording **Option B** as the chosen integration strategy.
