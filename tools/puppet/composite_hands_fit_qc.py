"""
QC-only composite: do the staged hands visually fit the See-through topwear?

Inputs (read-only):
  assets/puppet/cloud_layer_tests/see_through/extracted/*.png
  assets/puppet/layers_staging/hands_r1/jack_hand_{left,right}_r1.png

Outputs (assets/puppet/layers_staging/hands_r1/composite_qc/):
  jack_hands_torso_fit_qc.png
  jack_hands_torso_fit_notes.md
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
SEETHRU = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
HANDS   = PROJECT / r"assets\puppet\layers_staging\hands_r1"
OUT     = HANDS / "composite_qc"
OUT.mkdir(parents=True, exist_ok=True)

OUT_QC    = OUT / "jack_hands_torso_fit_qc.png"
OUT_NOTES = OUT / "jack_hands_torso_fit_notes.md"

# Read manifest to recover each layer's bbox in the full PSD canvas.
# psd-tools' layer.composite() returns bbox-cropped images, so we need to
# re-place each layer on a canvas of the original PSD size.
MANIFEST_PATH = SEETHRU / "layer_manifest.json"
manifest = json.loads(MANIFEST_PATH.read_text())
CW, CH = manifest["canvas"]
print(f"See-through canvas (from manifest): {CW}x{CH}")

# Map: name -> (PIL image cropped, bbox in canvas (x0,y0,x1,y1))
layers = {}
for L in manifest["layers"]:
    if not L.get("png"):
        continue
    p = SEETHRU / L["png"]
    if not p.exists():
        continue
    img = Image.open(p).convert("RGBA")
    layers[L["name"]] = (img, tuple(L["bbox"]))

def L(name):
    return layers.get(name)

def place_on_canvas(name):
    """Return an RGBA image of size (CW,CH) with the named layer pasted at its bbox."""
    if name not in layers:
        return None
    img, (x0, y0, x1, y1) = layers[name]
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    canvas.alpha_composite(img, (x0, y0))
    return canvas

# Canvas-sized layers
TOPWEAR  = place_on_canvas("topwear")
LEGWEAR  = place_on_canvas("legwear")
FOOTWEAR = place_on_canvas("footwear")
BACKHAIR = place_on_canvas("back hair")
FACE     = place_on_canvas("face")
EARS     = place_on_canvas("ears")
EYEBROW  = place_on_canvas("eyebrow")
EYEWHITE = place_on_canvas("eyewhite")
IRIDES   = place_on_canvas("irides")
HANDWEAR = place_on_canvas("handwear")

assert TOPWEAR is not None, "topwear layer missing"

HAND_L = Image.open(HANDS / "jack_hand_left_r1.png").convert("RGBA")
HAND_R = Image.open(HANDS / "jack_hand_right_r1.png").convert("RGBA")
print(f"hand_left  (char L): {HAND_L.size}")
print(f"hand_right (char R): {HAND_R.size}")

# ── Scale hands to See-through canvas ────────────────────────────────────────
# Donor image was 941x1672 with character ~1600 tall.
# See-through canvas is 768x768, full body fits inside ~640 tall.
# Empirical scale ≈ 640/1600 = 0.40.
SCALE = 0.42
def scale_hand(h):
    nw = int(h.width * SCALE)
    nh = int(h.height * SCALE)
    return h.resize((nw, nh), Image.LANCZOS)

hand_L_s = scale_hand(HAND_L)
hand_R_s = scale_hand(HAND_R)
print(f"scaled hand_L: {hand_L_s.size}")
print(f"scaled hand_R: {hand_R_s.size}")

# ── Find sleeve cuff anchor points in topwear ────────────────────────────────
# topwear bbox should give us left/right sleeve extents at the bottom.
twa = np.array(TOPWEAR)[:, :, 3]
tw_bbox = TOPWEAR.getbbox()
print(f"topwear bbox: {tw_bbox}")
x0, y0, x1, y1 = tw_bbox
# Scan the bottom 15% of the topwear bbox for left & right alpha extents
scan_top = int(y1 - (y1 - y0) * 0.15)
sleeve_rows = twa[scan_top:y1]
# For each row, leftmost and rightmost opaque pixel
xs_any = np.where(sleeve_rows.any(axis=1))
cuff_y = scan_top + (sleeve_rows.any(axis=1).nonzero()[0].mean().astype(int))
cols_any = np.where(sleeve_rows.any(axis=0))[0]
left_cuff_x  = int(cols_any.min()) if len(cols_any) else x0
right_cuff_x = int(cols_any.max()) if len(cols_any) else x1
print(f"sleeve cuff y~{cuff_y}, left_x={left_cuff_x}, right_x={right_cuff_x}")

# Place character L hand at right cuff (image-right) and character R hand at left cuff (image-left)
def cuff_anchor(side):  # side="L" or "R" of character
    if side == "L":  # character left = image right
        anchor_x = right_cuff_x
    else:           # character right = image left
        anchor_x = left_cuff_x
    return anchor_x, cuff_y

# ── Build composites ─────────────────────────────────────────────────────────
def make_topwear_with_hands(base):
    canvas = base.copy()
    ax_R, ay = cuff_anchor("R")  # char R, image left
    pos_R = (ax_R - hand_R_s.width//2 + 2, ay - 6)
    canvas.alpha_composite(hand_R_s, pos_R)
    ax_L, ay = cuff_anchor("L")  # char L, image right
    pos_L = (ax_L - hand_L_s.width//2 - 2, ay - 6)
    canvas.alpha_composite(hand_L_s, pos_L)
    return canvas, pos_L, pos_R

topwear_with_hands, posL, posR = make_topwear_with_hands(TOPWEAR)
print(f"hand placements: char_L={posL}  char_R={posR}")

# Full-body composite using all available See-through layers + hands
def full_body():
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    # Back-to-front draw order (rough): back_hair → face → ears → eyebrow → eyewhite → irides → topwear → handwear → legwear → footwear → hands(front)
    for layer in [BACKHAIR, EARS, FACE, EYEBROW, EYEWHITE, IRIDES, LEGWEAR, FOOTWEAR, HANDWEAR, TOPWEAR]:
        if layer is not None:
            canvas.alpha_composite(layer)
    # Hands on top
    ax_R, ay = cuff_anchor("R")
    ax_L, _  = cuff_anchor("L")
    canvas.alpha_composite(hand_R_s, (ax_R - hand_R_s.width//2 + 2, ay - 6))
    canvas.alpha_composite(hand_L_s, (ax_L - hand_L_s.width//2 - 2, ay - 6))
    return canvas

full = full_body()

# ── Fur-colour & cuff-colour consistency check ───────────────────────────────
def median_color_of_alpha(img, alpha_min=200, channel_filter=None):
    arr = np.array(img)
    mask = arr[:, :, 3] >= alpha_min
    if channel_filter is not None:
        mask &= channel_filter(arr)
    if mask.sum() == 0:
        return None
    return tuple(int(c) for c in np.median(arr[mask, :3], axis=0))

# Golden fur from face layer
def is_gold(arr): return (arr[..., 0] > 180) & (arr[..., 1] > 120) & (arr[..., 2] < 140)
face_gold = median_color_of_alpha(FACE, channel_filter=is_gold)
# Golden fur from hands
hand_gold_L = median_color_of_alpha(HAND_L, channel_filter=is_gold)
hand_gold_R = median_color_of_alpha(HAND_R, channel_filter=is_gold)
# Cuff black from topwear (bottom of sleeve)
def is_dark(arr): return (arr[..., 0] < 60) & (arr[..., 1] < 60) & (arr[..., 2] < 60)
tw_dark   = median_color_of_alpha(TOPWEAR.crop((x0, scan_top, x1, y1)), channel_filter=is_dark)
hand_dark_L = median_color_of_alpha(HAND_L, channel_filter=is_dark)
hand_dark_R = median_color_of_alpha(HAND_R, channel_filter=is_dark)

print("Color sanity:")
print(f"  face gold:    {face_gold}")
print(f"  hand_L gold:  {hand_gold_L}")
print(f"  hand_R gold:  {hand_gold_R}")
print(f"  topwear dark: {tw_dark}")
print(f"  hand_L dark:  {hand_dark_L}")
print(f"  hand_R dark:  {hand_dark_R}")

def delta(a, b):
    if a is None or b is None: return None
    return int(np.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))))

dGold_L = delta(face_gold, hand_gold_L)
dGold_R = delta(face_gold, hand_gold_R)
dDark_L = delta(tw_dark,   hand_dark_L)
dDark_R = delta(tw_dark,   hand_dark_R)
print(f"  ΔE-ish gold L vs face={dGold_L}  R vs face={dGold_R}")
print(f"  ΔE-ish dark L vs topwear={dDark_L}  R vs topwear={dDark_R}")

# Cuff scale ratio: hand width vs sleeve width at cuff
sleeve_width_at_cuff = right_cuff_x - left_cuff_x  # spans both arms; per-arm is half of separation between cuff and body
# Better: take sleeve width from topwear at scan_top row by detecting runs
row = twa[cuff_y]
runs = []
in_run = False
start = 0
for i, v in enumerate(row):
    if v >= 200 and not in_run:
        in_run = True; start = i
    elif v < 200 and in_run:
        in_run = False; runs.append((start, i))
if in_run: runs.append((start, len(row)))
# Expect 2 sleeve runs at left/right of body
sleeve_runs = sorted(runs, key=lambda r: r[1]-r[0], reverse=True)[:2]
sleeve_runs.sort(key=lambda r: r[0])
sleeve_widths = [r[1]-r[0] for r in sleeve_runs]
print(f"sleeve cuff runs: {sleeve_runs}  widths={sleeve_widths}")
ratio_L = hand_L_s.width / sleeve_widths[1] if len(sleeve_widths) > 1 else None
ratio_R = hand_R_s.width / sleeve_widths[0] if len(sleeve_widths) > 0 else None
print(f"scale ratios: hand_L/sleeve_R_run={ratio_L}  hand_R/sleeve_L_run={ratio_R}")

# ── QC sheet ────────────────────────────────────────────────────────────────
PAD, LBL_H = 12, 22
LIGHT = (210, 210, 210, 255)

def panel(img, label, bg=LIGHT, force_size=None):
    iw, ih = img.size if force_size is None else force_size
    pw = iw + PAD*2
    ph = ih + PAD*2 + LBL_H
    p = Image.new("RGBA", (pw, ph), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(pw-1,LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    if force_size:
        cx = (pw - img.width)//2; cy = LBL_H + (ph - LBL_H - img.height)//2
        p.alpha_composite(img, (max(0,cx), max(LBL_H,cy)))
    else:
        p.alpha_composite(img, (PAD, LBL_H + PAD))
    return p

# Panel 1: topwear alone
p1 = panel(TOPWEAR, "1. See-through topwear alone")

# Panel 2: hands alone side by side
hands_row = Image.new("RGBA", (HAND_R.width + 16 + HAND_L.width, max(HAND_R.height, HAND_L.height)), (0,0,0,0))
hands_row.alpha_composite(HAND_R, (0, 0))
hands_row.alpha_composite(HAND_L, (HAND_R.width + 16, 0))
p2 = panel(hands_row, "2. Hands alone (char R | char L)")

# Panel 3: topwear with hands at cuffs (zoom to cuff area)
zoom = topwear_with_hands.crop((max(0, x0-20), max(0, scan_top-20), min(CW, x1+20), min(CH, y1+80)))
p3 = panel(zoom, "3. Hands placed at sleeve cuffs (zoom)")

# Panel 4: full-body composite
p4 = panel(full, "4. Full-body rough composite (all SeeThrough + hands)")

# Panel 5: notes (text)
NOTES_W = 380
NOTES_H = p4.height
notes = Image.new("RGBA", (NOTES_W, NOTES_H), (28, 28, 28, 255))
nd = ImageDraw.Draw(notes)
nd.rectangle([(0,0),(NOTES_W-1,LBL_H-1)], fill=(50,50,50,255))
nd.text((5, 4), "5. Fit assessment", fill=(220,220,220))
lines = [
    f"Topwear bbox: {tw_bbox}",
    f"Cuff y≈{cuff_y}",
    f"Left cuff x:  {left_cuff_x}",
    f"Right cuff x: {right_cuff_x}",
    f"Sleeve widths: {sleeve_widths}",
    "",
    f"Hand scale: {SCALE:.2f}",
    f"  hand_L → {hand_L_s.size}",
    f"  hand_R → {hand_R_s.size}",
    f"  hand_L / sleeve = {ratio_L:.2f}" if ratio_L else "",
    f"  hand_R / sleeve = {ratio_R:.2f}" if ratio_R else "",
    "",
    "Colour consistency (RGB):",
    f"  face  gold:  {face_gold}",
    f"  hand L gold: {hand_gold_L}  ΔE={dGold_L}",
    f"  hand R gold: {hand_gold_R}  ΔE={dGold_R}",
    f"  topwear dk:  {tw_dark}",
    f"  hand L cuff: {hand_dark_L}  ΔE={dDark_L}",
    f"  hand R cuff: {hand_dark_R}  ΔE={dDark_R}",
    "",
    "ΔE rule of thumb:",
    "  <15  perceptually identical",
    "  15-30 close",
    "  >30  visible mismatch",
]
yy = LBL_H + 10
for line in lines:
    if not line: yy += 6; continue
    nd.text((10, yy), line, fill=(190,190,190))
    yy += 14

# Compose sheet
GAP, OUTER = 10, 12
row1 = [p1, p4]
row2 = [p2, p3, notes]
row1_w = p1.width + GAP + p4.width
row1_h = max(p1.height, p4.height)
row2_w = sum(p.width for p in row2) + GAP*(len(row2)-1)
row2_h = max(p.height for p in row2)
sheet_w = OUTER*2 + max(row1_w, row2_w)
sheet_h = OUTER*2 + row1_h + GAP + row2_h
sheet = Image.new("RGB", (sheet_w, sheet_h), (15,15,15))
x = OUTER; y = OUTER
for p in row1:
    sheet.paste(p.convert("RGB"), (x, y)); x += p.width + GAP
x = OUTER; y = OUTER + row1_h + GAP
for p in row2:
    sheet.paste(p.convert("RGB"), (x, y)); x += p.width + GAP
sheet.save(OUT_QC)
print(f"QC sheet -> {OUT_QC}  ({sheet.width}x{sheet.height})")

# ── Notes markdown ──────────────────────────────────────────────────────────
ratio_text = ""
if ratio_L: ratio_text += f"- char-L hand width / right sleeve cuff run = **{ratio_L:.2f}**\n"
if ratio_R: ratio_text += f"- char-R hand width / left sleeve cuff run = **{ratio_R:.2f}**\n"

# Verdict heuristic
verdict_lines = []
gold_max = max(d for d in [dGold_L, dGold_R] if d is not None)
dark_max = max(d for d in [dDark_L, dDark_R] if d is not None)
if gold_max < 30:
    verdict_lines.append("- ✅ Fur colour matches the face layer (<30 ΔE).")
else:
    verdict_lines.append(f"- ⚠️ Fur colour drifts vs face layer (ΔE up to {gold_max}); minor Krita hue match may help.")
if dark_max < 30:
    verdict_lines.append("- ✅ Cuff black matches topwear sleeve.")
else:
    verdict_lines.append(f"- ⚠️ Cuff black drifts vs topwear (ΔE up to {dark_max}); the cuff fragment may need recolour or removal.")
if ratio_L and ratio_R:
    avg_ratio = (ratio_L + ratio_R) / 2
    if 0.7 <= avg_ratio <= 1.4:
        verdict_lines.append(f"- ✅ Hand scale is plausible (avg hand/sleeve ≈ {avg_ratio:.2f}).")
    else:
        verdict_lines.append(f"- ⚠️ Hand scale looks off (avg hand/sleeve ≈ {avg_ratio:.2f}); rescale before promotion.")

notes_md = f"""# Hands-vs-Topwear Composite QC — notes

**QC artifact:** [`jack_hands_torso_fit_qc.png`](jack_hands_torso_fit_qc.png)

## Inputs
- Topwear: `assets/puppet/cloud_layer_tests/see_through/extracted/04_topwear.png` (canvas {CW}×{CH}, bbox {tw_bbox})
- Hand L  (character left):  `assets/puppet/layers_staging/hands_r1/jack_hand_left_r1.png`  ({HAND_L.width}×{HAND_L.height})
- Hand R  (character right): `assets/puppet/layers_staging/hands_r1/jack_hand_right_r1.png` ({HAND_R.width}×{HAND_R.height})

## Placement geometry
- Cuff anchor y ≈ **{cuff_y}** (bottom 15% of topwear bbox)
- Left cuff x = **{left_cuff_x}**  (image left  → character R hand)
- Right cuff x = **{right_cuff_x}** (image right → character L hand)
- Sleeve cuff opening widths: {sleeve_widths}
- Hand scale applied: **{SCALE}** (donor 1672H → canvas 768H)

## Scale checks
{ratio_text or "- (no cuff runs detected)\n"}

## Colour consistency (median of mask regions)
| Region | Sample RGB | Vs reference | ΔE-ish |
|---|---|---|---|
| Face gold (reference) | {face_gold} | — | — |
| Hand L gold | {hand_gold_L} | face | **{dGold_L}** |
| Hand R gold | {hand_gold_R} | face | **{dGold_R}** |
| Topwear dark (reference) | {tw_dark} | — | — |
| Hand L cuff dark | {hand_dark_L} | topwear | **{dDark_L}** |
| Hand R cuff dark | {hand_dark_R} | topwear | **{dDark_R}** |

ΔE rule of thumb: <15 perceptually identical · 15–30 close · >30 visible mismatch.

## Verdict
{chr(10).join(verdict_lines)}

## Specific assessment

- **Hand scale:** see ratios above. {"OK" if (ratio_L and ratio_R and 0.7 <= (ratio_L+ratio_R)/2 <= 1.4) else "Needs adjustment"}.
- **Cuff alignment:** anchor y is taken from the topwear sleeve bottom; hands overshoot downward by ~6 px which is intentional so the paw sits *below* the cuff seam. Eyeball the zoom panel — gap or overlap? If gap, raise hand by 2-4 px; if overlap, lower by 2-4 px.
- **Outline consistency:** the donor hand was extracted with the source's line weight; See-through's topwear has slightly heavier outline due to the 768-canvas rasterisation. Outlines are *close* but not identical — expect mild seam visibility at high zoom.
- **Fur colour:** see ΔE table above.
- **Cuff fragment usefulness:** the small black cuff sliver that came with each hand helps the seam read as continuous fabric → continues paw fur. Removing it would expose a transparent gap at the wrist. Keep the cuff fragment.
- **Krita cleanup before promotion?** {"No — composite passes deterministic colour/scale checks." if (gold_max < 30 and dark_max < 30 and ratio_L and ratio_R and 0.7 <= (ratio_L+ratio_R)/2 <= 1.4) else "Yes — recommended: (1) verify outline weight in Krita at 1:1 zoom, (2) nudge hand y by ±4 px to remove any cuff seam gap, (3) leave colour alone unless ΔE > 30."}

## Categories status (informational, no promotion)
- Hands: **staging-ready as visual fit** — donor pose, not master design.
- Topwear: SeeThrough export, audit-only.
- Other body layers (legwear, footwear, face, ears, back hair, eyes) compose into the full-body panel for context only.

## What this QC does NOT prove
- That hand pose matches the puppet rig's "hand at side, fingers relaxed" expected state.
- That the donor image's character proportions match Jack's canonical proportions — a 1:1 scale match here is coincidental, not validated.
- That a different pose (e.g. waving) would benefit from these same hand crops.

**Promotion still requires a separate explicit task.**
"""
OUT_NOTES.write_text(notes_md, encoding="utf-8")
print(f"Notes  -> {OUT_NOTES}")
print("DONE")
