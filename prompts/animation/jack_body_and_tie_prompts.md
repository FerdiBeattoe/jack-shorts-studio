# Jack Body and Tie Prompts

**Version:** 1.0  
**Date:** 2026-05-19  
**Purpose:** Prompts for generating Jack's body, arm, hand, and tie puppet layers.

---

## Base Body Description

Include this in every body prompt:

```
Humanoid golden retriever character, adult male. Seated in a modern office chair.
No head — torso and arms only (head is a separate compositing layer).
Clothing: slim-fit black suit jacket, white dress shirt, black skinny tie.
Golden/amber fur on visible skin (hands, wrists where shirt cuff rides up).
Flat 2D illustration style, clean linework, cel shading.
Soft lighting from upper-left. Transparent background.
Suit jacket is professional but slightly lived-in — this is not a brand-new suit.
```

---

## Prompt B1 — Resting Arms (default body position)

**File target:** `assets/puppet/layers/body/jack_arm_left_resting.png`  
**File target:** `assets/puppet/layers/body/jack_arm_right_resting.png`

```
[BASE BODY]
Body position: RESTING ARMS.
Both arms resting on the armrests of an office chair.
Arms relaxed — slightly outward from the body, elbows on armrests,
forearms horizontal, hands loosely resting palms-down or slightly curled.

Generate LEFT ARM and RIGHT ARM as separate files 
(the arm that appears on viewer's left and viewer's right respectively).

Shoulder should be included with enough overlap to composite against the torso.
Black suit jacket sleeve, white shirt cuff just visible at wrist.
Hands: golden fur, relaxed, not a fist, not spread wide.
```

---

## Prompt B2 — Tie-Fix Pose (key action)

**File target:** `assets/puppet/layers/body/jack_arm_right_tie_fix.png`

```
[BASE BODY]
Body position: TIE-FIX.
Right arm only. Arm raised to chest level — elbow bent at approximately 90 degrees,
forearm pointing upward, hand at sternum level.

Hand is grasping a black skinny tie knot at the collar.
This is a deliberate, unhurried gesture — the motion of a man who has decided 
to reassert control by adjusting his tie. It is not a nervous gesture. 
It is a power gesture performed at a measured pace.

Show the arm from shoulder to fingertips. Include enough shoulder 
to composite against the torso.
Black suit jacket sleeve, white shirt cuff slightly raised from the wrist action.
Hand: golden fur, fingers wrapped around the tie knot.

Transparent background.
```

---

## Prompt B3 — Hand Detail: Tie Grip

**File target:** `assets/puppet/layers/body/jack_hand_right_tie_grip.png`

```
Close-up of a humanoid golden retriever right hand gripping a black skinny tie knot.
Golden/amber fur on the back of the hand. Standard humanoid hand anatomy with 
slightly stylised proportions — four fingers and a thumb, clean and readable.

The grip is deliberate and controlled — thumb and first two fingers around 
the narrow part of the tie knot, adjusting it with precision.

Flat 2D illustration, clean linework, transparent background.
This is a close-up detail layer that may be used as an insert shot or 
composited with the arm layer.
```

---

## Prompt B4 — Tie: Straight Position

**File target:** `assets/puppet/layers/body/jack_tie_straight.png`

```
A single black slim/skinny necktie isolated on transparent background.
No character, no shirt — just the tie.

Full length of the tie: from knot at the top down to the pointed tip, 
approximately 300–350px in height at final rendering scale.

Knot: a standard, slightly off-centre four-in-hand knot — small and professional.
The tie is NOT perfectly centred — it is ever-so-slightly to one side, 
suggesting a man who straightened it but didn't quite achieve perfection.

Material: black with a very subtle sheen — silk-adjacent. Not flat matte, 
not mirror-shiny. A small, tasteful pattern may be implied (very subtle diagonal 
texture), but keep it clean and business-appropriate.

Flat 2D illustration style, clean linework. Transparent background.
```

---

## Prompt B5 — Tie: Askew (optional paranoid variant)

**File target:** `assets/puppet/layers/body/jack_tie_askew.png`

```
Same as Prompt B4 (black slim tie, transparent background, same style),
but the tie is notably off-centre — rotated approximately 10–15 degrees 
to one side, clearly displaced from a centred position.

This variant is used for moments of increased internal stress — 
when Jack's professional composure is at its thinnest.

The displacement is visible but not comedically extreme. 
This is a man who started with a straight tie and it has drifted.
```

---

## Prompt B6 — Leaning Forward (torso variant)

**File target:** `assets/puppet/layers/body/jack_torso_leaning_forward.png`

```
[BASE BODY]
Body position: LEANING FORWARD.
Torso only (no head). Suit jacket, white shirt, tie.
Body inclined approximately 15–20 degrees forward from vertical — 
leaning toward the viewer (or toward a desk/monitor).
This is the "calculating something important" posture.

Arms are slightly forward as well — elbows may rest on desk or forward on chair arms.
Subtle forward lean, not dramatic. Professional but engaged.

Transparent background. Same style and lighting as other body layers.
```

---

## Prompt B7 — Sitting Back (torso variant)

**File target:** `assets/puppet/layers/body/jack_torso_sitting_back.png`

```
[BASE BODY]
Body position: SITTING BACK.
Torso only (no head). Suit jacket, white shirt, tie.
Body inclined approximately 10–15 degrees backward — leaning back in the chair.
The confidence posture. This is the post-tie-fix position.

The tie hangs at a slight angle as a result of the lean.
The jacket lapels fall naturally. Slight chest out — not dramatically, 
just the natural shape of sitting back.

This posture should read as "I have reassessed the situation 
and I have decided I am comfortable with it."

Transparent background. Same style and lighting.
```

---

## Prompt B8 — Turning Toward Monitor (body variant)

**File target:** `assets/puppet/layers/body/jack_torso_turning_monitor.png`

```
[BASE BODY]
Body position: TURNING TOWARD MONITOR.
Torso only (no head). 3/4 angle — body rotating to character's right 
(viewer's left), as if turning toward a monitor on the right side of the desk.

Right shoulder turned forward, left shoulder slightly back.
Arms relaxed but transitioning — right arm may be moving toward the keyboard 
or resting on the desk surface.

This is the "I have finished narrating, I am returning to the work" posture.
(Whether the work is actual work or checking the CRM again is left ambiguous.)

Transparent background. Same style.
```

---

## Body Pose Reference Sheet Prompt

**File target:** `assets/puppet/refs/jack_body_pose_reference_sheet.png`

```
A professional character body pose reference sheet for an animated character.
Character: humanoid golden retriever torso, black suit, white shirt, black tie.
No head in any panel. Transparent backgrounds per panel, assembled on light grey sheet.

Layout: 3×2 grid, 6 poses.
Panel labels:
1. Arms Resting (default)
2. Tie-Fix (arm raised)
3. Leaning Forward
4. Sitting Back
5. Turning Toward Monitor (3/4)
6. Arms Resting 3/4 View

Each panel same size. Clean, professional character reference sheet format.
Label each panel. Consistent style and lighting across all panels.
```

---

## Consistency Checklist for Body Layers

After generating body assets:
- [ ] All layers have transparent backgrounds
- [ ] Fur colour on hands/wrists matches head layers (golden/amber)
- [ ] Suit jacket colour is consistent (true black, same across all poses)
- [ ] Tie is consistent in colour and material treatment
- [ ] Shoulder position allows clean compositing with the head layer
- [ ] Style (linework, shading) is consistent with head and environment layers
- [ ] Lighting direction is consistent (upper-left)
