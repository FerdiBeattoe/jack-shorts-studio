# Jack Body Rebuild Batch R1 Prompt

Date: 2026-05-19

## Batch Goal

Create production-quality body puppet layer assets for Jack only in staging.

Use `assets/puppet/refs/jack_body_pose_reference_sheet.png` as the primary accepted design source. Match its adult-animation style, body proportions, suit fit, simple dog paws, black suit jacket, white shirt, and black skinny tie.

Do not use the existing active body PNGs as visual references. They failed visual QC and are crude placeholders.

## Output Folder

Save generated files only to:

`assets/puppet/layers_staging/body_r1/`

Do not overwrite files in:

`assets/puppet/layers/body/`

## Required Files

- `assets/puppet/layers_staging/body_r1/jack_torso_front.png`
- `assets/puppet/layers_staging/body_r1/jack_torso_three_quarter.png`
- `assets/puppet/layers_staging/body_r1/jack_arm_left_resting.png`
- `assets/puppet/layers_staging/body_r1/jack_arm_right_resting.png`
- `assets/puppet/layers_staging/body_r1/jack_arm_right_tie_fix.png`
- `assets/puppet/layers_staging/body_r1/jack_tie_straight.png`

## Global Style Lock

Use this style for every asset in this batch:

Production-quality 2D adult-animation puppet layer of Jack, a humanoid golden retriever adult male account manager. Match the accepted Jack body pose reference sheet exactly in design language: clean black linework, flat colors with subtle cel shading, warm golden/amber fur, black slim-fit suit jacket, white dress shirt, black skinny tie, slightly tired professional posture. Use simple cartoon dog paws, not human hands. Paws should be rounded golden dog paws with simple finger/toe separation only where needed. The clothing should feel like the same black suit and white shirt shown in the accepted body pose sheet, not a generic suit icon.

All assets must be isolated cuttable puppet layers on a transparent PNG background. No checkerboard background. No grey or white baked background. No office scene. No chair. No desk. No text. No labels. No props except the requested body part or tie. No crude vector placeholder shapes. No generic suit icons. No photorealism. No 3D render. No anime style. No painterly texture. No extra accessories.

Lighting: soft, even, from upper-left, consistent with the accepted reference sheets.

Canvas guidance:

- Torso and arm layers: square transparent canvas, preferably 1024 x 1024 px.
- Tie layer: square transparent canvas, preferably 1024 x 1024 px.
- Keep enough transparent padding and overlap at shoulders/wrists/tie knot for puppet rigging.
- Do not crop the artwork tightly at joints.

## Asset Prompts

### 1. Front Torso

Target file:

`assets/puppet/layers_staging/body_r1/jack_torso_front.png`

Prompt:

Create Jack's front-facing torso puppet layer only, matching `jack_body_pose_reference_sheet.png`, especially the seated/front and standing/front suit design. No head, no neck/head fur, no arms as separate long limbs, no chair, no background.

The layer should include the upper body clothing from shoulders to upper hips: black slim-fit suit jacket, white dress shirt, collar, visible shirt opening, and enough shoulder/chest structure to connect cleanly to separate arm layers. The black skinny tie may be represented only as collar/knot alignment guidance if needed, but the final tie should remain a separate layer. Keep the center of the shirt clear so `jack_tie_straight.png` can be composited over it.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic suit icon.

### 2. Three-Quarter Torso

Target file:

`assets/puppet/layers_staging/body_r1/jack_torso_three_quarter.png`

Prompt:

Create Jack's torso puppet layer at a seated 3/4 angle, matching the accepted body pose reference sheet panels for seated 3/4 and seated tie-adjustment. No head, no chair, no background, no desk, no full arms.

The body is turned about 30 degrees to Jack's right, viewer's left. Show black slim-fit suit jacket, white dress shirt, collar, and natural jacket lapel overlap at this angle. Keep proportions consistent with the accepted body pose sheet. Leave room for a separate black skinny tie layer and separate arm layers.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic suit icon.

### 3. Left Arm Resting

Target file:

`assets/puppet/layers_staging/body_r1/jack_arm_left_resting.png`

Prompt:

Create Jack's left arm resting puppet layer only, matching the accepted body pose sheet seated front pose. The arm should be suitable for compositing over/near the front torso. Include black suit sleeve, small white shirt cuff, and a simple golden cartoon dog paw resting low as if on a chair arm or lap. Do not include the chair itself.

Use Jack's left arm from shoulder overlap to paw. The paw must be a simple dog paw, not a human hand. It should look like the same rounded golden paw shapes in the accepted body pose sheet, with simple clean linework and subtle shading.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic sleeve icon.

### 4. Right Arm Resting

Target file:

`assets/puppet/layers_staging/body_r1/jack_arm_right_resting.png`

Prompt:

Create Jack's right arm resting puppet layer only, matching the accepted body pose sheet seated front pose. The arm should be suitable for compositing over/near the front torso. Include black suit sleeve, small white shirt cuff, and a simple golden cartoon dog paw resting low as if on a chair arm or lap. Do not include the chair itself.

Use Jack's right arm from shoulder overlap to paw. The paw must be a simple dog paw, not a human hand. It should look like the same rounded golden paw shapes in the accepted body pose sheet, with simple clean linework and subtle shading.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic sleeve icon.

### 5. Right Arm Tie-Fix

Target file:

`assets/puppet/layers_staging/body_r1/jack_arm_right_tie_fix.png`

Prompt:

Create Jack's right arm tie-fix puppet layer only, matching the accepted body pose sheet panel where Jack adjusts his tie. Include black suit sleeve, small white shirt cuff, golden retriever forearm/paw, and the paw grasping near the tie knot position. The gesture should be deliberate and controlled, not nervous. Do not include head, torso, chair, background, or the full tie as a separate long object.

The paw must be a simple cartoon dog paw, not a human hand. It should read clearly as a dog paw gripping or pinching the tie knot area with minimal finger detail. Include enough shoulder and elbow overlap for puppet rigging.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic bent-arm icon.

### 6. Straight Tie

Target file:

`assets/puppet/layers_staging/body_r1/jack_tie_straight.png`

Prompt:

Create Jack's separate black skinny tie puppet layer only, matching the accepted body pose sheet. The tie should be a slim black necktie with a small knot at the top and a long narrow body hanging straight down. It should have subtle cel-shaded shape and clean black outline, not a flat generic icon.

The tie should be suitable as an independent Character Animator physics layer, with transparent padding around it and enough top/knot detail to align to Jack's shirt collar. Do not include shirt, suit, torso, paws, chair, background, text, or any other object.

Transparent PNG. Production-quality Jack-matching 2D adult-animation style. No checkerboard. No baked background. No generic tie icon.

## Negative Prompt / Reject Conditions

Reject any output that has:

- A checkerboard background baked into the pixels.
- A white, grey, beige, or office background.
- A chair, desk, monitor, or office scene.
- Text, labels, filenames, captions, signatures, or watermarks.
- Human hands instead of simple cartoon dog paws.
- Crude vector placeholder shapes.
- Generic business suit icon styling.
- Photorealistic fabric or 3D-rendered clothing.
- Cropped joints that cannot be rigged.
- A merged full-body character when a single puppet layer was requested.
- A tie merged into torso when the tie should be separate.

## QC Before Activation

After files are generated in staging:

1. Run `node scripts/build-body-r1-contact-sheet.mjs`.
2. Review `assets/puppet/layers_staging/body_r1/body_r1_contact_sheet.png`.
3. Complete `reports/jack_body_r1_qc_checklist.md`.
4. Only after all six staged files pass visual QC should any replacement of active body assets be considered.
