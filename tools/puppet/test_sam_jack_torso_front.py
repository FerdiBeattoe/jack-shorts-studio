"""
Feasibility test: SAM2-tiny (Ultralytics) promptable segmentation on the
front-facing Jack torso region of jack_character_sheet_master.png.

Strict scope:
  - One asset only: jack_torso_front
  - Reads only the character sheet (read-only)
  - Writes only to experiments/
  - Does NOT touch the polygon draft or the rembg smoke-test outputs

Outputs (all under assets/puppet/layers_staging/body_r1/experiments/):
  - jack_torso_front_sam_test.png   RGBA cleaned segmentation
  - jack_torso_front_sam_mask.png   8-bit mask preview
  - jack_torso_front_sam_qc.png     7-panel QC sheet

Method: Ultralytics SAM 'sam2_t.pt' (~150 MB) with a manually-defined bounding
box around the jacket torso region. CPU inference.
"""

from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import sys
import time

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT  = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT_DIR  = PROJECT / r"assets\puppet\layers_staging\body_r1\experiments"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_TEST = OUT_DIR / "jack_torso_front_sam_test.png"
OUT_MASK = OUT_DIR / "jack_torso_front_sam_mask.png"
OUT_QC   = OUT_DIR / "jack_torso_front_sam_qc.png"

BASELINE_POLY  = PROJECT / r"assets\puppet\layers_staging\body_r1\jack_torso_front_draft.png"
BASELINE_REMBG = PROJECT / r"assets\puppet\layers_staging\body_r1\experiments\jack_torso_front_assetseg_test.png"

cs_matches = list(PROJECT.rglob("jack_character_sheet_master.png"))
if not cs_matches:
    sys.exit("ERROR: jack_character_sheet_master.png not found")
CS_PATH = cs_matches[0]

# Reference-space coord helpers (1536 x 864 → actual sheet dims)
def sx(x, w): return int(x / 1536 * w)
def sy(y, h): return int(y / 864  * h)

# ── Step 1: load + same crop as polygon baseline ─────────────────────────────
print(f"Source: {CS_PATH}")
cs = Image.open(CS_PATH).convert("RGBA")
csw, csh = cs.size

crop_box = (sx(82, csw), sy(190, csh), sx(315, csw), sy(437, csh))
torso_crop_rgba = cs.crop(crop_box)
torso_crop_rgb  = torso_crop_rgba.convert("RGB")
cw, ch = torso_crop_rgb.size
print(f"Crop box: {crop_box}  -> {cw}x{ch}")

# ── Step 2: define bbox inside cropped torso ─────────────────────────────────
# Polygon baseline outer extent (in crop coords):
#   left/right shoulder pad: x≈100→292 (full width within crop ≈ 33→237)
#   top: ry=195 (≈6 in crop), bottom: ry=430 (≈278 in crop)
# Use a slightly tighter bbox to discourage SAM from grabbing arms/chin.
def to_crop(x_ref, y_ref):
    ax = sx(x_ref, csw) - crop_box[0]
    ay = sy(y_ref, csh) - crop_box[1]
    return ax, ay

bx1, by1 = to_crop(100, 192)   # left shoulder, just above jacket fabric
bx2, by2 = to_crop(292, 432)   # right waist / belt
# Clamp to crop
bx1 = max(0, min(bx1, cw - 1)); bx2 = max(0, min(bx2, cw - 1))
by1 = max(0, min(by1, ch - 1)); by2 = max(0, min(by2, ch - 1))
bbox_xyxy = [bx1, by1, bx2, by2]
print(f"Prompt bbox (crop coords): {bbox_xyxy}")

# ── Step 3: SAM2-tiny segmentation ───────────────────────────────────────────
from ultralytics import SAM
print("Loading SAM2-tiny (downloads sam2_t.pt ~150 MB on first run)…")
t0 = time.time()
model = SAM("sam2_t.pt")
print(f"Model ready in {time.time()-t0:.1f}s")

# Save a temp RGB to feed the model (ultralytics expects path or array)
torso_arr_rgb = np.array(torso_crop_rgb)
t0 = time.time()
results = model(torso_arr_rgb, bboxes=[bbox_xyxy], verbose=False)
print(f"Inference in {time.time()-t0:.1f}s")

if not results or results[0].masks is None or len(results[0].masks.data) == 0:
    sys.exit("ERROR: SAM returned no masks")

# masks.data: tensor [N, H, W] in [0,1]; take the first (best) mask
raw_mask = results[0].masks.data[0].cpu().numpy()
if raw_mask.shape != (ch, cw):
    # ultralytics sometimes returns 1024x1024; resize to crop dims
    raw_mask_img = Image.fromarray((raw_mask * 255).astype(np.uint8), mode="L").resize((cw, ch), Image.BILINEAR)
    raw_mask = np.array(raw_mask_img).astype(np.float32) / 255.0
print(f"Raw mask shape: {raw_mask.shape}  unique min/max={raw_mask.min():.3f}/{raw_mask.max():.3f}")

# ── Step 4: deterministic alpha cleanup ──────────────────────────────────────
alpha = (raw_mask * 255).astype(np.uint8)

# Threshold low/high
alpha[alpha < 30]  = 0
alpha[alpha > 220] = 255

# Remove tiny disconnected fragments (keep components ≥ 0.5% of crop area)
import cv2
binary = (alpha > 0).astype(np.uint8) * 255
n_comp, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
min_area = max(50, int(0.005 * cw * ch))
keep = np.zeros_like(binary)
kept_components = 0
for i in range(1, n_comp):
    if stats[i, cv2.CC_STAT_AREA] >= min_area:
        keep[labels == i] = 255
        kept_components += 1
alpha = np.where(keep > 0, alpha, 0).astype(np.uint8)
print(f"Connected components: {n_comp-1} total, {kept_components} kept (min_area={min_area})")

# Compose RGBA output
rgb_arr = np.array(torso_crop_rgb)
result_rgba = np.dstack([rgb_arr, alpha])
result_img  = Image.fromarray(result_rgba, mode="RGBA")
result_img.save(OUT_TEST)
print(f"Saved: {OUT_TEST}")

mask_img = Image.fromarray(alpha, mode="L")
mask_img.save(OUT_MASK)
print(f"Saved: {OUT_MASK}")

# ── Step 5: stats ────────────────────────────────────────────────────────────
total_px  = alpha.size
opaque_px = int((alpha == 255).sum())
transp_px = int((alpha == 0).sum())
semi_px   = total_px - opaque_px - transp_px
bbox_seg  = result_img.getbbox()
corners   = [(0,0), (cw-1,0), (0,ch-1), (cw-1,ch-1)]
corner_a  = [int(alpha[cy, cx]) for cx, cy in corners]

# Region presence checks (qualitative):
# - chin would appear above by1 → outside bbox = no chin
# - legs would appear below by2 → outside bbox = no legs
# Verify alpha is zero outside bbox vertically
above_bbox_alpha = int(alpha[:max(0, by1-2), :].sum())
below_bbox_alpha = int(alpha[min(ch-1, by2+2):, :].sum())

print("-" * 56)
print(f"  Mode:        RGBA")
print(f"  Dimensions:  {cw} x {ch}")
print(f"  Alpha:       True")
print(f"  Bbox seg:    {bbox_seg}")
print(f"  Opaque:      {opaque_px} px  ({100*opaque_px/total_px:.1f}%)")
print(f"  Transparent: {transp_px} px  ({100*transp_px/total_px:.1f}%)")
print(f"  Semi-alpha:  {semi_px} px  ({100*semi_px/total_px:.1f}%)")
print(f"  Corners A:   {corner_a}")
print(f"  Above-bbox alpha sum: {above_bbox_alpha}  (expect 0 → no chin)")
print(f"  Below-bbox alpha sum: {below_bbox_alpha}  (expect 0 → no legs)")
print("-" * 56)

# ── Step 6: build 7-panel QC sheet ───────────────────────────────────────────
PAD, LBL_H = 16, 22
PW = cw + PAD * 2
PH = ch + PAD * 2 + LBL_H

LIGHT  = (210, 210, 210, 255)
DARK   = (50,  50,  50,  255)
BG_DK  = (22,  22,  22,  255)
LBL_L  = (170, 170, 170, 255)
LBL_D  = (28,  28,  28,  255)

def make_panel(img_rgba, bg, label, lbl_bg, lbl_fg, w=PW, h=PH):
    p = Image.new("RGBA", (w, h), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0, 0), (w - 1, LBL_H - 1)], fill=lbl_bg)
    d.text((5, 4), label, fill=lbl_fg)
    if img_rgba is not None:
        # center image inside panel
        ox = (w - img_rgba.width) // 2
        oy = LBL_H + (h - LBL_H - img_rgba.height) // 2
        p.alpha_composite(img_rgba, (max(0, ox), max(LBL_H, oy)))
    return p

# Load baselines
poly_img = Image.open(BASELINE_POLY).convert("RGBA")   if BASELINE_POLY.exists()  else None
remb_img = Image.open(BASELINE_REMBG).convert("RGBA")  if BASELINE_REMBG.exists() else None

# Panel 1 — polygon draft on light
p1 = make_panel(poly_img,    LIGHT, "1. Polygon draft (light)", LBL_L, (30,30,30))
# Panel 2 — rembg on light
p2 = make_panel(remb_img,    LIGHT, "2. rembg isnet-anime (light)", LBL_L, (30,30,30))
# Panel 3 — SAM on light
p3 = make_panel(result_img,  LIGHT, "3. SAM2-tiny (light)", LBL_L, (30,30,30))
# Panel 4 — SAM on dark
p4 = make_panel(result_img,  DARK,  "4. SAM2-tiny (dark)",  LBL_D, (200,200,200))

# Panel 5 — SAM overlaid on original character-sheet context crop
CTX_L, CTX_T = sx(30, csw),  sy(60, csh)
CTX_R, CTX_B = sx(345, csw), sy(800, csh)
ctx_crop = cs.crop((CTX_L, CTX_T, CTX_R, CTX_B))
scale_ctx = PH / ctx_crop.height
ctx_pw    = max(1, int(ctx_crop.width * scale_ctx))
ctx_rs    = ctx_crop.resize((ctx_pw, PH), Image.LANCZOS)
p5 = Image.new("RGBA", (ctx_pw, PH), BG_DK)
p5.alpha_composite(ctx_rs, (0, 0))
d5 = ImageDraw.Draw(p5)
d5.rectangle([(0, 0), (ctx_pw - 1, LBL_H - 1)], fill=LBL_D)
d5.text((5, 4), "5. SAM overlaid on original pose", fill=(200,200,200))
rel_l = int((crop_box[0] - CTX_L) * scale_ctx)
rel_t = int((crop_box[1] - CTX_T) * scale_ctx) + LBL_H
rel_r = int((crop_box[2] - CTX_L) * scale_ctx)
rel_b = int((crop_box[3] - CTX_T) * scale_ctx) + LBL_H
seg_rs = result_img.resize((max(1, rel_r-rel_l), max(1, rel_b-rel_t)), Image.LANCZOS)
p5.alpha_composite(seg_rs, (rel_l, rel_t))
d5.rectangle([(rel_l, rel_t), (rel_r, rel_b)], outline=(255,80,80), width=2)

# Panel 6 — SAM mask preview
mask_rgb = Image.merge("RGB", [mask_img, mask_img, mask_img]).convert("RGBA")
p6 = make_panel(mask_rgb, (80,80,80,255), "6. SAM alpha mask", LBL_D, (200,200,200))

# Panel 7 — notes
NOTES_W = max(PW, 380)
NOTES_H = PH
p7 = Image.new("RGBA", (NOTES_W, NOTES_H), (28, 28, 28, 255))
nd = ImageDraw.Draw(p7)
nd.rectangle([(0, 0), (NOTES_W - 1, LBL_H - 1)], fill=LBL_D)
nd.text((5, 4), "7. Notes / stats", fill=(200,200,200))

# Visual recommendation heuristic
total_baseline_opaque = None
if poly_img is not None:
    pa = np.array(poly_img)[:, :, 3]
    total_baseline_opaque = int((pa > 0).sum())
recommend = "SAM" if (opaque_px > 0 and below_bbox_alpha == 0 and above_bbox_alpha == 0 and semi_px/total_px < 0.08) else "polygon"
notes = [
    "Method:      Ultralytics SAM2-tiny (sam2_t.pt)",
    "Device:      CPU (torch 2.12 cpu)",
    "Venv:        .venv-sam (Python 3.11)",
    f"Source:      {CS_PATH.name}",
    f"Crop box:    x={crop_box[0]}-{crop_box[2]} y={crop_box[1]}-{crop_box[3]}",
    f"Bbox prompt: {bbox_xyxy} (crop coords)",
    f"Dimensions:  {cw} x {ch}",
    f"Image mode:  RGBA",
    f"Alpha:       True",
    f"Seg bbox:    {bbox_seg}",
    f"Opaque:      {opaque_px} ({100*opaque_px/total_px:.1f}%)",
    f"Transparent: {transp_px} ({100*transp_px/total_px:.1f}%)",
    f"Semi-alpha:  {semi_px} ({100*semi_px/total_px:.1f}%)",
    f"Corners A:   {corner_a}  (expect [0,0,0,0])",
    f"Above-bbox:  {above_bbox_alpha}  (expect 0 → no chin)",
    f"Below-bbox:  {below_bbox_alpha}  (expect 0 → no legs/crotch)",
    f"Components:  kept {kept_components}",
    "",
    "Post-process: a<30→0, a>220→255, tiny CC removed",
    "",
    f"Recommendation: {recommend}",
]
yy = LBL_H + 10
for line in notes:
    nd.text((10, yy), line, fill=(190, 190, 190))
    yy += 15

# ── Compose sheet (3 panels per row × 3 rows; 7 panels + 2 blanks) ───────────
GAP, OUTER = 8, 10
row1 = [p1, p2, p3]
row2 = [p4, p5, p6]
row3 = [p7]

def row_dims(row):
    return sum(p.width for p in row) + GAP*(len(row)-1), max(p.height for p in row)

w1, h1 = row_dims(row1)
w2, h2 = row_dims(row2)
w3, h3 = row_dims(row3)

total_w = OUTER*2 + max(w1, w2, w3)
total_h = OUTER*2 + h1 + GAP + h2 + GAP + h3

sheet = Image.new("RGB", (total_w, total_h), (15, 15, 15))

def paste_row(row, y):
    x = OUTER
    for p in row:
        sheet.paste(p.convert("RGB"), (x, y))
        x += p.width + GAP

paste_row(row1, OUTER)
paste_row(row2, OUTER + h1 + GAP)
paste_row(row3, OUTER + h1 + GAP + h2 + GAP)

sheet.save(OUT_QC)
print(f"QC sheet -> {OUT_QC}")
print(f"Sheet size: {sheet.width} x {sheet.height}")
print("DONE")
