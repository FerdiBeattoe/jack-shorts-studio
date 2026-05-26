"""
Extract Jack's two paw/hands from the hands-visible donor image.
Deterministic Pillow + numpy only; no AI, no cloud.

Input:
  assets/puppet/cloud_layer_tests/inputs/jack_front_hands_visible_r1.png

Outputs (assets/puppet/layers_staging/hands_r1/):
  jack_hand_left_r1.png            RGBA, transparent, character's LEFT hand
  jack_hand_right_r1.png           RGBA, transparent, character's RIGHT hand
  jack_hands_r1_visual_qc.png      4-panel QC
  hand_extraction_manifest.json    bboxes, stats, naming convention
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json
import sys

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
SRC = PROJECT / r"assets\puppet\cloud_layer_tests\inputs\jack_front_hands_visible_r1.png"
OUT = PROJECT / r"assets\puppet\layers_staging\hands_r1"
OUT.mkdir(parents=True, exist_ok=True)

OUT_L  = OUT / "jack_hand_left_r1.png"
OUT_R  = OUT / "jack_hand_right_r1.png"
OUT_QC = OUT / "jack_hands_r1_visual_qc.png"
OUT_MF = OUT / "hand_extraction_manifest.json"

# Optional: See-through topwear layer for QC overlay
SEETHRU_TOP = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted\04_topwear.png"

if not SRC.exists():
    sys.exit(f"ERROR: {SRC} not found")

print(f"Source: {SRC}")
src = Image.open(SRC).convert("RGB")
W, H = src.size
print(f"Size: {W}x{H}")
arr = np.array(src)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

# ── Background detection (corner sample) ─────────────────────────────────────
corners = np.stack([arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]])
bg = corners.mean(axis=0).astype(int)
print(f"Background sample (mean of corners): {bg.tolist()}")

# Foreground = NOT background-grey (tolerance 18)
TOL = 18
fg_mask = ~((np.abs(arr.astype(int) - bg) < TOL).all(axis=-1))
print(f"Foreground pixels (anti-bg): {int(fg_mask.sum())}")

# ── Locate hand clusters via golden-fur in cuff band ─────────────────────────
gold_mask = (r > 180) & (g > 120) & (g < 210) & (b < 140) & (b > 40)
# Hands are below the head; the head fur ends around y≈400.
# Restrict gold search to y >= 700 to isolate paws from face/neck/tail-fur.
CUFF_Y0, CUFF_Y1 = 700, 1050
band_gold = np.zeros_like(gold_mask)
band_gold[CUFF_Y0:CUFF_Y1] = gold_mask[CUFF_Y0:CUFF_Y1]
print(f"Golden-fur pixels in cuff band y[{CUFF_Y0}-{CUFF_Y1}]: {int(band_gold.sum())}")

# Connected components on the cuff-band gold mask
import cv2
binary = (band_gold.astype(np.uint8)) * 255
n_comp, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
clusters = []
for ci in range(1, n_comp):
    x, y, w, h, area = stats[ci]
    if area < 200:
        continue
    clusters.append((ci, x, y, w, h, area, centroids[ci][0]))
clusters.sort(key=lambda c: c[6])  # by centroid x → image-left first
print(f"Candidate hand clusters (area>=200): {len(clusters)}")
for c in clusters:
    print(f"  comp={c[0]} bbox=({c[1]},{c[2]},{c[1]+c[3]},{c[2]+c[4]}) area={c[5]}")

if len(clusters) < 2:
    sys.exit("ERROR: expected 2 hand clusters, found fewer. Aborting.")

# Take the largest two by area; if more than 2, pick the two with lowest centroid_y? Actually two largest.
clusters.sort(key=lambda c: c[5], reverse=True)
hands = clusters[:2]
hands.sort(key=lambda c: c[6])  # left then right (image-left first)
print("Selected hands:")
for h in hands:
    print(f"  comp={h[0]} bbox=({h[1]},{h[2]},{h[1]+h[3]},{h[2]+h[4]}) area={h[5]} cx={h[6]:.0f}")

# ── For each hand, expand bbox to include cuff edge & paw outline ────────────
PAD = 14  # pixels padding around bbox

def crop_hand(ci, x, y, w, h):
    x0 = max(0, x - PAD); y0 = max(0, y - PAD)
    x1 = min(W, x + w + PAD); y1 = min(H, y + h + PAD)
    # Build hand mask within this bbox = fg_mask AND connected to the gold component (8-conn flood)
    # Approach: take fg_mask in bbox, then keep only CC that overlaps the gold component pixels.
    sub_fg = fg_mask[y0:y1, x0:x1].astype(np.uint8) * 255
    sub_gold_cc = (labels[y0:y1, x0:x1] == ci).astype(np.uint8) * 255
    # CC of foreground in bbox
    nfg, fglabels, fstats, _ = cv2.connectedComponentsWithStats(sub_fg, connectivity=8)
    keep = np.zeros_like(sub_fg)
    # Find which fg-CC labels contain any gold pixel
    overlap_labels = set(np.unique(fglabels[sub_gold_cc > 0])) - {0}
    for lbl in overlap_labels:
        keep[fglabels == lbl] = 255
    # Compose RGBA crop
    rgb_crop = arr[y0:y1, x0:x1]
    rgba = np.dstack([rgb_crop, keep])
    return Image.fromarray(rgba, mode="RGBA"), (x0, y0, x1, y1)

(ci_l, lx, ly, lw, lh, larea, lcx) = hands[0]
(ci_r, rx, ry, rw, rh, rarea, rcx) = hands[1]

img_left_in_image,  bbox_l_image = crop_hand(ci_l, lx, ly, lw, lh)
img_right_in_image, bbox_r_image = crop_hand(ci_r, rx, ry, rw, rh)
print(f"Image-left  hand crop:  {img_left_in_image.size}  bbox={bbox_l_image}")
print(f"Image-right hand crop:  {img_right_in_image.size}  bbox={bbox_r_image}")

# Anatomy mapping: image-left = character's RIGHT hand (mirror).
# OUTPUT FILENAME CONVENTION (user-specified): hand_left / hand_right.
# We map to CHARACTER anatomy (rig-friendly):
#   jack_hand_left_r1.png  = character's left hand  = image-RIGHT
#   jack_hand_right_r1.png = character's right hand = image-LEFT
char_left_img    = img_right_in_image
char_left_bbox   = bbox_r_image
char_right_img   = img_left_in_image
char_right_bbox  = bbox_l_image

char_left_img.save(OUT_L)
char_right_img.save(OUT_R)
print(f"Saved: {OUT_L}")
print(f"Saved: {OUT_R}")

# Stats per hand
def stats_of(img):
    a = np.array(img)[:, :, 3]
    total = a.size
    op = int((a == 255).sum())
    tr = int((a == 0).sum())
    semi = total - op - tr
    return {"width": int(img.width), "height": int(img.height),
            "opaque_pct": round(100*op/total, 2),
            "transparent_pct": round(100*tr/total, 2),
            "semi_alpha_pct": round(100*semi/total, 2),
            "bbox_in_layer": list(img.getbbox()) if img.getbbox() else None}

manifest = {
    "source": str(SRC),
    "source_size": [W, H],
    "background_color_sample": bg.tolist(),
    "background_tolerance": TOL,
    "cuff_band_y": [CUFF_Y0, CUFF_Y1],
    "method": "golden-fur cluster → 8-connectivity foreground-CC overlap → RGBA crop",
    "naming_convention": "character anatomy (left = character's left = image-right)",
    "outputs": {
        "jack_hand_left_r1.png":  {"bbox_in_source": list(char_left_bbox),  **stats_of(char_left_img)},
        "jack_hand_right_r1.png": {"bbox_in_source": list(char_right_bbox), **stats_of(char_right_img)},
    },
    "promotion_status": "STAGING_ONLY — donor pose, not master design",
}
def _jsonable(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.ndarray,)):  return o.tolist()
    raise TypeError(f"not jsonable: {type(o)}")
OUT_MF.write_text(json.dumps(manifest, indent=2, default=_jsonable))
print(f"Manifest: {OUT_MF}")

# ── QC sheet (4 panels) ──────────────────────────────────────────────────────
PAD_P, LBL_H = 12, 22

# Panel 1: shrunk source
src_thumb_h = 700
src_thumb_w = int(W * src_thumb_h / H)
src_thumb = src.resize((src_thumb_w, src_thumb_h), Image.LANCZOS).convert("RGBA")
# Box overlays for hand bboxes
sd = ImageDraw.Draw(src_thumb)
def scaled(b, scale):
    return (int(b[0]*scale), int(b[1]*scale), int(b[2]*scale), int(b[3]*scale))
scale = src_thumb_h / H
sd.rectangle(scaled(char_left_bbox, scale),  outline=(80,255,80), width=3)
sd.rectangle(scaled(char_right_bbox, scale), outline=(255,80,80), width=3)
sd.text((6, 4),  "1. Source (green=L, red=R, character anatomy)", fill=(255,255,255))

# Panels 2,3: hands on light grey
def panel_with_label(img, label, bg_color, w=None, h=None):
    pw = (w if w else img.width) + PAD_P*2
    ph = (h if h else img.height) + PAD_P*2 + LBL_H
    p = Image.new("RGBA", (pw, ph), bg_color)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(pw-1,LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    cx = (pw - img.width)//2
    cy = LBL_H + (ph - LBL_H - img.height)//2
    p.alpha_composite(img, (max(0,cx), max(LBL_H,cy)))
    return p

# Make all hand panels same size for tidy layout
maxhw = max(char_left_img.width, char_right_img.width)
maxhh = max(char_left_img.height, char_right_img.height)
p2 = panel_with_label(char_left_img,  "2. jack_hand_left_r1 (character L)",  (200,200,200,255), w=maxhw, h=maxhh)
p3 = panel_with_label(char_right_img, "3. jack_hand_right_r1 (character R)", (200,200,200,255), w=maxhw, h=maxhh)

# Panel 4: hands placed near topwear if available
topwear_available = SEETHRU_TOP.exists()
if topwear_available:
    top = Image.open(SEETHRU_TOP).convert("RGBA")
    # Topwear bbox: x in 314-505, y in 152-423 (See-through 768x768 canvas)
    # Pull topwear bbox to know placement zone
    talp = np.array(top)[:, :, 3]
    tb = top.getbbox() or (0, 0, top.width, top.height)
    # Build composite canvas: topwear on light bg, hands placed roughly at sleeve cuff y
    canvas_h = max(top.height, maxhh + 200)
    canvas_w = top.width + maxhw + 60
    p4 = Image.new("RGBA", (canvas_w, canvas_h + LBL_H), (210,210,210,255))
    d4 = ImageDraw.Draw(p4)
    d4.rectangle([(0,0),(canvas_w-1,LBL_H-1)], fill=(50,50,50,255))
    d4.text((5,4), "4. Hands beside See-through topwear (rough placement)", fill=(220,220,220))
    p4.alpha_composite(top, (0, LBL_H))
    # Place character-left hand to the LEFT side of topwear (image left), char-right to image right
    # Topwear sleeve bottom is approx y=420 in 768-canvas
    sleeve_y = LBL_H + 380
    p4.alpha_composite(char_right_img.resize((maxhw//2, maxhh//2)), (10, sleeve_y))     # image-left = char R
    p4.alpha_composite(char_left_img.resize((maxhw//2, maxhh//2)),  (top.width - 10, sleeve_y))  # image-right = char L
    d4.text((10, sleeve_y - 14), "char R", fill=(140,30,30))
    d4.text((top.width + 4, sleeve_y - 14), "char L", fill=(30,140,30))
else:
    # Fallback: skip overlay
    p4 = Image.new("RGBA", (maxhw + PAD_P*2, maxhh + PAD_P*2 + LBL_H), (28,28,28,255))
    d4 = ImageDraw.Draw(p4)
    d4.rectangle([(0,0),(p4.width-1,LBL_H-1)], fill=(50,50,50,255))
    d4.text((5,4), "4. (no topwear layer found — skipped)", fill=(220,220,220))

# Wrap panel 1 with label header
p1 = Image.new("RGBA", (src_thumb_w, src_thumb_h), (200,200,200,255))
p1.alpha_composite(src_thumb, (0,0))

# Compose sheet: row1 = [p1], row2 = [p2, p3, p4]
GAP, OUTER = 10, 12
row2_w = p2.width + GAP + p3.width + GAP + p4.width
row2_h = max(p2.height, p3.height, p4.height)
sheet_w = OUTER*2 + max(p1.width, row2_w)
sheet_h = OUTER*2 + p1.height + GAP + row2_h
sheet = Image.new("RGB", (sheet_w, sheet_h), (15,15,15))
sheet.paste(p1.convert("RGB"), (OUTER, OUTER))
x = OUTER
y = OUTER + p1.height + GAP
for p in [p2, p3, p4]:
    sheet.paste(p.convert("RGB"), (x, y))
    x += p.width + GAP
sheet.save(OUT_QC)
print(f"QC sheet -> {OUT_QC}  ({sheet.width}x{sheet.height})")
print("DONE")
