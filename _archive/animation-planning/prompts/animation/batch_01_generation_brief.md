# Jack Animation Pack v1 — Batch 1 Generation Brief

**Date:** 2026-05-19  
**Batch:** 1 of N — Design-lock reference sheets only  
**Status:** Ready to generate

---

## What This Batch Produces

| # | Output file | Purpose | Status |
|---|-------------|---------|--------|
| 1 | `assets/puppet/refs/jack_expression_reference_sheet.png` | Locks all 8 expressions before puppet layers are cut | ⬜ Not generated |
| 2 | `assets/puppet/refs/jack_viseme_reference_sheet.png` | Locks all 11 mouth shapes before viseme layers are cut | ⬜ Not generated |

**Why sheets first, layers second:**  
These sheets are design-lock artefacts. Once accepted, every subsequent layer generation uses them as the style anchor. A rejected sheet costs one generation pass. A rejected layer set after 30 individual renders costs much more.

**Do not generate individual layers until both sheets are accepted.**

---

## Design Anchor (read before generating anything)

Jack is a humanoid golden retriever account manager. He exists in a narrow tonal band: professional composure on the outside, controlled internal chaos on the inside. Every expression is filtered through that professional mask.

**Canonical existing assets — use these as style reference:**
- `public/images/jack_01_forward_calculating.png`
- `public/images/jack_02_tie_fix_confident_smirk.png`
- `public/images/jack_03_turning_to_monitor.png`

**Core visual spec (do not deviate):**
- Species: humanoid golden retriever, adult male
- Fur: golden/amber — warm, not bright yellow, not orange, not brown
- Nose: black, round, small — centred on the muzzle
- Eyebrows: dark, thick, highly expressive — the primary emotional instrument
- Eyes: dark almond-shaped with warm golden irises — not round, not anime
- Ears: floppy, golden, forward-set — present but not the focus
- Muzzle: anthropomorphic but restrained — readable as a muzzle, not an exaggerated cartoon snout
- Build: average adult male, seated posture
- Clothing: black slim-fit suit jacket, white dress shirt, black skinny tie — professional but slightly lived-in
- Style: flat 2D illustration, clean vector-like linework, cel shading — professional animated series
- Lighting: soft from upper-left throughout — no dramatic shadows, no rim lights, no fill from below

---

## Batch 1, Asset 1 — Expression Reference Sheet

**Save path:** `assets/puppet/refs/jack_expression_reference_sheet.png`

---

### EXPRESSION SHEET — MAIN PROMPT

Copy everything between the triple-dash lines. Paste as-is into your image generation tool.

---

```
Character design reference sheet. Professional 2D animated series style.

Character: humanoid golden retriever, adult male, professional account manager. 
Golden/amber fur. Black round nose centred on muzzle. Dark thick expressive eyebrows. 
Dark almond-shaped eyes with warm golden irises. Floppy golden ears. 
Slight anthropomorphic muzzle — readable but not exaggerated.
Black slim-fit suit jacket, white dress shirt, black skinny tie.
Flat vector-like 2D illustration, clean consistent linework, soft cel shading.
Lighting: soft from upper-left, no dramatic shadows.

LAYOUT: 4-column by 2-row grid. 8 panels total. Each panel is the same size.
Clean light grey sheet background. Thin panel borders between cells.
Each panel has the expression name printed in small text below the face.

PANEL 1 — "Neutral":
Eyebrows flat, horizontal, resting. Zero tension.
Eyes fully open. Pupils centred, gaze directly forward.
Mouth closed, flat or a very faint natural downward curve. Professional composure.

PANEL 2 — "Concerned":
Both inner brows drawn upward and inward — a slight V-shaped furrow between them.
Not a deep frown. A professional's managed concern.
Eyes wide open, slightly wider than neutral. Pupils centred.
Mouth closed.

PANEL 3 — "Thinking":
LEFT eyebrow in the image (character's right) raised slightly higher than the right.
Right eyebrow neutral/lower. Asymmetric — only one brow doing the work.
Eyes very slightly narrowed. Pupils angled fractionally upward and to the left in the image.
Mouth closed.

PANEL 4 — "Quietly Paranoid":
Both eyebrows raised and held. Controlled vigilance — not shock, not surprise.
Eyes slightly wider than neutral. Pupils shifted fractionally toward the left in the image (character looking toward a monitor).
Mouth closed.

PANEL 5 — "Controlled Smug (building)":
LEFT eyebrow in the image arched upward — a single confident arch. Right eyebrow neutral/lower.
Eyes slightly lidded — not half-closed yet, just the beginning of the "I know something" look.
Mouth closed.

PANEL 6 — "Smug (held)":
LEFT eyebrow in the image arched high and confident. Right eyebrow lower, slightly amused.
Eyes clearly lidded — half-open, deliberately unhurried. The look of someone choosing not to react.
Mouth closed.

PANEL 7 — "Side-Eye":
LEFT eyebrow in the image very slightly elevated. Right eyebrow neutral. Subtle.
Pupils clearly shifted to the LEFT in the image — a sideways glance without turning the head.
More white of eye visible on the right side of each eye.
Mouth closed.

PANEL 8 — "Blink (mid-blink)":
Both upper eyelids descended approximately 70% — eyes mostly closed.
Lower eyelids unchanged — only upper lids move.
Eyebrows neutral. Mouth closed.

CRITICAL RULES ACROSS ALL 8 PANELS:
- Same character. Same face proportions. Same fur colour. Same clothing.
- Same head angle in all panels: front-facing, no rotation, no tilt.
- Same lighting in all panels: soft from upper-left.
- Mouth is CLOSED and NEUTRAL in every panel. Mouth shape does not change between panels.
- Eyebrows and eye state are the only features that change between panels.
- No open mouths. No visible teeth. No tongues.
- No extreme expressions. This character is a professional.
- No random objects. No speech bubbles. No added accessories.
- Panel labels are the only text in the image.
```

---

### EXPRESSION SHEET — TOOL-SPECIFIC ADDITIONS

**If using Midjourney:**
Append to the end of the prompt:
```
--ar 2:1 --style raw --v 6
```

**If using DALL-E 3 / ChatGPT image generation:**
Add before your prompt:
```
Generate exactly as specified. Do not add creative liberties. Do not add open mouths or smiling expressions. Follow the layout and panel descriptions precisely.
```

**If using Adobe Firefly:**
Use the "Reference image" feature and attach `public/images/jack_01_forward_calculating.png` as the style reference with weight set to Strong.

**If using Stable Diffusion / ComfyUI:**
Use the negative prompt block in the next section. Set CFG scale to 7–9. Use a character-design or illustration LoRA if available.

---

## Batch 1, Asset 2 — Viseme Reference Sheet

**Save path:** `assets/puppet/refs/jack_viseme_reference_sheet.png`

---

### VISEME SHEET — MAIN PROMPT

Copy everything between the triple-dash lines. Paste as-is.

---

```
Character design reference sheet showing 11 mouth shapes for lip sync animation. Professional 2D animated series style.

Subject: the lower face and muzzle of a humanoid golden retriever character.
Golden/amber fur. Black round nose visible at the top of each panel (fixed, does not move).
Slight anthropomorphic muzzle. Flat 2D illustration, clean consistent linework, soft cel shading.
Lighting: soft from upper-left, no dramatic shadows.
The rest of the face (eyebrows, ears, eyes) is NEUTRAL and DOES NOT CHANGE between panels. Only the mouth/muzzle changes.

LAYOUT: 4-column by 3-row grid. 11 panels + 1 empty label panel.
Clean light grey sheet background. Thin panel borders.
Each panel shows the same muzzle/lower face area at the same scale and angle.
Each panel has the shape name printed in small text below.

PANEL 1 — "Neutral":
Mouth completely closed. Muzzle line flat. A very faint natural downward curve.
No teeth. No tongue. Just the closed muzzle.

PANEL 2 — "Open":
Jaw drops. Lower muzzle descends. Opening is rounded, approximately 30–35% of muzzle height.
Upper muzzle stays fixed at the nose.
Upper row of small clean teeth faintly visible at top of opening. Bottom teeth faintly at lower edge.
Teeth are small, off-white, minimally detailed. Not oversized.

PANEL 3 — "Ee":
Mouth stretched horizontally outward. Corners pulled sideways.
Both rows of small teeth visible. Mouth narrow vertically, wide horizontally.
Not a smile — this is the mechanical shape of the "ee" phoneme.

PANEL 4 — "Oh":
Rounded oval opening. Both the upper and lower muzzle contribute to the shape.
Width narrows compared to Open. Opening is oval, moderate height.
No teeth visible. Corners rounded.

PANEL 5 — "Ooh":
Lips/muzzle pursed and projected slightly forward toward the viewer.
Smallest opening of all open shapes — narrow, almost circular.
Forward projection is the key visual feature. No teeth.

PANEL 6 — "M-B-P":
Mouth completely closed, lips pressed firmly together.
Very slightly more corner tension than Neutral — nearly identical but with implied pressure.
No opening, no teeth, no tongue.

PANEL 7 — "F-V":
Lower muzzle edge (lower lip) curled slightly inward under the upper teeth.
Upper teeth faintly visible at top of a very slight opening.
Subtle shape. The lower muzzle tucks in rather than dropping down.

PANEL 8 — "L":
Mouth open approximately 20% of muzzle height.
Tongue tip barely visible at the upper teeth/gum line.
The tongue is small, fleshy, just the tip — not a large tongue, not dramatic.
Upper teeth visible. Opening narrower than Oh.

PANEL 9 — "S":
Teeth very close together or touching — near-closed position.
Slight gap between upper and lower tooth rows visible.
Corners neutral. A tightly controlled near-closed shape.

PANEL 10 — "Smile":
Mouth closed. Corners of the muzzle raised in a subtle, genuine smile.
Not a grin — a controlled satisfaction. Mouth stays closed.

PANEL 11 — "Smirk":
One side only — left corner of muzzle (right side of image, viewer's right) raised.
Right corner (viewer's left) flat/neutral.
Asymmetric knowing expression. Mouth mostly closed. Very subtle.
The smirk of professional private satisfaction.

PANEL 12 — empty. Fill with the character name "JACK" as a small centred label only.

CRITICAL RULES ACROSS ALL 11 PANELS:
- Same muzzle. Same dimensions. Same scale. Same angle (front-facing, slight downward view so muzzle is visible).
- Black nose position is IDENTICAL in every panel — fixed anchor point.
- Muzzle width does not change between panels — only the opening and internal shapes change.
- Eyebrows, ears, and upper face are NEUTRAL and IDENTICAL in every panel.
- Fur colour is consistent golden/amber throughout.
- Linework weight is consistent throughout.
- Teeth when visible: small, clean, off-white. Not cartoon-white, not oversized.
- No drool, no fangs, no exaggerated gapes.
- Transparent-feeling background per panel for clean visibility. Sheet background is light grey.
- Panel labels are the only text in the image.
```

---

### VISEME SHEET — TOOL-SPECIFIC ADDITIONS

**If using Midjourney:**
Append to the end of the prompt:
```
--ar 4:3 --style raw --v 6
```

**If using DALL-E 3 / ChatGPT:**
Add before your prompt:
```
Generate exactly as specified. Each panel must show the same muzzle at a consistent scale. Do not add open mouths where the spec says closed. Do not add large tongues. Follow panel descriptions precisely.
```

**If using Adobe Firefly:**
Use `public/images/jack_01_forward_calculating.png` as a style reference with weight Strong.

**If using Stable Diffusion:**
Use the negative prompt block below.

---

## Negative Prompt / Failure Prevention Block

This block applies to BOTH sheets. Use it as a negative prompt where your tool supports one (Stable Diffusion, some Midjourney workflows), or paste it as a DO-NOT-DO section into tools that accept freeform instructions.

---

```
NEGATIVE PROMPT — DO NOT INCLUDE ANY OF THE FOLLOWING:

Style failures:
- photorealistic fur or skin
- painterly or impressionistic shading
- anime, manga, or chibi proportions
- thick black anime outlines with no interior detail
- watercolour or sketch style
- pixel art or low-resolution rendering

Character drift:
- any non-golden-retriever dog breed features
- brown fur, orange fur, cream fur, grey fur, white fur
- blue eyes, green eyes, red eyes
- round bubble eyes or anime eyes
- small or thin eyebrows — eyebrows must be DARK and THICK
- pointed ears, upright ears, any non-floppy ear shape
- wolf-like muzzle, long pointed snout, flat pug-like nose
- extra accessories (glasses, hat, badge, earrings, watch)
- clothing other than black suit jacket, white shirt, black tie
- coloured tie, patterned tie
- exposed chest, open shirt
- missing tie

Expression failures (expression sheet):
- any open mouth or visible teeth in any of the 8 expression panels
- laughing, screaming, crying, shocked, or disgusted expressions
- tongues visible in expression panels
- extreme emotions — all expressions are filtered professional composure
- eyebrows that look angry (downward-slanting) rather than raised/concerned
- identical expressions in all panels (no differentiation)

Viseme failures (viseme sheet):
- large tongue, floppy tongue, exaggerated tongue
- fangs, oversized teeth, cartoon-white teeth
- drool
- exaggerated wide-open gaping mouths
- muzzle changing size or width between panels
- nose position changing between panels
- expression/eyebrow drift between panels

Layout failures:
- uneven panel sizes
- panels cut off at edges
- faces at different scales across panels
- different head angles across panels (must all be front-facing)
- background elements bleeding into panels
- watermarks, signatures, model text
- labels in an unusual font or style (keep them minimal and small)

Technical failures:
- compression artefacts
- blurry linework
- inconsistent line weight
- colour banding in flat areas
```

---

## Save Paths

| Asset | Exact save path | Directory exists? |
|-------|-----------------|-------------------|
| Expression reference sheet | `assets/puppet/refs/jack_expression_reference_sheet.png` | ✅ Yes |
| Viseme reference sheet | `assets/puppet/refs/jack_viseme_reference_sheet.png` | ✅ Yes |

Save as PNG. Do not save as JPEG (JPEG compression degrades line art).  
Minimum recommended output resolution: 2000px on the longest edge.  
Preferred: 2400×1200 for expression sheet (4:2 ratio), 2400×1800 for viseme sheet (4:3 ratio).

---

## QC Checklist — Expression Sheet

Review the generated sheet against this checklist before accepting it.

### Hard failures — REJECT and regenerate if any of these are true:
- [ ] Any panel has an open mouth or visible teeth
- [ ] Any panel has an expression not matching the spec (e.g. panel 1 looks smug, panel 6 looks neutral)
- [ ] Panels 1 and 6 are visually identical (no differentiation between Neutral and Smug)
- [ ] Head angle varies across panels (any tilting, rotation, or scale inconsistency)
- [ ] Character design differs from existing keyframes (wrong fur colour, wrong eye shape, wrong nose)
- [ ] Extreme emotion present (shouting, crying, shock, wild grin)
- [ ] Panels are blank or corrupted

### Soft failures — ACCEPT with note, fix in Photoshop:
- [ ] Label text is unreadable or missing — add labels manually in Photoshop
- [ ] Panel borders are uneven — crop and recompose in Photoshop
- [ ] One panel's brow is slightly off-spec — adjust in Photoshop rather than regenerating
- [ ] Fur colour is slightly warm or cool vs keyframes — colour-correct in Photoshop

### Accept criteria — sheet is GOOD when:
- [ ] All 8 panels show the same character at the same scale and angle
- [ ] Mouth is visibly closed and neutral in all 8 panels
- [ ] Expressions are distinguishable from each other — eyebrows and eye state vary
- [ ] Neutral (panel 1) looks clearly different from Smug (panel 6)
- [ ] Concerned (panel 2) shows visible inner-brow tension vs Neutral
- [ ] Thinking (panel 3) shows clear asymmetry — one brow visibly higher than the other
- [ ] Side-eye (panel 7) shows pupils shifted left
- [ ] Blink (panel 8) shows eyes mostly closed
- [ ] Style is consistent with `public/images/jack_01_forward_calculating.png`
- [ ] No teeth, no tongue, no open mouths anywhere in the sheet

---

## QC Checklist — Viseme Sheet

### Hard failures — REJECT and regenerate:
- [ ] Muzzle width changes between panels (nose anchor drifts)
- [ ] Eyebrows change expression between panels (any non-neutral brow)
- [ ] Panels 1 (Neutral) and 6 (M-B-P) are visually identical to each other AND to panels 2 (Open) — no differentiation
- [ ] Panel 2 (Open) muzzle does not visibly open
- [ ] Panel 5 (Ooh) is not visibly different from Panel 4 (Oh) — pucker must be distinct
- [ ] Large tongue visible in any panel except Panel 8 (L)
- [ ] Character design differs from existing keyframes
- [ ] Panels are blank or corrupted

### Soft failures — ACCEPT with note, fix in Photoshop:
- [ ] Teeth in Panel 9 (S) or Panel 3 (Ee) are too bright/white — desaturate slightly
- [ ] Label text missing — add manually
- [ ] Panel 12 (Smirk) asymmetry is very subtle — acceptable if the corner raise is at least slightly readable
- [ ] One panel's lighting is slightly inconsistent — acceptable if not dramatic

### Accept criteria — sheet is GOOD when:
- [ ] All 11 panels show the same muzzle at the same scale, angle, and position
- [ ] Black nose position is identical across all panels — fixed anchor
- [ ] The following shapes are clearly distinguishable from each other:
  - Neutral (closed flat) vs Open (jaw dropped) — must be obvious
  - Oh (rounded oval) vs Ooh (pursed/projected) — must be distinct
  - Ee (wide horizontal) vs Neutral — must be obviously different
  - Smile (corners up, closed) vs Neutral (flat, closed) — subtle but readable
- [ ] Eyebrows are neutral/identical in every panel
- [ ] Teeth (where visible) are small, clean, off-white — not cartoon-white, not oversized
- [ ] No large tongue, no drool, no fangs in any panel
- [ ] Style matches existing keyframes
- [ ] The sheet reads as a professional production reference sheet at a glance

---

## Cropping and Cutting Instructions (after acceptance)

The reference sheets are kept whole for QC purposes. Individual panels are cut when assembling the PSD. Here is how to do it.

### Expression Sheet — Panel Extraction (optional, for Photoshop assembly reference)

If the sheet is a clean 4×2 grid at 2400×1200px, each panel is approximately 600×600px.

| Panel | Approx crop (x, y, w, h) at 2400×1200 |
|-------|---------------------------------------|
| Panel 1 — Neutral | 0, 0, 600, 600 |
| Panel 2 — Concerned | 600, 0, 600, 600 |
| Panel 3 — Thinking | 1200, 0, 600, 600 |
| Panel 4 — Quietly Paranoid | 1800, 0, 600, 600 |
| Panel 5 — Controlled Smug | 0, 600, 600, 600 |
| Panel 6 — Smug (held) | 600, 600, 600, 600 |
| Panel 7 — Side-Eye | 1200, 600, 600, 600 |
| Panel 8 — Blink | 1800, 600, 600, 600 |

**Adjust crop coordinates based on your actual output dimensions.** These are estimates for a perfect 4×2 grid.

In Photoshop: use the Slice Tool or the Crop Tool on a duplicated layer. Save each slice as a separate PNG. Label using the expression names.

**Note:** The expression sheet is a reference document only. The actual eyebrow layers for the PSD will be individual clean renders, not cropped from the sheet. The sheet tells you what the result should look like; it is not the source material for puppet layers.

### Viseme Sheet — Panel Extraction (for PSD review, not final puppet layers)

Same principle. At 2400×1800 (4×3 grid), each panel is approximately 600×600px.

| Panel | Shape |
|-------|-------|
| Row 1, Col 1 | Neutral |
| Row 1, Col 2 | Open |
| Row 1, Col 3 | Ee |
| Row 1, Col 4 | Oh |
| Row 2, Col 1 | Ooh |
| Row 2, Col 2 | M-B-P |
| Row 2, Col 3 | F-V |
| Row 2, Col 4 | L |
| Row 3, Col 1 | S |
| Row 3, Col 2 | Smile |
| Row 3, Col 3 | Smirk |
| Row 3, Col 4 | (empty / character label) |

**Note:** Like the expression sheet, the viseme sheet is a QC reference. Individual clean mouth layers for the PSD will be generated separately in Batch 2, using the accepted viseme sheet as the style anchor.

---

## Manifest Update Instructions (after both sheets are accepted)

Once both sheets are saved to the correct paths and pass QC, update `manifests/jack_puppet_manifest_v1.json`.

Find these two entries and change `"status": "missing"` to `"status": "present"` for each:

**Entry 1:**
```json
{
  "asset_id": "ref_expression_sheet",
  "required_file_path": "assets/puppet/refs/jack_expression_reference_sheet.png",
  ...
  "status": "present"
}
```

**Entry 2:**
```json
{
  "asset_id": "ref_viseme_sheet",
  "required_file_path": "assets/puppet/refs/jack_viseme_reference_sheet.png",
  ...
  "status": "present"
}
```

After updating, run the validation script to confirm:

```
node scripts/validate-jack-puppet-pack.mjs
```

The script will show these two assets as present. The overall count will move from 4/52 present to 6/52 present. The blocked count will decrease from 40 to 38.

---

## What Comes Next (Batch 2)

Once both sheets are accepted and the manifest is updated, Batch 2 generates the individual puppet layers using the accepted sheets as the style anchor. Batch 2 priority order:

1. `jack_head_front_base.png` — the base canvas for all face compositing
2. All 11 mouth/viseme layers — generated with the accepted viseme sheet as reference
3. Eye layers (open/half/closed, left and right) — 6 files
4. Eyebrow layers (neutral + concerned minimum) — 4 files
5. `jack_torso_front.png` — body base
6. `jack_tie_straight.png` — tie physics layer

**Do not start Batch 2 until both Batch 1 sheets are accepted.**
