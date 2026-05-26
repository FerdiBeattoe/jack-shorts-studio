# Jack Puppet Asset Visual Audit v1

Date: 2026-05-19

## Executive Decision

Structural validation passed, but visual QC failed.

`node scripts\validate-jack-puppet-pack.mjs` exits successfully because every V1-required filename exists. That validator only proves the manifest paths resolve. It does not verify transparent puppet quality, style match, production composition, baked backgrounds, or whether an image is real artwork.

PSD assembly must remain paused. The current layer set contains too many crude placeholders and technically invalid files to assemble into a useful Character Animator puppet. Continuing would only bake bad sources into a PSD and create cleanup work.

## Validator Result

Command:

```powershell
node scripts\validate-jack-puppet-pack.mjs
```

Result:

| Check | Result |
| --- | --- |
| Exit code | 0 |
| Present assets | 44 / 52 |
| Missing V1-required assets | 0 |
| Missing optional assets | 8 |
| Validator conclusion | V1 READY |
| Visual audit conclusion | NOT PRODUCTION READY |

Recorded but not accepted as production approval.

## Audit Scope

Audited every PNG under:

- `assets/puppet/layers/head`
- `assets/puppet/layers/eyes`
- `assets/puppet/layers/eyebrows`
- `assets/puppet/layers/mouth`
- `assets/puppet/layers/body`
- `assets/puppet/layers/environment`

Required references reviewed:

- `manifests/jack_puppet_manifest_v1.json`
- `scripts/validate-jack-puppet-pack.mjs`
- `docs/animation/`
- `prompts/animation/jack_puppet_generation_prompt_book.md`
- `assets/puppet/refs/`
- `assets/puppet/layers/`
- `assets/puppet/jack_character_animator_v1_layout_preview.png`

## Totals

| Classification | Count |
| --- | ---: |
| KEEP_REFERENCE | 2 |
| KEEP_TEMPORARY | 6 |
| REJECT_PLACEHOLDER | 21 |
| REJECT_TECHNICAL | 8 |
| REBUILD_REQUIRED | 0 |
| Total audited PNGs | 37 |

Rejected assets copied to:

`assets/puppet/_rejected_placeholder_assets_v1/`

## Still Usable

These are not production-approved final layers. They are the only assets worth preserving as current working references or temporary layout aids.

| Asset | Classification | Reason |
| --- | --- | --- |
| `head/jack_head_front_base.png` | KEEP_REFERENCE | Transparent, style-adjacent, useful as a face reference. Still needs approval before production use. |
| `head/jack_head_three_quarter_base.png` | KEEP_REFERENCE | Transparent and visually coherent, but expression/pose should be reviewed against the canonical sheet before final rigging. |
| `eyes/jack_eye_left_open.png` | KEEP_TEMPORARY | Transparent and usable for alignment tests only. Needs final visual approval with rebuilt head/face. |
| `eyes/jack_eye_right_open.png` | KEEP_TEMPORARY | Transparent and usable for alignment tests only. Needs final visual approval with rebuilt head/face. |
| `eyes/jack_eye_left_half.png` | KEEP_TEMPORARY | Transparent and style-adjacent, but not production approved. |
| `eyes/jack_eye_right_half.png` | KEEP_TEMPORARY | Transparent and style-adjacent, but not production approved. |
| `eyes/jack_eye_left_closed.png` | KEEP_TEMPORARY | Transparent and style-adjacent, but not production approved. |
| `eyes/jack_eye_right_closed.png` | KEEP_TEMPORARY | Transparent and style-adjacent, but not production approved. |

## Garbage / Rejected

### Body

All body assets are crude vector placeholders. They have transparent backgrounds but do not match Jack's original adult-animation design, suit anatomy, linework, or production shading.

| Asset | Classification | Reason |
| --- | --- | --- |
| `body/jack_torso_front.png` | REJECT_PLACEHOLDER | Simple flat suit silhouette, not production Jack body art. |
| `body/jack_torso_three_quarter.png` | REJECT_PLACEHOLDER | Simple flat suit silhouette, weak 3/4 anatomy. |
| `body/jack_arm_left_resting.png` | REJECT_PLACEHOLDER | Blocky sleeve and paw, no real anatomy or shading. |
| `body/jack_arm_right_resting.png` | REJECT_PLACEHOLDER | Blocky sleeve and paw, no real anatomy or shading. |
| `body/jack_arm_right_tie_fix.png` | REJECT_PLACEHOLDER | Gesture is schematic and not production usable. |
| `body/jack_tie_straight.png` | REJECT_PLACEHOLDER | Generic black tie shape, not enough style/detail for final physics layer. |

### Mouth / Visemes

All mouth assets are crude symbolic placeholders. They do not match Jack's muzzle anatomy, fur, lighting, or reference-sheet viseme design. They are useful only as naming/structure markers.

| Asset | Classification | Reason |
| --- | --- | --- |
| `mouth/jack_mouth_neutral.png` | REJECT_PLACEHOLDER | Simple line, no Jack muzzle context. |
| `mouth/jack_mouth_ah.png` | REJECT_PLACEHOLDER | Generic black oval mouth, not Jack-specific. |
| `mouth/jack_mouth_ee.png` | REJECT_PLACEHOLDER | Generic teeth bar, no muzzle anatomy. |
| `mouth/jack_mouth_oh.png` | REJECT_PLACEHOLDER | Generic oval, no muzzle anatomy. |
| `mouth/jack_mouth_oo_w.png` | REJECT_PLACEHOLDER | Generic oval, no muzzle anatomy. |
| `mouth/jack_mouth_mbp.png` | REJECT_PLACEHOLDER | Generic line/bar, no muzzle anatomy. |
| `mouth/jack_mouth_fv.png` | REJECT_PLACEHOLDER | Generic teeth mark, no muzzle anatomy. |
| `mouth/jack_mouth_l.png` | REJECT_PLACEHOLDER | Generic mouth icon, not Jack's viseme style. |
| `mouth/jack_mouth_s_dtn.png` | REJECT_PLACEHOLDER | Generic teeth bar, no muzzle anatomy. |
| `mouth/jack_mouth_smile.png` | REJECT_PLACEHOLDER | Generic curve, not Jack-specific. |
| `mouth/jack_mouth_smirk.png` | REJECT_PLACEHOLDER | Generic curve, not Jack-specific. |

### Eyes / Pupils

The six eye-open/half/closed layers can remain as temporary layout aids. The pupil layers are placeholders.

| Asset | Classification | Reason |
| --- | --- | --- |
| `eyes/jack_pupil_left.png` | REJECT_PLACEHOLDER | Four-color generic oval dot, not production eye art. |
| `eyes/jack_pupil_right.png` | REJECT_PLACEHOLDER | Four-color generic oval dot, not production eye art. |

### Eyebrows

All eyebrow files are technically invalid puppet layers. They are RGB files with no alpha channel, and the checkerboard is baked into the pixels. Even if the brow shapes are visually close, these cannot be composited as transparent layers.

| Asset | Classification | Reason |
| --- | --- | --- |
| `eyebrows/jack_eyebrow_left_neutral.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_right_neutral.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_left_concerned.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_right_concerned.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_left_thinking.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_right_thinking.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_left_smug.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |
| `eyebrows/jack_eyebrow_right_smug.png` | REJECT_TECHNICAL | Baked checkerboard, opaque RGB, not a transparent puppet layer. |

### Environment

Both environment assets are crude placeholders. The background may be intentionally opaque, but it is not visually acceptable. The chair is transparent but simplified and does not match the reference office shot.

| Asset | Classification | Reason |
| --- | --- | --- |
| `environment/office_background_clean.png` | REJECT_PLACEHOLDER | Flat schematic office, not matching canonical keyframes. |
| `environment/office_chair.png` | REJECT_PLACEHOLDER | Simplified chair icon, not production scene art. |

## Rebuild Priority

Use one category at a time, in this order:

1. Body/torso/arms/tie
2. Mouth/visemes
3. Eyes/pupils
4. Eyebrows
5. Environment/chair
6. PSD assembly after visual approval only

## Why PSD Workflow Remains Paused

- The manifest passed only filename/path validation.
- 29 of 37 audited layer PNGs are rejected.
- Mouth layers are structure markers, not real visemes.
- Body layers are crude placeholders and would produce a bad rig silhouette.
- Eyebrow layers have baked checkerboard backgrounds and cannot composite correctly.
- Environment layers do not match the canonical office references.
- The layout preview already shows the risk of assembling visually invalid sources.

Do not run PSD assembly again until each rebuild batch has passed visual QC.
