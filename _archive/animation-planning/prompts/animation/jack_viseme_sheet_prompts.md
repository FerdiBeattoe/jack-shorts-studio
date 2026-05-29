# Jack Viseme Sheet Prompts

**Version:** 1.0  
**Date:** 2026-05-19  
**Purpose:** Prompts for generating Jack's mouth/viseme shapes for Character Animator lip sync.

---

## Critical Warnings

Read these before generating any viseme layer:

1. **Same head angle for every shape.** All visemes must be generated from the same viewing angle — front-facing. If angle drifts, they will not composite cleanly.
2. **Same lighting for every shape.** Soft from upper-left, matching the head base layer.
3. **Same muzzle dimensions.** The muzzle width and the position of the nose anchor must not change between shapes. Only the lower muzzle, corners, and internal shapes change.
4. **Same linework weight.** Consistent line thickness across all shapes.
5. **Same fur colour and texture.** Golden/amber, same as the head base layer.
6. **Transparent background.** Every viseme layer is PNG-32 with full alpha channel.
7. **No expression drift.** These are MOUTH SHAPES only. The eyebrows, ears, and overall head expression must remain neutral. The rest of the face does not change between visemes.
8. **No random teeth unless specified.** Teeth should be minimal, off-white, not over-detailed.
9. **Do not generate gaping mouths.** Jack is a professional.
10. **Generate all shapes in a single session** if possible, using the same style/seed parameters.

---

## Base Prompt (applies to ALL viseme layers)

Include this base in every viseme prompt:

```
Close-up of a humanoid golden retriever muzzle and lower face, front-facing view.
Golden/amber fur, black round nose at the top of frame (fixed position).
Flat 2D illustration style, clean linework, cel shading.
Neutral expression — no eyebrow movement, no ear movement.
Transparent background — muzzle area only, with surrounding fur blending to alpha.
Soft lighting from upper-left. Consistent with a professional animated series character.
```

---

## Prompt V1 — Neutral (Rest)

**File target:** `assets/puppet/layers/mouth/jack_mouth_neutral.png`

```
[BASE PROMPT]
Mouth shape: NEUTRAL / REST.
Lips completely closed. Corners in neutral position — neither pulled up nor down.
A very slight, almost imperceptible natural downward curve — this is a professional's 
default expression, not a frown.
No teeth visible. No tongue. Just the closed muzzle line.
```

---

## Prompt V2 — Open (Ah)

**File target:** `assets/puppet/layers/mouth/jack_mouth_ah.png`

```
[BASE PROMPT]
Mouth shape: OPEN / AH.
Jaw drops. Lower muzzle descends approximately 35% of muzzle height.
Rounded opening. Upper muzzle stays anchored at the nose.
Upper teeth row faintly visible at top of opening. Lower teeth at bottom edge.
Teeth are small, clean, off-white — not detailed. Do not over-render teeth.
```

---

## Prompt V3 — Ee

**File target:** `assets/puppet/layers/mouth/jack_mouth_ee.png`

```
[BASE PROMPT]
Mouth shape: EE.
Horizontal stretch — corners pull outward slightly.
Both rows of teeth visible (top and bottom), mouth narrow vertically.
Slight upward pull at corners — not a smile, just the mechanical shape of "ee".
Teeth: small, clean, both rows showing. Do not over-render.
```

---

## Prompt V4 — Oh

**File target:** `assets/puppet/layers/mouth/jack_mouth_oh.png`

```
[BASE PROMPT]
Mouth shape: OH.
Rounded oval opening. Neither as wide as Ah nor as pursed as Ooh.
Both lips contribute to rounding. 
Opening is approximately oval, moderate size.
No teeth visible. Corners neutralised.
```

---

## Prompt V5 — Ooh / W

**File target:** `assets/puppet/layers/mouth/jack_mouth_oo_w.png`

```
[BASE PROMPT]
Mouth shape: OOH / W.
Lips pursed and projected slightly forward.
Smallest opening of all open mouth shapes — narrow, circular pucker.
No teeth visible. The defining characteristic is the forward projection 
and reduced opening.
```

---

## Prompt V6 — M B P (Lips Together)

**File target:** `assets/puppet/layers/mouth/jack_mouth_mbp.png`

```
[BASE PROMPT]
Mouth shape: M / B / P — lips together.
Lips fully pressed together — nearly identical to Neutral.
Very slight increase in lip pressure/tension at the corners.
This shape may be almost indistinguishable from Neutral to the viewer — 
that is correct. It signals the moment of bilabial closure.
No teeth, no opening.
```

---

## Prompt V7 — F V

**File target:** `assets/puppet/layers/mouth/jack_mouth_fv.png`

```
[BASE PROMPT]
Mouth shape: F / V.
Lower lip (lower muzzle edge) slightly tucked inward toward upper teeth.
Upper teeth are very faintly visible at the top of the slight opening.
This is a subtle shape — the key difference from Neutral is 
the slight inward curl of the lower lip/muzzle edge.
```

---

## Prompt V8 — L

**File target:** `assets/puppet/layers/mouth/jack_mouth_l.png`

```
[BASE PROMPT]
Mouth shape: L.
Mouth slightly open — approximately 20% of muzzle height.
Tongue tip is barely visible at the upper teeth/gum line.
The tongue is small, fleshy pink, just the tip — not a large tongue.
Upper teeth visible. Opening is narrower than Ah, less horizontal than Ee.
```

---

## Prompt V9 — S / D / T / N

**File target:** `assets/puppet/layers/mouth/jack_mouth_s_dtn.png`

```
[BASE PROMPT]
Mouth shape: S / D / T / N.
Teeth nearly together — very small gap between upper and lower rows.
This looks like a near-closed position with teeth showing — 
the jaw is slightly dropped but teeth are together or touching.
Corners neutral. A "tight" version of slightly-open.
```

---

## Prompt V10 — Smile

**File target:** `assets/puppet/layers/mouth/jack_mouth_smile.png`

```
[BASE PROMPT]
Mouth shape: SMILE — closed, controlled.
Corners of the mouth are raised in a genuine but restrained smile.
Mouth remains closed — no teeth showing.
This is NOT a grin. This is the smile of a man who has made a good point 
and is trying not to show how pleased he is about it.
Slight upward curve at corners. Subtle.
```

---

## Prompt V11 — Smirk (Trigger Override)

**File target:** `assets/puppet/layers/mouth/jack_mouth_smirk.png`

```
[BASE PROMPT]
Mouth shape: SMIRK.
One-sided: right corner of mouth (viewer's left) raised, left corner flat.
An asymmetric, knowing expression. Mouth mostly closed.
The smirk of a man who has delivered a devastating observation professionally.
Very subtle — this is not a villain smirk, it is a professional's moment of 
private satisfaction showing through.
One corner up, slight narrowing of that eye is implied in the shape.
```

---

## Reference Sheet Prompt (for QC)

After all viseme layers are generated, combine into a reference sheet:

**File target:** `assets/puppet/refs/jack_viseme_reference_sheet.png`

```
A reference sheet showing 11 mouth shape variations for a humanoid golden retriever character.
Arranged in a 4×3 grid. Each shape labelled below with its name:
Neutral, Open, Ee, Oh, Ooh, M-B-P, F-V, L, S, Smile, Smirk.

Same character face, same angle, same lighting in all panels.
Clean layout, white or light grey background for the sheet.
Each panel is approximately 400×400px.
Professional character design reference sheet format.
```

---

## QC Checklist Before PSD Assembly

After generating all viseme layers, verify:
- [ ] All 11 mouth layers have transparent backgrounds
- [ ] Nose position is identical in all layers (anchor point consistency)
- [ ] Muzzle width is consistent across all layers
- [ ] Fur colour matches `jack_01_forward_calculating.png`
- [ ] Linework weight is consistent
- [ ] No layer has a baked-in expression (eyebrows, ears must be neutral)
- [ ] Composite test: layer all shapes on top of head base — do they blend cleanly?
