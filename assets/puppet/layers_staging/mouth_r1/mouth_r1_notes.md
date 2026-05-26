# Mouth r1 — assessment notes

**Status:** STAGING ONLY. No promotion. Stop after notes.

## Artifacts
- 9 viseme PNGs: `jack_mouth_*_r1.png` (512×512 RGBA, intrinsic anchor (256, 270))
- Face patch (audit-only): `jack_face_mouth_patch_r1.png` (220×80 RGBA, bbox-cropped)
- Patch test composite: `jack_face_mouth_patch_test_composite_r1.png`
- Visual QC: `jack_mouth_r1_visual_qc.png`
- Composite QC: `jack_mouth_r1_composite_qc.png` (See-through primary + head secondary)
- Manifest: `mouth_r1_manifest.json`
- Scripts: `tools/puppet/build_mouth_r1.py`, `tools/puppet/build_mouth_r1_qc_and_patch.py`

## TL;DR

**Closed mouths (`neutral`, `slight_frown`, `slight_smirk`, `mbp`): visually usable on both anchors.**

**Open mouths (`open_small`, `open_medium`, `oo`, `ee`, `fv`): functional but need Krita cleanup before promotion** — they sit cleanly geometrically but the open hole needs a thin golden muzzle contour around it so the dark interior doesn't read as a sticker. `ee` and `fv` additionally need character-bible review (Jack's deadpan style may not want visible teeth at all).

The face patch is **not strictly required** by either anchor:
- See-through face layer has no baked mouth (only 28 dark pixels, all in the brow region).
- On the production head, mouth y=745 sits *above* the baked chin split (y=748-820), so the chin split reads as a faint chin-shadow rather than a competing mouth line.

The patch is retained as an audit-only support asset.

## Method recap

- **Deterministic Pillow procedural draw.** No AI, no cloud. CoPainter not depended on.
- 4× supersample + LANCZOS downsample for clean anti-aliasing.
- 512×512 mouth canvas; intrinsic anchor (256, 270) — matches centroid cluster of existing production set.
- Style: simple black lineart (RGB 20,20,20), maroon mouth interior (RGB 88,36,32), warm tongue (RGB 160,70,78), cream teeth (RGB 240,235,220 — matches Jack's shirt cream tone).

## Anchor system (documented in manifest)

| Anchor | Reference | Position | Scale to apply |
|---|---|---|---|
| **Primary** | See-through face layer (07_face.png in 768×768 canvas) — face bbox (366, 44, 453, 147) | Muzzle bottom-center: **(405, 142)** | Mouth canvas × **0.183** |
| **Secondary** | Production head (jack_head_front_base.png, 1024×1024) | Just below nose tip: **(489, 745)** | 1.0 (no scale) |

Rule for both: place the scaled mouth canvas so its intrinsic anchor (256, 270) lands on the target's mouth anchor.

## Assessment per criterion

### Style compatibility with Jack
| Viseme | Verdict | Notes |
|---|---|---|
| neutral | ✅ matches | Wide shallow tired curve — reads as Jack's deadpan default |
| slight_frown | ✅ matches | Deeper droop, still understated |
| slight_smirk | ✅ matches | Asymmetric upturn on character-right side |
| open_small | ⚠️ functional | Dark interior + tongue OK; floats on muzzle without a contour |
| open_medium | ⚠️ functional | Same as small, more visible — needs muzzle contour |
| oo | ⚠️ functional | Rounder vertical oval; same floating-on-fur issue |
| ee | ⚠️ stylised | Wide tooth bar; verify against character bible — may be too theatrical |
| fv | ⚠️ stylised | Teeth-on-lip; busy detail — verify before keeping |
| mbp | ✅ matches | Tight compressed flat line; reads as "pressed lips" |

### Anchor placement consistency
✅ All 9 visemes have opaque-pixel centroid at x=256 (canvas center, ±0), y=268-281. Composite y-jitter is intentional and natural — open mouths drop slightly lower than closed mouths to follow natural mouth anatomy.

### Baked-mouth interference
- **See-through face layer:** no baked mouth (only 28 dark pixels, all in brow region). No interference.
- **Production head:** dark linework at y=748-820 (chin split centerline y=748-780, jaw underline y=784-820). Mouth y=745 was chosen to sit *above* the chin split — the baked line falls *below* the new mouth artwork and reads as a faint chin-shadow rather than competing artwork.

### Face patch usability
- **Status:** audit-only support asset.
- **Tone match:** ✅ fur RGB (251, 219, 151) sampled from the immediate neighbours of the patch zone.
- **Edge blend:** ⚠️ uniform fill lacks the surrounding fur's hand-drawn micro-shading; reads as a slightly lighter blob under close inspection.
- **Conclusion:** patch is technically functional but for production a **Krita clone-stamp with brush jitter** is preferable. Not required at the mouth y=745 anchor.

### Pass / fail summary
| Asset | Pass? | Reason |
|---|---|---|
| `jack_mouth_neutral_r1.png` | ✅ | Style-correct, anchor-correct |
| `jack_mouth_slight_frown_r1.png` | ✅ | Style-correct |
| `jack_mouth_slight_smirk_r1.png` | ✅ | Style-correct |
| `jack_mouth_mbp_r1.png` | ✅ | Style-correct, thicker compression reads as pressed lips |
| `jack_mouth_open_small_r1.png` | ⚠️ Conditional pass | Functional but needs muzzle-contour pass |
| `jack_mouth_open_medium_r1.png` | ⚠️ Conditional pass | As above |
| `jack_mouth_oo_r1.png` | ⚠️ Conditional pass | As above |
| `jack_mouth_ee_r1.png` | ⚠️ Style review needed | Teeth detail may not fit Jack's deadpan |
| `jack_mouth_fv_r1.png` | ⚠️ Style review needed | As above |
| `jack_face_mouth_patch_r1.png` | ⚠️ Audit-only | Functional; Krita clone-stamp preferable for production |

**Outright rejections:** None. All visemes are at minimum functional placeholders.

### Krita cleanup checklist (required before any promotion of the open/teeth set)
1. **All open mouths**: paint a thin (~3 px at 512 res) golden fur edge highlight around the dark interior — fixes the "floating sticker" effect when composited.
2. **ee, fv**: verify with character bible. If Jack's spec says no visible teeth, replace with closed-mouth variants. If teeth are allowed, hand-polish lineart to remove the machine-symmetric feel.
3. **Patch (if used)**: replace with Krita clone-stamp + brush jitter; do not ship the flat-fill patch as-is.
4. **All visemes (optional)**: nudge stroke endpoints by ±2 px to break the slight machine-symmetry — Jack's lineart has hand-drawn asymmetry.

## What this QC does NOT prove
- That these mouth shapes exactly match the puppet rig's expected viseme tags (rig spec not consulted in this task).
- That open-mouth interior tones are colourimetrically correct for Jack's species/style — only visual plausibility tested.
- That re-renders of the See-through PSD or `jack_head_front_base.png` won't shift the muzzle anchor; if either changes, re-derive anchors before reuse.

## Decision

**No promotion.** The closed-mouth set (`neutral`, `slight_frown`, `slight_smirk`, `mbp`) is publishable now if needed; the open and teeth visemes need a Krita pass. Recommend: address the Krita checklist, regenerate this QC, then decide as a separate explicit task whether the full set goes to `assets/puppet/layers/mouth/` or only the closed subset.
