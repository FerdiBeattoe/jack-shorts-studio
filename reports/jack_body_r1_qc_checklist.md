# Jack Body R1 QC Checklist

Date: 2026-05-19

## Batch Scope

Staged folder:

`assets/puppet/layers_staging/body_r1/`

Reference source:

`assets/puppet/refs/jack_body_pose_reference_sheet.png`

Contact sheet:

`assets/puppet/layers_staging/body_r1/body_r1_contact_sheet.png`

Active assets must not be overwritten during this QC pass.

## Global Batch Checks

- [ ] The staged files visually match Jack's accepted body pose reference sheet.
- [ ] The style is 2D adult-animation with clean linework and subtle cel shading.
- [ ] The clothing is Jack's black suit jacket, white shirt, and black skinny tie.
- [ ] Paws are simple cartoon dog paws, not human hands.
- [ ] All character/body-part layers have real transparency.
- [ ] No file has a baked checkerboard background.
- [ ] No file has a grey, white, beige, or office background.
- [ ] No file contains a chair, desk, monitor, scene, text, watermark, or label.
- [ ] No file looks like a crude vector placeholder or generic suit icon.
- [ ] Body parts are suitable as cuttable puppet layers with useful overlap for rigging.
- [ ] Tie is black, skinny, visually Jack-matching, and separate from the torso.
- [ ] PSD assembly remains paused.

## Asset Decisions

| Asset | Looks like Jack? | Real transparency? | Aligns with body pose sheet? | Rig-usable? | No baked background? | Not placeholder? | PASS/FAIL | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `jack_torso_front.png` |  |  |  |  |  |  |  |  |
| `jack_torso_three_quarter.png` |  |  |  |  |  |  |  |  |
| `jack_arm_left_resting.png` |  |  |  |  |  |  |  |  |
| `jack_arm_right_resting.png` |  |  |  |  |  |  |  |  |
| `jack_arm_right_tie_fix.png` |  |  |  |  |  |  |  |  |
| `jack_tie_straight.png` |  |  |  |  |  |  |  |  |

## Per-Asset Requirements

### `jack_torso_front.png`

- [ ] Front-facing torso only.
- [ ] No head.
- [ ] No chair or background.
- [ ] Suit/shirt silhouette matches Jack's accepted front body design.
- [ ] Leaves room for the separate tie layer.
- [ ] Shoulder area can accept separate arm layers.

Decision: PASS / FAIL

Notes:

### `jack_torso_three_quarter.png`

- [ ] 3/4 torso angle matches the accepted seated 3/4/tie-adjustment references.
- [ ] No head.
- [ ] No chair or background.
- [ ] Lapels, shirt, and torso perspective are coherent.
- [ ] Leaves room for separate tie and arm layers.

Decision: PASS / FAIL

Notes:

### `jack_arm_left_resting.png`

- [ ] Left resting arm only.
- [ ] Black sleeve and white cuff match Jack.
- [ ] Paw is a simple cartoon dog paw.
- [ ] Shoulder/wrist overlap is useful for puppet rigging.
- [ ] No chair is included.

Decision: PASS / FAIL

Notes:

### `jack_arm_right_resting.png`

- [ ] Right resting arm only.
- [ ] Black sleeve and white cuff match Jack.
- [ ] Paw is a simple cartoon dog paw.
- [ ] Shoulder/wrist overlap is useful for puppet rigging.
- [ ] No chair is included.

Decision: PASS / FAIL

Notes:

### `jack_arm_right_tie_fix.png`

- [ ] Right raised arm only.
- [ ] Gesture matches the accepted tie-adjusting pose.
- [ ] Paw is a simple cartoon dog paw, not a human hand.
- [ ] Paw position can align with the tie knot/collar area.
- [ ] No torso, head, chair, or full tie is included.
- [ ] Shoulder and elbow overlap are useful for puppet rigging.

Decision: PASS / FAIL

Notes:

### `jack_tie_straight.png`

- [ ] Tie is separate from shirt/torso.
- [ ] Tie is black and skinny.
- [ ] Knot is small and professional.
- [ ] Shape matches Jack's accepted body pose sheet.
- [ ] Transparent PNG with no baked background.
- [ ] Looks like finished puppet art, not a flat generic icon.

Decision: PASS / FAIL

Notes:

## Final Batch Decision

Batch R1 status: PASS / FAIL

Reason:

Approved by:

Date:
