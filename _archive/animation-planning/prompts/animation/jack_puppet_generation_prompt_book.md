# Jack Puppet Generation Prompt Book

**Version:** 1.0  
**Date:** 2026-05-19  
**Purpose:** Image generation prompts for all Jack puppet layers and reference sheets.

---

## Design Anchor

Every prompt in this book must preserve the canonical Jack design. The ground truth is:
- `assets/.../01_character/master_refs/jack_character_sheet_master.png`
- `public/images/jack_01_forward_calculating.png`
- `public/images/jack_02_tie_fix_confident_smirk.png`
- `public/images/jack_03_turning_to_monitor.png`

**Jack's core design:**
> Humanoid golden retriever, adult male, account manager. Golden/amber fur. Black round nose. Dark expressive eyebrows — thick, communicative. Black slim-fit suit jacket. White dress shirt. Black skinny tie, slightly askew. Mid-30s energy. Professional demeanour with visible subtext. Seated at a modern office desk. Stylised 2D illustration style, clean linework, soft shading.

All new assets must match this description unless the prompt explicitly calls out a variation.

---

## Prompt Usage Rules

1. Always start with the base character description above.
2. Specify transparent background where the asset needs alpha.
3. Specify consistent lighting: **soft, even lighting from upper-left**.
4. Specify the view angle explicitly: **front-facing**, **3/4 view**, **profile**, etc.
5. Specify what should NOT be in the frame.
6. Do not request extreme expressions — Jack is a professional.
7. After generation, compare against keyframe assets for colour/style match.

---

## Prompt 01 — Canonical Head Front (base layer)

**File target:** `assets/puppet/layers/head/jack_head_front_base.png`

```
Humanoid golden retriever, adult male character, front-facing portrait view. 
Head and neck only, no body. Clean transparent background.

Character design: golden/amber fur, black round nose, dark thick expressive eyebrows 
(neutral resting position), dark almond-shaped eyes with warm golden irises. 
Floppy golden ears. Slight anthropomorphic muzzle — readable but not exaggerated.

Style: flat stylised 2D illustration, clean vector-like linework, soft cel shading. 
Consistent with a professional animated character — not a cartoon dog, not photorealistic. 
Think: professional business animated series.

Lighting: soft from upper-left. No dramatic shadows. Clean rendering suitable for 
compositing as a puppet layer.

Mood: neutral expression. No smile, no frown. Professional composure.

Do not include: body, clothing, background, any UI elements.
```

---

## Prompt 02 — Head 3/4 View (base layer)

**File target:** `assets/puppet/layers/head/jack_head_three_quarter_base.png`

```
Same character as Prompt 01: humanoid golden retriever, adult male, flat 2D illustration style.

3/4 angle view — head turned approximately 30–40 degrees to his right 
(viewer's left). Slight rotation showing right ear more prominently.

Head and neck only, transparent background. Neutral expression. 
Same lighting as front view (soft upper-left). Same fur colour, same linework style.

This is for the "turning toward monitor" shot where Jack pivots his attention.

Do not include: body, clothing, background.
```

---

## Prompt 03 — Seated Body Front (torso layer)

**File target:** `assets/puppet/layers/body/jack_torso_front.png`

```
Humanoid golden retriever seated in a modern office chair. 
Torso only — from shoulders to mid-thigh. No head (will be composited separately).

Clothing: slim-fit black suit jacket, white dress shirt with top button visible, 
black skinny tie hanging straight. Jacket fits well but slightly lived-in.

View: front-facing, seated upright. Arms resting on chair armrests.

Style: same flat 2D illustration as character head prompts. Clean linework, 
cel shading, professional animation series aesthetic. Transparent background.

Lighting: soft from upper-left, matching head layer.

Do not include: head or neck, background, desk, other objects.
```

---

## Prompt 04 — Seated Body 3/4 View

**File target:** `assets/puppet/layers/body/jack_torso_three_quarter.png`

```
Same as Prompt 03 (torso only, no head, transparent background), but at 3/4 angle —
body turned approximately 30 degrees to his right (viewer's left).

Right shoulder slightly forward. Suit jacket shows more of the right lapel.
Tie hangs naturally at this angle.

Same clothing, same style, same lighting as Prompt 03.
```

---

## Prompt 05 — Arm and Hand: Resting Position

**File target:** `assets/puppet/layers/body/jack_arm_right_resting.png`

```
Humanoid golden retriever right arm only. Golden fur, black suit jacket sleeve, 
white shirt cuff peeking at wrist. Hand resting relaxed on an office chair armrest.

Front-facing view. Arm from shoulder joint to fingertips. 
Transparent background. Same 2D illustration style, soft shading.

Hand: relaxed, slightly closed, natural resting position. Not a fist, not waving.
```

---

## Prompt 06 — Arm and Hand: Tie-Fix Pose

**File target:** `assets/puppet/layers/body/jack_arm_right_tie_fix.png`

```
Humanoid golden retriever right arm raised to chest height. 
Hand grasping a black skinny tie knot at the collar.

Arm is lifted, elbow bent, hand at sternum level grasping tie. 
This is a deliberate, controlled gesture — adjusting the tie with one hand.
Not a nervous gesture — a power gesture. Slow and intentional.

Golden fur, black suit jacket sleeve. Transparent background. 
Same style as other arm layers.
```

---

## Prompt 07 — Tie Layer (separate physics layer)

**File target:** `assets/puppet/layers/body/jack_tie_straight.png`

```
A single black slim/skinny necktie on transparent background. 
No character, no shirt — just the tie.

The tie hangs straight down from collar level to below the waist (full length).
The knot at the top is a standard four-in-hand or half-Windsor — small and professional.
The tie has a subtle sheen — not completely flat black, slight silk/satin quality.

The tie is slightly off-centre — characteristic of a man who straightened it 
but didn't quite get it perfect.

Style: same flat 2D illustration, clean linework.
```

---

## Prompt 08 — Clean Office Background

**File target:** `assets/puppet/layers/environment/office_background_clean.png`

```
A modern corporate office background. No characters.

Elements to include: large window with city view (soft, slightly blurred exterior), 
modern shelving or bookcase against one wall, neutral-coloured walls (warm off-white 
or soft grey), diffuse natural lighting from the window, indoor plants optional.

View: straight-on perspective, as if looking directly at the back wall of the office.
Aspect ratio: approximately portrait (1080 × 1920) or wider to allow cropping.

Style: flat 2D illustration with some atmospheric depth — 
not photorealistic, not cartoon-simplified. Professional animated show aesthetic.
Colour temperature: warm slightly — office lighting with daylight accent.

Do not include: people, characters, desk/foreground elements 
(those are separate layers), screens showing visible content.
```

---

## How to Use This Prompt Book

1. Read the relevant prompt for the asset you need.
2. Use your preferred image generation tool (Midjourney, DALL-E 3, Stable Diffusion, Firefly).
3. Compare the output against the existing keyframes in `public/images/`.
4. If the style doesn't match, iterate: add "match this character's style", 
   reference the existing keyframes as style anchors if the tool supports it.
5. Save to the target file path specified in each prompt.
6. Run `node scripts/validate-jack-puppet-pack.mjs` to check completeness.

---

## Style Consistency Checklist

Before accepting any generated asset:
- [ ] Fur colour matches `jack_01_forward_calculating.png` (golden/amber)
- [ ] Linework weight matches existing assets (clean, consistent)
- [ ] Shading style matches (flat cel, not gradient/painterly)
- [ ] Background is transparent where required
- [ ] No added accessories not in the original design
- [ ] Lighting direction matches (upper-left)
- [ ] Proportions are consistent with the character sheet master
