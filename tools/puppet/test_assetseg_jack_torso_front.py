"""
Smoke test: rembg isnet-anime background removal on the front-facing Jack torso region.

Inputs  (read-only):
  - jack_character_sheet_master.png  (found via rglob)
  - assets/puppet/layers_staging/body_r1/jack_torso_front_draft.png  (polygon baseline)

Outputs (all in experiments/ subdirectory — never touches production assets):
  - jack_torso_front_assetseg_test.png   RGBA transparent result
  - jack_torso_front_assetseg_qc.png     6-panel QC sheet

QC panels:
  1. Polygon draft (baseline) on light grey
  2. rembg result on light grey
  3. rembg result on dark grey
  4. rembg result overlaid on original front-Jack context crop
  5. Alpha/mask preview (white = opaque, black = transparent)
  6. Notes: dimensions, alpha stats, method
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import sys

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT     = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT_DIR     = PROJECT / r"assets\puppet\layers_staging\body_r1\experiments"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_TEST    = OUT_DIR / "jack_torso_front_assetseg_test.png"
OUT_QC      = OUT_DIR / "jack_torso_front_assetseg_qc.png"
BASELINE    = PROJECT / r"assets\puppet\layers_staging\body_r1\jack_torso_front_draft.png"

cs_matches  = list(PROJECT.rglob("jack_character_sheet_master.png"))
if not cs_matches:
    sys.exit("ERROR: jack_character_sheet_master.png not found")
CS_PATH = cs_matches[0]

# ── Coordinate helpers (reference space 1536x864 -> actual) ──────────────────
def sx(x, w): return int(x / 1536 * w)
def sy(y, h): return int(y / 864  * h)

# ── Step 1: crop the same torso region used in the polygon extraction ─────────
print("Loading character sheet...")
cs = Image.open(CS_PATH).convert("RGBA")
csw, csh = cs.size

# Identical crop to extract_jack_torso_front_draft.py
crop_box = (sx(82, csw), sy(190, csh), sx(315, csw), sy(437, csh))
torso_crop = cs.crop(crop_box).convert("RGB")   # rembg expects RGB or RGBA
print(f"Crop: {crop_box}  size={torso_crop.size}")

# ── Step 2: rembg background removal with isnet-anime ────────────────────────
print("Running rembg (isnet-anime)... this downloads ~175 MB on first run")
from rembg import remove, new_session
session = new_session("isnet-anime")
result_rgba = remove(torso_crop, session=session)   # returns RGBA PIL image
print(f"rembg done. Result mode={result_rgba.mode}  size={result_rgba.size}")

result_rgba.save(OUT_TEST)
print(f"Saved: {OUT_TEST}")

# ── Step 3: compute stats ─────────────────────────────────────────────────────
arr        = np.array(result_rgba)
total_px   = arr.shape[0] * arr.shape[1]
opaque_px  = int((arr[:, :, 3] == 255).sum())
transp_px  = int((arr[:, :, 3] == 0).sum())
semi_px    = total_px - opaque_px - transp_px
bbox_seg   = result_rgba.getbbox()

corners = [(0, 0), (result_rgba.width - 1, 0),
           (0, result_rgba.height - 1), (result_rgba.width - 1, result_rgba.height - 1)]
corner_alphas = [arr[cy, cx, 3] for cx, cy in corners]

print("-" * 48)
print(f"  Mode:        {result_rgba.mode}")
print(f"  Dimensions:  {result_rgba.width} x {result_rgba.height}")
print(f"  Alpha:       True")
print(f"  Bbox:        {bbox_seg}")
print(f"  Opaque:      {opaque_px} px  ({100*opaque_px/total_px:.1f}%)")
print(f"  Transparent: {transp_px} px  ({100*transp_px/total_px:.1f}%)")
print(f"  Semi-alpha:  {semi_px} px  ({100*semi_px/total_px:.1f}%)")
print(f"  Corners (alpha): {corner_alphas}")
print("-" * 48)

# ── Step 4: load polygon baseline ────────────────────────────────────────────
baseline = None
if BASELINE.exists():
    baseline = Image.open(BASELINE).convert("RGBA")
    print(f"Baseline loaded: {baseline.size}")
else:
    print("WARNING: polygon baseline not found, panel 1 will be blank")

# ── Step 5: build 6-panel QC sheet ───────────────────────────────────────────
rw, rh  = result_rgba.size
PAD     = 16
LBL_H   = 22
PW      = rw + PAD * 2          # panel width
PH      = rh + PAD * 2 + LBL_H  # panel height (includes label strip)

LIGHT   = (210, 210, 210, 255)
DARK    = (50,  50,  50,  255)
BG_DARK = (22,  22,  22,  255)
LBL_BG_L = (170, 170, 170, 255)
LBL_BG_D = (28,  28,  28,  255)

def make_panel(img_rgba, bg_color, label, lbl_bg, lbl_fg):
    p = Image.new("RGBA", (PW, PH), bg_color)
    d = ImageDraw.Draw(p)
    d.rectangle([(0, 0), (PW - 1, LBL_H - 1)], fill=lbl_bg)
    d.text((5, 4), label, fill=lbl_fg)
    if img_rgba is not None:
        p.alpha_composite(img_rgba, (PAD, LBL_H + PAD))
    return p

# Panel 1 — polygon baseline on light grey
p1 = make_panel(
    baseline if baseline else Image.new("RGBA", (rw, rh), (0, 0, 0, 0)),
    LIGHT, "1. Polygon draft (baseline)", LBL_BG_L, (30, 30, 30)
)

# Panel 2 — rembg result on light grey
p2 = make_panel(result_rgba, LIGHT, "2. rembg isnet-anime (light)", LBL_BG_L, (30, 30, 30))

# Panel 3 — rembg result on dark grey
p3 = make_panel(result_rgba, DARK, "3. rembg isnet-anime (dark)", LBL_BG_D, (200, 200, 200))

# Panel 4 — rembg overlaid on original character-sheet context
CTX_L, CTX_T = sx(30, csw),  sy(60, csh)
CTX_R, CTX_B = sx(345, csw), sy(800, csh)
ctx_crop   = cs.crop((CTX_L, CTX_T, CTX_R, CTX_B))
scale_ctx   = PH / ctx_crop.height
ctx_pw      = max(1, int(ctx_crop.width * scale_ctx))
ctx_rs      = ctx_crop.resize((ctx_pw, PH), Image.LANCZOS)
p4          = Image.new("RGBA", (ctx_pw, PH), BG_DARK)
p4.alpha_composite(ctx_rs, (0, 0))
d4 = ImageDraw.Draw(p4)
d4.rectangle([(0, 0), (ctx_pw - 1, LBL_H - 1)], fill=LBL_BG_D)
d4.text((5, 4), "4. rembg overlaid on context", fill=(200, 200, 200))
rel_l = int((sx(82, csw)  - CTX_L) * scale_ctx)
rel_t = int((sy(190, csh) - CTX_T) * scale_ctx) + LBL_H
rel_r = int((sx(315, csw) - CTX_L) * scale_ctx)
rel_b = int((sy(437, csh) - CTX_T) * scale_ctx) + LBL_H
rseg_ctx = result_rgba.resize((rel_r - rel_l, max(1, rel_b - rel_t)), Image.LANCZOS)
p4.alpha_composite(rseg_ctx, (rel_l, rel_t))
d4.rectangle([(rel_l, rel_t), (rel_r, rel_b)], outline=(255, 80, 80), width=2)

# Panel 5 — alpha/mask preview (white = opaque, black = transparent)
alpha_ch  = result_rgba.getchannel("A")
mask_rgb  = Image.merge("RGB", [alpha_ch, alpha_ch, alpha_ch])
mask_rgba = mask_rgb.convert("RGBA")
p5 = make_panel(mask_rgba, (80, 80, 80, 255), "5. Alpha mask (white=opaque)", LBL_BG_D, (200, 200, 200))

# Panel 6 — notes text
NOTES_W = PW
NOTES_H = PH
p6 = Image.new("RGBA", (NOTES_W, NOTES_H), (28, 28, 28, 255))
nd = ImageDraw.Draw(p6)
nd.rectangle([(0, 0), (NOTES_W - 1, LBL_H - 1)], fill=LBL_BG_D)
nd.text((5, 4), "6. Stats & method", fill=(200, 200, 200))
lines = [
    f"Method:      rembg v2.0.75 / isnet-anime",
    f"Python:      3.13 (.venv-assetseg)",
    f"Source:      {CS_PATH.name}",
    f"Crop:        x={sx(82,csw)}-{sx(315,csw)} y={sy(190,csh)}-{sy(437,csh)}",
    f"Dimensions:  {result_rgba.width} x {result_rgba.height}",
    f"Mode:        {result_rgba.mode}",
    f"Alpha:       True",
    f"Bbox:        {bbox_seg}",
    f"Opaque px:   {opaque_px} ({100*opaque_px/total_px:.1f}%)",
    f"Transp px:   {transp_px} ({100*transp_px/total_px:.1f}%)",
    f"Semi-alpha:  {semi_px} ({100*semi_px/total_px:.1f}%)",
    f"Corners:     {corner_alphas}",
    "",
    "Baseline: polygon draft (Pillow mask)",
    f"  file: {BASELINE.name}",
    f"  size: {baseline.size if baseline else 'N/A'}",
]
y_txt = LBL_H + 10
for line in lines:
    nd.text((10, y_txt), line, fill=(190, 190, 190))
    y_txt += 16

# ── Step 6: compose sheet ─────────────────────────────────────────────────────
GAP        = 8
OUTER      = 10
panels_row1 = [p1, p2, p3]
panels_row2 = [p4, p5, p6]

row1_w = sum(p.width for p in panels_row1) + GAP * (len(panels_row1) - 1)
row2_w = sum(p.width for p in panels_row2) + GAP * (len(panels_row2) - 1)
row1_h = max(p.height for p in panels_row1)
row2_h = max(p.height for p in panels_row2)

# Make row 2 panels consistent width (p4 may differ)
p5_wide = Image.new("RGBA", (PW, PH), (28, 28, 28, 255))
p5_wide.alpha_composite(p5)
p6_wide = p6
# re-measure
panels_row2 = [p4, p5, p6_wide]
row2_w = sum(p.width for p in panels_row2) + GAP * 2

total_w = OUTER * 2 + max(row1_w, row2_w)
total_h = OUTER * 2 + row1_h + GAP + row2_h

sheet = Image.new("RGB", (total_w, total_h), (15, 15, 15))

x = OUTER
for p in panels_row1:
    sheet.paste(p.convert("RGB"), (x, OUTER))
    x += p.width + GAP

x = OUTER
for p in panels_row2:
    sheet.paste(p.convert("RGB"), (x, OUTER + row1_h + GAP))
    x += p.width + GAP

sheet.save(OUT_QC)
print(f"QC sheet -> {OUT_QC}")
print(f"Sheet size: {sheet.width} x {sheet.height}")
print("DONE")
