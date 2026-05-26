# Eyes / Blink r1 — assessment notes

**Status:** STAGING ONLY. No promotion. Stop after notes.

## Artifacts

- `jack_eye_left_closed_r1.png` — 60×55 RGBA crop, character-left eye
- `jack_eye_right_closed_r1.png` — 60×55 RGBA crop, character-right eye
- `jack_eye_blink_r1_visual_qc.png` — 6-panel QC (source + isolated + composites + comparison + 1:1 zoom)
- `jack_eye_blink_r1_composite_qc.png` — See-through + head composites side-by-side
- `eyes_blink_r1_manifest.json` — bbox sources, scales, alpha stats, do-not list
- Script: `tools/puppet/stage_eyes_blink_r1.py`

## TL;DR

**⚠️ Conditional pass.** CoPainter's "closed" eyes are technically extracted cleanly but they represent a **heavy-lidded squint**, NOT a fully-shut blink frame. The existing production `jack_eye_*_closed.png` is full-lid-down golden (no eye visible). The CoPainter bottom pair is a DIFFERENT state — closer to a deep "half-closed/sleepy" look than a true blink.

**Recommendation:** Do NOT promote r1 as a drop-in replacement for the existing closed. Either (a) **promote under a different name** (e.g., `_squint`/`_sleepy`) to serve as a new intermediate state, or (b) reject and stick with the existing eye set.

**Half variants NOT produced** — the top pair in layer_43 is Jack's normal OPEN deadpan look, indistinguishable from existing `jack_eye_*_open.png` style. CoPainter does not provide a genuinely-new half state.

## Source map (layer_43 = 152×249)

| y band | Content | Action |
|---|---|---|
| 12-29 | Eyebrows (left + right) | Ignored (out of scope) |
| 30-94 | OPEN eyes pair (with iris + sclera) | Ignored — duplicates existing `_open` |
| 95-150 | "Closed" / heavy-lidded squinted pair | **Extracted** as `_closed_r1` |
| 160-249 | Snout / jaw fragment | Ignored (out of scope) |

## QC against criteria

| Criterion | Verdict | Notes |
|---|---|---|
| Closed eyes usable? | ⚠️ Partial — usable as **squint/sleepy**, NOT as full blink | Bottom pair still shows visible eye slit; existing `_closed` is full-golden lid-down |
| Half eyes useful? | ❌ Rejected | Top pair is OPEN-style, duplicates existing `_open`; bottom already taken as `_closed_r1` |
| Preserves tired/deadpan look? | ✅ Yes | Heavy-lidded squint reads as tired-Jack; nothing anime/cute |
| Align with existing eye whites/pupils? | ⚠️ Partial | Bbox crops include golden-fur surround; existing rig uses separate eye/pupil/eyebrow assets — these are MORE-INTEGRATED single-asset crops |
| CoPainter brows/snout useful? | ❌ Rejected | Out of scope for this task; existing production has eyebrow set, snout is part of head |
| Should be promoted? | ⚠️ Conditional — see TL;DR | Rename to `_squint` if kept, or reject |
| Krita cleanup required? | ⚠️ Yes if promoting | Need to (a) re-tag the variant name, (b) verify alignment against existing eye anchor, (c) confirm the golden-fur surround doesn't clash with head fur tone |

## Key issue: "closed" mismatch with existing convention

| Asset | Visual | Lid coverage |
|---|---|---|
| Existing `jack_eye_left_open.png` | Golden upper lid + large white sclera + pupil | ~30% lid |
| Existing `jack_eye_left_half.png` | Golden upper lid + smaller white sclera + pupil | ~60% lid |
| Existing `jack_eye_left_closed.png` | **All golden**, thin black slit at bottom | **100% lid** |
| **r1 closed (CoPainter)** | Heavy golden upper lid + thin eye slit visible + small iris dot | **~85% lid** |

CoPainter's r1 is **between existing half and closed**. It does NOT match the existing "closed" convention.

## Anchor derivation

**See-through canvas (768×768) — primary:**
- Eye row y = **86** (midpoint of `eyewhite` bbox y=79-94)
- Left eye centre x = **397** (midpoint of eyewhite x=380 and overall mid x=413)
- Right eye centre x = **430** (midpoint of eyewhite x=447 and overall mid x=413)
- Scale CoPainter → See-through: **0.3439** (CoPainter head width 253 → See-through face width 87)

**Production head (1024×1024) — secondary:**
- Eye row y = **420**
- Left eye centre x = **420**
- Right eye centre x = **565**
- Scale CoPainter → head: **1.33** (rough match — 60 px crop → ~80 px target)

Both anchors are visual derivations; CoPainter ZIP has no origin metadata.

## Alignment concerns

When composited on the production head (panel 6 in the QC sheet):
- The CoPainter bbox crops include surrounding **golden fur**. This is NOT transparent fur — it's actual painted fur pixels.
- When composited over the production head (which already has its own golden fur), the CoPainter golden patches show a SLIGHT TONE DIFFERENCE vs the head's golden fur, creating visible "eye patches" on the face.
- The existing production rig uses **separate** eye/pupil/eyebrow/eyewhite assets that composite on top of a clean head — no fur patch is part of the eye asset.

## Should this be promoted?

**Not as `_closed`.** Three viable paths:

1. **Promote as `_squint`** — give CoPainter's heavy-lid look its own slot in the rig (`jack_eye_left_squint.png`, `jack_eye_right_squint.png`). Adds a new emotion state without breaking existing closed.
2. **Reject entirely** — the existing closed/half/open trio plus pupils already covers Jack's needs.
3. **Use as INSPIRATION for a hand-drawn squint** — extract reference, hand-paint in Krita to match existing eye-asset style (no surrounding fur, line-only eyelid shape).

**My recommendation:** Path 2 (reject) unless there's a specific need for a squint state. The CoPainter golden-fur surround creates compositing complications that don't pay off if the existing eye set is sufficient.

## Krita / Photoshop cleanup needed (if promoting)

- **Mandatory:** Erase the golden-fur surround so the asset is just the eye outline + lid + iris on transparent background. This matches the existing rig convention.
- **Optional:** Verify the eye-anchor offset places the squint correctly over the existing `_open` pupil position.
- **Optional:** Confirm at 1:1 zoom that the squint lineart weight matches Jack's other facial lineart.

## What this QC does NOT prove

- That Jack's puppet rig needs a squint state at all — rig spec not consulted.
- That CoPainter's eye layer would composite differently with a re-rendered head — anchor was derived against the current production head.
- That the squint reads correctly in motion (mid-blink animation frame) — only static QC done.

## Decision

**No promotion in this task.** The closed eyes are extracted, documented, and ready for review. Recommend: **reject for the existing `_closed` slot** (convention mismatch). If a `_squint` state is desired, run a separate explicit task that includes Krita cleanup to strip the fur surround.
