# Jack — Cloud Layer Splitter Output Audit

**Audit date:** 2026-05-19 (re-scanned)
**Status:** **No downloaded outputs found.** Nothing to audit yet.

> Re-scanned all 5 tool folders for any file (not just `.psd`/`.zip`/`.png`/`.json`/`.atlas`) — every folder is still empty. No extraction, layer export, or contact-sheet generation possible.

## Folders scanned

| Tool | Folder | Files found |
|---|---|---|
| See-through | `assets/puppet/cloud_layer_tests/see_through/` | — |
| Komiko | `assets/puppet/cloud_layer_tests/komiko/` | — |
| ImageToLayers | `assets/puppet/cloud_layer_tests/imagetolayers/` | — |
| Layer.ai | `assets/puppet/cloud_layer_tests/layer_ai/` | — |
| Stretchy | `assets/puppet/cloud_layer_tests/stretchy/` | — |

(Scanned for `.psd`, `.zip`, `.png`, `.json`, `.atlas`. Inputs folder excluded.)

## Next step

1. Follow [jack_cloud_layer_splitter_test_checklist.md](jack_cloud_layer_splitter_test_checklist.md) to upload `assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test.png` to each tool and save downloads into the matching folder.
2. Re-run the audit by telling Claude: **"audit the cloud test outputs"**.

When outputs exist, the audit will populate the sections below — currently empty.

---

## See-through results

**Audit pass:** 2026-05-19 (PSD audit)
**Source:** `assets/puppet/cloud_layer_tests/see_through/seethrough_output.psd` (2.9 MB)
**Canvas:** 768 × 768 RGBA (HF demo down-scaled / re-padded our 310×990 upload)
**Status:** ✅ **PASS** — 11 semantically named transparent layers exported cleanly.

### Downstream promotions (this audit cycle)

| Category | Source | Destination | Status |
|---|---|---|---|
| Hands | `assets/puppet/layers_staging/hands_r1/jack_hand_{left,right}_r1.png` (extracted from `inputs/jack_front_hands_visible_r1.png` donor pose, not from See-through) | `assets/puppet/layers/hands/jack_hand_{left,right}.png` | ✅ **Promoted 2026-05-19** — byte-identical copy, approved via composite-QC fit against See-through `topwear` layer ([notes](../assets/puppet/layers_staging/hands_r1/composite_qc/jack_hands_torso_fit_notes.md), [manifest](../assets/puppet/layers/hands/manifest.json)) |
| All other categories | — | — | Not promoted; staging only |

### Files created (audit-only, all under `assets/puppet/cloud_layer_tests/see_through/`)

| File | Purpose |
|---|---|
| `extracted/00_footwear.png` … `extracted/10_eyebrow.png` | 11 per-layer RGBA PNGs |
| `extracted/layer_manifest.json` | bbox, blend, opacity, path per layer |
| `see_through_contact_sheet.png` | 4×3 visual contact sheet |
| `tools/puppet/audit_seethrough_psd.py` | re-runnable audit script (in `tools/`) |

### Layer inventory

| # | Name | Bbox | Visual content |
|---|---|---|---|
| 00 | footwear | (289, 625, 505, 719) | Black hi-top sneakers — clean, full pair |
| 01 | legwear | (310, 364, 504, 641) | Black pants — clean, full both legs |
| 02 | handwear | (280, 190, 505, 423) | **Misnomer.** Black jacket sleeves only — Jack's hands are in pockets so no skin layer |
| 03 | back hair | (334, 24, 499, 214) | Full golden retriever head silhouette (back-of-head fur, ears merged in) |
| 04 | topwear | (314, 152, 505, 423) | Jacket + white shirt + black tie — clean, well-inpainted |
| 05 | eyelash | (378, 66, 450, 95) | Tiny dark slivers |
| 06 | ears | (360, 82, 470, 119) | Two golden ears, isolated |
| 07 | face | (366, 44, 453, 147) | Front face including snout — **mouth not separated** |
| 08 | eyewhite | (380, 79, 447, 94) | Two small white shapes |
| 09 | irides | (388, 78, 441, 87) | Two dark iris dots |
| 10 | eyebrow | (379, 54, 449, 71) | Two thin brow strokes |

### QC against criteria

| Criterion | Verdict | Notes |
|---|---|---|
| Separate transparent PNG layers? | ✅ YES | All 11 are RGBA with proper alpha |
| Preserves Jack's exact 2D style? | ✅ YES | This is decomposition, not regeneration — linework and colour match the source |
| Head / torso / arms / legs / eyes / mouth / eyebrows separated? | ⚠️ MOSTLY | Head=face+back_hair+ears, torso=topwear, legs=legwear, feet=footwear, eyes=eyewhite+irides+eyelash, eyebrows=eyebrow ✅. **Arms = sleeves only (no skin/forearm)** because front pose has hands in pockets. **Mouth NOT separated** — merged into `face` |
| Hidden / inpainted areas usable or garbage? | ✅ USABLE | Where one layer sits behind another (e.g. `back hair` behind `face`, `topwear` behind `handwear`) the reconstructed pixels look continuous and on-style — no obvious AI mush or hue shifts |
| Better than polygon/Pillow torso draft? | ✅ DECISIVELY | Polygon = one rectangular shell with teal seepage. See-through `topwear` = clean, full, addressable jacket+shirt+tie shape with proper edges — and it's only one of 11 layers |

### Usable categories

| Category | Status | Source layer(s) |
|---|---|---|
| Body / torso | ✅ Usable | `topwear` (04) |
| Legs | ✅ Usable | `legwear` (01) |
| Feet | ✅ Usable | `footwear` (00) |
| Head — face | ✅ Usable | `face` (07) |
| Head — back / fur volume | ✅ Usable | `back hair` (03) |
| Ears | ✅ Usable | `ears` (06) |
| Eyebrows | ✅ Usable | `eyebrow` (10) |
| Eyes (whites + irides) | ✅ Usable | `eyewhite` (08), `irides` (09), `eyelash` (05) — small but clean |
| Arms (sleeve geometry only) | ⚠️ Partial | `handwear` (02) — sleeve mass only, no separate forearm or hand skin |
| Environment / background | ❌ Missing | No background layer exported (input was white-bg) |

### Rejected categories

- **Mouth** — not exported as its own layer. Anything mouth-related is baked into `face` (07). Lip-sync / talk states cannot be driven from this PSD alone.
- **Hands / arm skin** — Jack's hands are in pockets in the front pose, so the model never had skin pixels to segment. Need a different pose (e.g. hands at side) to get this.
- **Tail** — not present (front pose hides the tail).

### Verdict

**See-through is the strongest cloud option tested so far and beats the polygon draft by a large margin.** It's good enough that I would build the V1 puppet body on top of it — clothing + legs + feet + head shells are essentially production-ready as audit assets; eye sub-layers are usable as-is for blink rigs.

**Important caveat (visual QC overrides alpha stats):** Despite 11 clean layers, this PSD alone does **not** give us a full puppet. Missing pieces are *the* puppet-critical ones for talking-head shorts: mouth, eyebrows-with-states, hands. The mouth gap is the deal-breaker for V1 lip-style states; we'll need to either (a) re-run See-through on the side pose + hands-visible pose to capture arms/tail/hand-skin, or (b) hand-paint mouth states on top of the See-through `face` layer.

### Exact next recommendation

1. **Don't promote anything yet.** Keep these in `cloud_layer_tests/see_through/extracted/`.
2. **Re-run See-through on two more poses** to fill the gaps:
   - **Side pose** of the character sheet (middle pose) — to get a `tail` layer and confirm `handwear` separation when hands aren't in pockets.
   - **A hands-out / arms-visible pose** (use jack_02 alt pose if it exists, otherwise hand-crop a 3/4 pose) — to get true arm skin + hand layers.
3. **Hand-paint mouth states** on a copy of layer `07_face.png` (closed / open / talking) — See-through won't give us this no matter how many poses we feed it; the source art doesn't have a separate mouth.
4. After steps 2-3, decide whether to promote — that's a separate explicit task, not part of this audit.

## CoPainter results

**Audit pass:** 2026-05-19
**ZIP:** `assets/puppet/cloud_layer_tests/copainter/layers_1779216312185.zip` (948 KB, moved from project root)
**Extracted to:** `assets/puppet/cloud_layer_tests/copainter/extracted_layers_1779216312185/`
**Status:** ✅ **PASS** — 11 cleanly named transparent layers with **finer granularity than See-through** (jacket / shirt+tie / belt split separately).

### Short verdict

CoPainter beats See-through on clothing granularity and provides a bonus eyes-with-blink-states layer. But: every layer maxes at alpha ≈254 (no fully-opaque pixels), and there's **no origin/offset metadata**, so any composite needs manual alignment. The "arm" layers are a generated splayed-hand pose, not Jack's at-side puppet pose — they do NOT replace the promoted at-side hand crops. **No mouth layer** — confirms that no automated tool will give us Jack's mouth.

### Exact file list

| File | Size (W×H) | a≥200 | Content (visual) | Heuristic category |
|---|---|---|---|---|
| `layer_01.png` | 253×284 | 45.1% | Golden head with face, eyes, ears, nose, faint baked mouth line | **head_full** (clean) |
| `layer_05.png` | 80×11 | 0.0% | Tiny semi-alpha white strip | **noise / eye sparkle** — discard |
| `layer_15.png` | 41×10 | 0.0% | Tiny semi-alpha white strip | **noise / eye sparkle** — discard |
| `layer_43.png` | 152×249 | 22.9% | TWO eye pairs (open + closed) + eyebrows + golden snout/chin fragment | **eyes_with_blink_states + jaw bit** |
| `layer_71.png` | 269×390 | 76.5% | Black jacket alone (shirt-collar gap shows transparent) | **jacket** (better than ST topwear) |
| `layer_75.png` | 239×311 | 68.9% | White shirt + black tie (fully reconstructed under-jacket) | **shirt_with_tie** |
| `layer_76.png` | 94×385 | 61.3% | Full arm + open paw with 4 spread fingers | **arm_extended_pose** (NOT at-side) |
| `layer_77.png` | 174×44 | 52.8% | Black belt with metal buckle | **belt** (NEW — ST didn't split this) |
| `layer_78.png` | 115×398 | 67.5% | Tapered leg/thigh-or-arm-piece — pose ambiguous | **limb_piece** (unclear) |
| `layer_79.png` | 255×544 | 61.0% | Both legs + both Converse hi-tops (pose A) | **legs_shoes_A** |
| `layer_80.png` | 278×542 | 57.3% | Both legs + both Converse hi-tops (pose B, alt) | **legs_shoes_B** |

### Layer mapping table (Jack-anatomy → CoPainter file)

| Jack anatomy | CoPainter source | Notes |
|---|---|---|
| Head (full) | `layer_01` | Includes eyes, nose, faint mouth — all baked in |
| Eyes (open) | `layer_43` (top pair) | Separable from head |
| Eyes (closed / blink) | `layer_43` (bottom pair) | **Bonus** — blink rig possible |
| Eyebrows | `layer_43` | Baked into the eyes layer |
| Muzzle / snout | `layer_43` (fur fragment) + `layer_01` | Split awkwardly; mostly in head |
| Jacket | `layer_71` | Alone — better split than ST |
| Shirt + tie | `layer_75` | Alone — better split than ST |
| Belt | `layer_77` | NEW — ST merged this |
| Arms / hands | `layer_76`, `layer_78` (?), nothing for the at-side pose | Generated pose, not Jack's pocket pose |
| Legs + shoes | `layer_79` and/or `layer_80` | Two near-identical variants |
| Mouth | **none** | No separate mouth layer |

### QC against criteria

| Criterion | Verdict |
|---|---|
| Transparent PNGs? | ✅ Yes (RGBA mode) — but **no alpha=255 pixels in any layer** (max ≈254). Composites will be very slightly washed out unless thresholded. |
| Bbox-cropped or canvas-sized? | **Bbox-cropped**, **no origin metadata in the ZIP** — recompose requires manual alignment. |
| Preserves Jack's locked design? | ✅ Yes — head, jacket, shirt, pants all match the character sheet (no anime/redraw). |
| Head/eyes/muzzle/jacket/shirt/belt/arms/legs/shoes mapping? | See table above. |
| Hidden / inpainted areas? | ✅ Clean. Shirt layer shows full under-jacket reconstruction; legs layer shows full ankle area under pants. No AI mush. |
| Mouth fragments usable? | ❌ **No mouth layer exported.** `layer_05`/`layer_15` are anti-aliased noise strips, not mouth artwork. |
| Output changes the plan? | ⚠️ Partly — see below. |

### Comparison vs already-promoted hands

**Promoted hands** (`assets/puppet/layers/hands/jack_hand_left.png`, `jack_hand_right.png`): tightly-cropped 98-102 × 160 paws in Jack's **at-side closed pose**, extracted from the hands-visible donor image.

**CoPainter arms** (`layer_76`, `layer_78`): full arm assets in an **extended / splayed-fingers pose** that does not match Jack's canonical at-side pose. Layer 78 may not even be an arm — its shape suggests a thigh/leg piece.

**Conclusion:** the CoPainter arms **do NOT replace the promoted hands.** Different pose, different scope (arm vs paw-only). Promoted hands stay locked.

### Comparison vs See-through

| Category | See-through | CoPainter | Winner |
|---|---|---|---|
| Jacket | Merged into `topwear` (jacket+shirt+tie) | `layer_71` alone | **CoPainter** — finer split |
| Shirt + tie | Merged into `topwear` | `layer_75` alone | **CoPainter** — finer split |
| Belt | Not split | `layer_77` alone | **CoPainter** — exclusive asset |
| Legs / pants | `legwear` (255×311ish, padded) | `layer_79`/`80` (full legs+shoes) | **CoPainter** — includes shoes too |
| Shoes | `footwear` separate | Baked into `layer_79`/`80` | **See-through** — separate shoes allow independent rig |
| Head | Split: `face` + `back hair` + `ears` (3 layers) | `layer_01` (one layer) | **See-through** — finer head rig possible |
| Eyes | `eyewhite` + `irides` + `eyelash` + `eyebrow` separate | `layer_43` includes open+closed pairs | **CoPainter** — blink states are a unique advantage |
| Mouth | None (limitation) | None (limitation) | tie — neither solves the mouth problem |
| Alpha quality | Solid 255 where opaque | Max ≈254, all anti-aliased | **See-through** — cleaner alpha |
| Origin metadata | PSD layer offsets included | None (loose bbox PNGs) | **See-through** — much easier to rig |

### Should anything replace See-through?

**Mostly no.** See-through's PSD-with-offsets is the better baseline because rigging needs origin metadata. CoPainter wins on a few specific categories that we could **adopt as supplements**, not replacements:
- `layer_71` (jacket alone) — useful if we want to rig the jacket independently from shirt+tie
- `layer_75` (shirt+tie alone) — same reason
- `layer_77` (belt) — only source we have for an addressable belt layer
- `layer_43` (closed-eye pair) — only source for blink states

For each, **alignment work is required** to map them onto our existing canvas convention.

### Should anything replace the promoted hands?

**No.** Promoted hands stay locked. CoPainter arms are a different pose (extended/splayed) and don't match Jack's at-side canonical pose. Layer 78 may not be an arm at all.

### Files created (audit-only)

| File | Purpose |
|---|---|
| `extracted_layers_1779216312185/layer_*.png` | 11 extracted PNGs |
| `copainter_layers_1779216312185_contact_sheet.png` | 4×3 contact sheet with bbox + median RGB per layer |
| `copainter_layers_1779216312185_recompose_qc.png` | Stack-test composite (misaligned — confirms origin metadata missing) |
| `copainter_layers_1779216312185_audit.json` | Per-layer probe stats |
| `tools/puppet/audit_copainter_zip.py` | Re-runnable audit script |

### Next recommended single category

**Belt.** It's the smallest, cleanest, lowest-risk CoPainter asset, has no See-through equivalent, and lets us validate the alignment workflow before tackling jacket/shirt/eyes. Once belt alignment is solved, the same workflow scales to the bigger categories.

Concretely:
1. Verify `layer_77` (174×44) places correctly on the production-head/torso composite.
2. Stage as `assets/puppet/layers_staging/belt_r1/` with documented anchor.
3. Decide promotion in a separate explicit task.

### What this audit does NOT do

- No promotion. No writes to `assets/puppet/layers/`.
- No edits to See-through extracted files.
- No edits to promoted hands.
- No PSD assembly.
- No alignment work — the misaligned recompose QC is a deliberate confirmation that origins are missing, not an attempted composite.

## Komiko results
*(empty — awaiting download)*

## ImageToLayers results
*(empty — awaiting download)*

## Layer.ai results
*(empty — awaiting download)*

## Stretchy results
*(empty — awaiting `#1-#4` to produce a layered file first)*

---

## Audit criteria (applied per tool once outputs exist)

For each tool I will record:

- **Layers exported:** count, names, transparency
- **Style fidelity:** matches Jack's exact linework? Or redrawn?
- **Anatomical separation:** head / torso / arms / legs / eyes / mouth / eyebrows split cleanly?
- **Inpainting quality:** behind-layer reconstruction usable or noisy garbage?
- **vs. polygon draft:** beats `assets/puppet/layers_staging/body_r1/jack_torso_front_draft.png`?
- **Usable categories:** body / arms / eyes / mouth / eyebrows / environment — which are production-ready?
- **Production verdict:** worth promoting to `assets/puppet/layers/`? (Decision only — promotion is not automatic.)
