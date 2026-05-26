# Jack Viseme System v1

**Version:** 1.0  
**Date:** 2026-05-19  
**Target:** Adobe Character Animator Auto Mouth lip sync

---

## Overview

Visemes are the visual mouth shapes that correspond to groups of phoneme sounds. Adobe Character Animator's Auto Mouth behaviour maps audio phonemes to mouth layers in the Mouth swap group.

Jack is a golden retriever. His mouth is a muzzle — it moves, but it is not a human mouth. The viseme shapes should:
- Feel natural on an animalistic muzzle
- Be readable at small screen sizes (mobile TikTok)
- NOT over-articulate — Jack is a professional, not a Tex Avery character
- Maintain consistent muzzle fur, size, and placement across all shapes

---

## Viseme Reference Table

| # | Layer Name (PSD) | Phoneme Group | Sound Examples | V1 Required | Description |
|---|----------------|--------------|----------------|-------------|-------------|
| 1 | `Neutral` | Silence / rest | Pauses, breath | ✅ | Mouth closed, flat natural line. Jack's jaw is slightly set. |
| 2 | `Open` | Open vowels | "ah", "aw", "father" | ✅ | Muzzle drops open, wide gap. Jaw drops. Teeth slightly visible. |
| 3 | `Ee` | Front vowels | "ee", "ih", "bit", "beat" | ✅ | Wide horizontal stretch. Teeth visible. Cheeks slightly raised. |
| 4 | `Oh` | Mid-back vowels | "oh", "go", "boat" | ✅ | Rounded opening, slightly oval. Lips form a soft O. |
| 5 | `Ooh` | Back rounded | "oo", "who", "w" onset | ✅ | Pursed forward. Smallest opening, most forward projection. |
| 6 | `M B P` | Bilabial stops | "m", "b", "p" | ✅ | Lips fully pressed together. Muzzle closed, slight tension. |
| 7 | `F V` | Labiodentals | "f", "v" | ✅ | Lower lip tucked slightly under upper teeth. Subtle. |
| 8 | `L` | Alveolar lateral | "l", "la", "let" | ✅ | Mouth slightly open, tongue tip visible at upper teeth. |
| 9 | `S` | Sibilants | "s", "z", "d", "t", "n" | ✅ | Teeth together or near-together, slight gap. |
| 10 | `Smile` | Smile / positive | Warmth in voice | ✅ | Closed mouth, corners up. Not a grin — controlled. |
| 11 | `Smirk` | Smirk (trigger) | Punchline delivery | ✅ | One corner raised, one flat. Knowing expression. Not lip sync — trigger-activated only. |

---

## Mandatory vs Polish

### Mandatory for V1 lip sync (minimum working puppet)
`Neutral`, `Open`, `Ee`, `Oh`, `Ooh`, `M B P`, `F V`, `L`, `S`, `Smile`

Without all 10 of these, Character Animator's Auto Mouth will fall back to Neutral for the missing shapes, producing degraded lip sync.

### Polish-only
`Smirk` — This is not used by Auto Mouth. It is a manually triggered expression override used at specific punchline moments. It visually overrides the mouth group. See Expression System doc.

---

## Muzzle Design Constraints

Jack's muzzle is based on the existing keyframe images. When generating viseme layers:

1. **Same muzzle dimensions across all shapes.** The muzzle width and height should not change — only the opening and internal shapes change.
2. **Same fur colour and texture.** Golden/amber fur, consistent with keyframes.
3. **Same lighting direction.** Light from upper-left, matching existing assets.
4. **Transparent background.** All viseme layers are PNG-32 with alpha. No background.
5. **Same anchor position.** The muzzle should sit at the same Y position relative to the nose in every frame. The nose is fixed; only the lower muzzle and corners move.
6. **Minimalist teeth.** When teeth are visible (Ee, S, L), they should be small, clean, off-white. Not cartoon-white, not detailed. Keep them simple.
7. **No tongue unless strictly needed.** The `L` viseme may show a tongue tip. This should be small and clean — not a large pink tongue flopping out.
8. **No drool, no fangs, no wide gapes.** Jack is a professional.

---

## Viseme Shape Details

### 1. Neutral
- Muzzle completely closed
- Corners of mouth in neutral position
- Very slight natural downward curve (Jack's resting face has a hint of weariness)
- No teeth visible

### 2. Open (Ah)
- Jaw drops — lower muzzle descends
- Width stays consistent
- Upper muzzle stays anchored at nose
- Gap: approximately 30–40% of muzzle height
- Teeth visible: top row faintly, bottom slightly

### 3. Ee
- Horizontal stretch — corners pull outward
- Teeth clearly visible: both rows, closed or near-closed
- Muzzle height reduced slightly
- Most "humanoid-feeling" shape — keep it readable but not over-stretched

### 4. Oh
- Rounded gap, oval shape
- Both lips (upper and lower muzzle) contribute to the rounding
- Width narrows slightly
- No teeth visible usually

### 5. Ooh
- Pursed and projected forward
- Smallest opening of all the open shapes
- Lips push slightly toward viewer
- No teeth

### 6. M B P
- Fully closed — identical to Neutral or nearly so
- Slight additional tension/pressure in the corners
- Can be treated as Neutral with imperceptibly more corner compression

### 7. F V
- Lower lip (lower muzzle edge) tucks under upper teeth
- Subtle shape — the key difference from Neutral is that lower muzzle is slightly drawn in
- Upper teeth visible slightly

### 8. L
- Mouth open approximately 20%
- Tongue tip visible at upper gum/teeth
- Smaller opening than Oh, rounder than Ee

### 9. S
- Teeth together or very close — near-closed like a flat grin
- Slight gap between teeth rows
- Corners natural

### 10. Smile
- Corners up — a controlled, genuine-ish smile
- Mouth closed or near-closed
- Jack smiling is rare and therefore memorable when it occurs

---

## Production Notes

- Generate all 10 mandatory visemes in a single reference sheet session to guarantee consistency.
- Use the same prompt base for all visemes, varying only the mouth shape description.
- QC step: composite all 10 onto a single reference sheet and check alignment before assembling into PSD.
- See `prompts/animation/jack_viseme_sheet_prompts.md` for exact generation prompts.
