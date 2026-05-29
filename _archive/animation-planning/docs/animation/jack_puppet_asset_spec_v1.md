# Jack Puppet Asset Spec v1

**Version:** 1.0  
**Date:** 2026-05-19  
**Status:** Spec — assets not yet generated

---

## Canvas and Color Standards

| Property | Value |
|---------|-------|
| Canvas size (puppet PSD) | 1920 × 1920 px (square, then cropped/composed in Character Animator) |
| Color mode | RGB / 8-bit |
| Color profile | sRGB IEC61966-2.1 |
| Background | Transparent (PNG-32) for all character layers |
| Resolution (PPI) | 72 dpi (screen only, pixel dimensions are what matters) |
| Naming convention | `jack_[category]_[description].png` — lowercase snake_case |

---

## Canonical Reference (existing — DO NOT MODIFY)

| Asset ID | File | Status |
|---------|------|--------|
| `ref_character_master` | `assets/.../01_character/master_refs/jack_character_sheet_master.png` | ✅ Present |
| `keyframe_01` | `public/images/jack_01_forward_calculating.png` | ✅ Present |
| `keyframe_02` | `public/images/jack_02_tie_fix_confident_smirk.png` | ✅ Present |
| `keyframe_03` | `public/images/jack_03_turning_to_monitor.png` | ✅ Present |

These existing keyframes are the **design anchor**. All new generated assets must match their style, fur colour, face proportions, clothing, and lighting direction.

---

## Head and Face Layers

All head layers must be on a transparent background and sized consistently so they composite cleanly in the PSD.

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `head_front_base` | `assets/puppet/layers/head/jack_head_front_base.png` | ✅ | Head + neck, no features, no expression. Used as base layer. |
| `head_three_quarter_base` | `assets/puppet/layers/head/jack_head_three_quarter_base.png` | ✅ | 3/4 angle version. For shots 04–07. |
| `head_front_with_ears` | `assets/puppet/layers/head/jack_head_front_ears.png` | ✅ | Includes floppy ears. Can be merged with base. |
| `head_nose` | `assets/puppet/layers/head/jack_nose.png` | ✅ | Black nose only, as separate layer for slight animation. |

**Design notes:**
- Head should show full face with enough neck to connect cleanly to the torso.
- Ears should be separate or on the head base — do NOT attach to body layer.
- Fur texture and colour must match existing keyframes exactly.

---

## Eye Layers

Eyes are split left/right and open/half/closed to enable blink animation in Character Animator.

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `eye_left_open` | `assets/puppet/layers/eyes/jack_eye_left_open.png` | ✅ | Left eye fully open |
| `eye_right_open` | `assets/puppet/layers/eyes/jack_eye_right_open.png` | ✅ | Right eye fully open |
| `eye_left_half` | `assets/puppet/layers/eyes/jack_eye_left_half.png` | ✅ | Left eye half-closed (suspicious/paranoid) |
| `eye_right_half` | `assets/puppet/layers/eyes/jack_eye_right_half.png` | ✅ | Right eye half-closed |
| `eye_left_closed` | `assets/puppet/layers/eyes/jack_eye_left_closed.png` | ✅ | Left eye fully closed (blink) |
| `eye_right_closed` | `assets/puppet/layers/eyes/jack_eye_right_closed.png` | ✅ | Right eye fully closed (blink) |
| `pupil_left` | `assets/puppet/layers/eyes/jack_pupil_left.png` | ✅ | Left pupil as separate warp layer |
| `pupil_right` | `assets/puppet/layers/eyes/jack_pupil_right.png` | ✅ | Right pupil as separate warp layer |

**Design notes:**
- Pupils on separate layers allow Character Animator's eye-tracking warp behaviour.
- Eyes should sit on a transparent background and align to a consistent facial landmark grid.

---

## Eyebrow Layers

Eyebrows are the primary emotional signal for Jack. Four states minimum for V1.

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `eyebrow_left_neutral` | `assets/puppet/layers/eyebrows/jack_eyebrow_left_neutral.png` | ✅ | Default resting position |
| `eyebrow_right_neutral` | `assets/puppet/layers/eyebrows/jack_eyebrow_right_neutral.png` | ✅ | |
| `eyebrow_left_concerned` | `assets/puppet/layers/eyebrows/jack_eyebrow_left_concerned.png` | ✅ | Inner brow raised, furrowed — used shots 01–03 |
| `eyebrow_right_concerned` | `assets/puppet/layers/eyebrows/jack_eyebrow_right_concerned.png` | ✅ | |
| `eyebrow_left_thinking` | `assets/puppet/layers/eyebrows/jack_eyebrow_left_thinking.png` | ✅ | One brow slightly raised, calculating look |
| `eyebrow_right_thinking` | `assets/puppet/layers/eyebrows/jack_eyebrow_right_thinking.png` | ✅ | |
| `eyebrow_left_smug` | `assets/puppet/layers/eyebrows/jack_eyebrow_left_smug.png` | ✅ | Confident arch — used shots 04–06 |
| `eyebrow_right_smug` | `assets/puppet/layers/eyebrows/jack_eyebrow_right_smug.png` | ✅ | |
| `eyebrow_left_paranoid` | `assets/puppet/layers/eyebrows/jack_eyebrow_left_paranoid.png` | ❌ optional | Twitchy raised brow — polish |
| `eyebrow_right_paranoid` | `assets/puppet/layers/eyebrows/jack_eyebrow_right_paranoid.png` | ❌ optional | |

---

## Mouth / Viseme Layers

All mouth layers go inside a single `Mouth` group in the PSD. Character Animator's lip sync swaps between them.

| Asset ID | File Path | V1 Required | Viseme |
|---------|-----------|-------------|--------|
| `mouth_neutral` | `assets/puppet/layers/mouth/jack_mouth_neutral.png` | ✅ | Rest / closed |
| `mouth_smile` | `assets/puppet/layers/mouth/jack_mouth_smile.png` | ✅ | Subtle closed smile |
| `mouth_smirk` | `assets/puppet/layers/mouth/jack_mouth_smirk.png` | ✅ | One-sided confident smirk |
| `mouth_ah` | `assets/puppet/layers/mouth/jack_mouth_ah.png` | ✅ | Open — ah/aw sounds |
| `mouth_ee` | `assets/puppet/layers/mouth/jack_mouth_ee.png` | ✅ | Wide horizontal — ee/ih sounds |
| `mouth_oh` | `assets/puppet/layers/mouth/jack_mouth_oh.png` | ✅ | Rounded open — oh sounds |
| `mouth_oo_w` | `assets/puppet/layers/mouth/jack_mouth_oo_w.png` | ✅ | Pursed — oo/w sounds |
| `mouth_mbp` | `assets/puppet/layers/mouth/jack_mouth_mbp.png` | ✅ | Lips together — m/b/p sounds |
| `mouth_fv` | `assets/puppet/layers/mouth/jack_mouth_fv.png` | ✅ | Lower lip under teeth — f/v sounds |
| `mouth_l` | `assets/puppet/layers/mouth/jack_mouth_l.png` | ✅ | Tongue behind teeth — l sounds |
| `mouth_s_dtn` | `assets/puppet/layers/mouth/jack_mouth_s_dtn.png` | ✅ | Teeth together — s/d/t/n sounds |

**Design notes:**
- All mouth layers must be identically positioned relative to the face, same size, same angle.
- Background transparent — only the mouth/muzzle area.
- Muzzle fur colour and texture must match the head base layer exactly.
- Keep teeth minimalist: small, white, tasteful. Do not overrender teeth.

---

## Body Layers

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `body_torso_front` | `assets/puppet/layers/body/jack_torso_front.png` | ✅ | Black suit jacket, white shirt, visible from neck to waist |
| `body_torso_three_quarter` | `assets/puppet/layers/body/jack_torso_three_quarter.png` | ✅ | Same but 3/4 angle |
| `arm_left_resting` | `assets/puppet/layers/body/jack_arm_left_resting.png` | ✅ | Left arm resting on chair arm |
| `arm_right_resting` | `assets/puppet/layers/body/jack_arm_right_resting.png` | ✅ | Right arm resting |
| `arm_right_tie_fix` | `assets/puppet/layers/body/jack_arm_right_tie_fix.png` | ✅ | Right arm raised with hand at tie |
| `hand_right_tie_grip` | `assets/puppet/layers/body/jack_hand_right_tie_grip.png` | ✅ | Hand grasping tie knot |
| `tie_straight` | `assets/puppet/layers/body/jack_tie_straight.png` | ✅ | Black skinny tie, straight position |
| `tie_adjusted` | `assets/puppet/layers/body/jack_tie_adjusted.png` | ❌ optional | Tie slightly adjusted, subtle variation |
| `tie_askew` | `assets/puppet/layers/body/jack_tie_askew.png` | ❌ optional | Slightly crooked tie — paranoid moments |

**Design notes:**
- Tie must be a separate layer from the shirt so it can be physics-animated in Character Animator.
- Arms must align cleanly to the torso at the shoulder joint.
- Include enough overlap at joints so warp handles don't reveal gaps.

---

## Environment / Background Layers

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `office_background_clean` | `assets/puppet/layers/environment/office_background_clean.png` | ✅ | Full office background, no character. Window, bookshelves, wall. |
| `office_chair` | `assets/puppet/layers/environment/office_chair.png` | ✅ | Office chair layer, Jack sits in front of this |
| `desk_foreground` | `assets/puppet/layers/environment/desk_foreground.png` | ❌ optional | Desk surface in foreground for depth |
| `monitor_blank` | `assets/puppet/layers/environment/monitor_blank.png` | ❌ optional | Monitor with blank/dark screen |
| `crm_monitor_closeup` | `assets/puppet/layers/environment/crm_monitor_closeup.png` | ❌ optional | CRM screen insert — beat 3 asset. See docs/missing_assets.md |
| `desk_mug` | `assets/puppet/layers/environment/desk_mug.png` | ❌ optional | Mug prop on desk |
| `desk_nameplate` | `assets/puppet/layers/environment/desk_nameplate.png` | ❌ optional | "Jack" nameplate prop |

---

## Reference Sheets (for QC and generation guidance)

| Asset ID | File Path | V1 Required | Notes |
|---------|-----------|-------------|-------|
| `ref_expression_sheet` | `assets/puppet/refs/jack_expression_reference_sheet.png` | ✅ | All 8 expressions in one sheet |
| `ref_viseme_sheet` | `assets/puppet/refs/jack_viseme_reference_sheet.png` | ✅ | All 11 mouth shapes in one sheet |
| `ref_body_poses` | `assets/puppet/refs/jack_body_pose_reference_sheet.png` | ✅ | All body/arm/tie poses |

---

## V1 Minimum Set (absolute minimum to rig and animate)

To produce a working Character Animator puppet capable of lip sync, you need at minimum:
1. `head_front_base` — the head canvas
2. All 11 mouth viseme layers
3. `eye_left_open`, `eye_right_open`, `eye_left_closed`, `eye_right_closed`
4. `eyebrow_left_neutral`, `eyebrow_right_neutral`, `eyebrow_left_concerned`, `eyebrow_right_concerned`
5. `body_torso_front`
6. `tie_straight`
7. `office_background_clean`
8. `office_chair`

Everything else adds fidelity but is not a hard blocker.
