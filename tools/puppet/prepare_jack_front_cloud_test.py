"""
Prepare a clean front-view Jack PNG for cloud layer-splitter testing.

Output:
  assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test.png      (chosen format)
  assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test_qc.png   (4-panel QC)
  assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test_white.png  (white-bg fallback)
  assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test_transparent.png (rembg alpha)

Method:
  1. Crop the front-facing full-body Jack from jack_character_sheet_master.png
  2. Run rembg (isnet-anime) for transparent-bg version
  3. Composite onto neutral white for white-bg fallback
  4. Both are written; the script picks the one to use as the canonical upload
     based on a corner-alpha sanity check.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import sys

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT_DIR = PROJECT / r"assets\puppet\cloud_layer_tests\inputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_CANON = OUT_DIR / "jack_front_clean_test.png"
OUT_QC    = OUT_DIR / "jack_front_clean_test_qc.png"
OUT_TRANS = OUT_DIR / "jack_front_clean_test_transparent.png"
OUT_WHITE = OUT_DIR / "jack_front_clean_test_white.png"

cs_matches = list(PROJECT.rglob("jack_character_sheet_master.png"))
if not cs_matches:
    sys.exit("ERROR: jack_character_sheet_master.png not found")
CS_PATH = cs_matches[0]
print(f"Source: {CS_PATH}")

cs = Image.open(CS_PATH).convert("RGBA")
csw, csh = cs.size
print(f"Sheet: {csw}x{csh}")

# Front pose crop. Hand-picked, padded so head fur and shoe shadow are inside.
# The front Jack occupies roughly x=15-305 of the 1536-wide sheet, full vertical.
crop_box = (10, 25, 320, 1015)
front_rgba = cs.crop(crop_box)
front_rgb  = front_rgba.convert("RGB")
fw, fh = front_rgb.size
print(f"Crop box {crop_box}  -> {fw}x{fh}")

# rembg transparent version
print("Running rembg isnet-anime on full body…")
from rembg import remove, new_session
session = new_session("isnet-anime")
trans = remove(front_rgb, session=session)
trans.save(OUT_TRANS)
print(f"Saved: {OUT_TRANS}")

# Compose onto neutral white
white_bg = Image.new("RGBA", trans.size, (255, 255, 255, 255))
white_bg.alpha_composite(trans)
white_bg.convert("RGB").save(OUT_WHITE, format="PNG")
print(f"Saved: {OUT_WHITE}")

# Stats on transparent
arr   = np.array(trans)
total = arr.shape[0] * arr.shape[1]
opaque = int((arr[:, :, 3] == 255).sum())
trans_px = int((arr[:, :, 3] == 0).sum())
semi  = total - opaque - trans_px
corners = [(0,0), (fw-1,0), (0,fh-1), (fw-1,fh-1)]
corner_a = [int(arr[cy, cx, 3]) for cx, cy in corners]
bbox = trans.getbbox()

print(f"  Dimensions:  {fw}x{fh}")
print(f"  Opaque:      {opaque} ({100*opaque/total:.1f}%)")
print(f"  Transparent: {trans_px} ({100*trans_px/total:.1f}%)")
print(f"  Semi-alpha:  {semi} ({100*semi/total:.1f}%)")
print(f"  Corner A:    {corner_a}  (expect [0,0,0,0])")
print(f"  Bbox:        {bbox}")

# Pick canonical: transparent if all corners are 0 and < 5% semi
clean_transparent = all(a == 0 for a in corner_a) and (semi/total < 0.05)
if clean_transparent:
    print("Canonical = TRANSPARENT (rembg cut-out is clean)")
    trans.save(OUT_CANON)
else:
    print("Canonical = WHITE BG (rembg unreliable, falling back to flat white)")
    white_bg.convert("RGB").save(OUT_CANON, format="PNG")

# ── QC sheet (4 panels) ───────────────────────────────────────────────────────
PAD, LBL_H = 14, 22
PW = fw + PAD * 2
PH = fh + PAD * 2 + LBL_H

LIGHT = (210, 210, 210, 255)
DARK  = (40,  40,  40,  255)
LBL_L = (170, 170, 170, 255)
LBL_D = (28,  28,  28,  255)

def make_panel(img, bg, label, lbl_bg, lbl_fg):
    p = Image.new("RGBA", (PW, PH), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0, 0), (PW - 1, LBL_H - 1)], fill=lbl_bg)
    d.text((5, 4), label, fill=lbl_fg)
    if img is not None:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        p.alpha_composite(img, (PAD, LBL_H + PAD))
    return p

p1 = make_panel(front_rgba, (60,60,60,255), "1. Raw crop (with teal bg)", LBL_D, (200,200,200))
p2 = make_panel(trans,      LIGHT,          "2. rembg transparent (light)", LBL_L, (30,30,30))
p3 = make_panel(trans,      DARK,           "3. rembg transparent (dark)",  LBL_D, (200,200,200))
p4 = make_panel(white_bg,   (220,220,220,255), "4. White-bg fallback",      LBL_L, (30,30,30))

# Notes column
NOTES_W = 360
NOTES_H = PH
notes = Image.new("RGBA", (NOTES_W, NOTES_H), (28, 28, 28, 255))
nd = ImageDraw.Draw(notes)
nd.rectangle([(0, 0), (NOTES_W - 1, LBL_H - 1)], fill=LBL_D)
nd.text((5, 4), "5. Notes", fill=(200,200,200))
canonical = "transparent" if clean_transparent else "white-bg"
notes_lines = [
    "Purpose: cloud layer-splitter upload",
    f"Source:  {CS_PATH.name}",
    f"Crop:    {crop_box}",
    f"Size:    {fw} x {fh}",
    f"Canonical chosen: {canonical}",
    "",
    "Files written:",
    f"  {OUT_CANON.name}",
    f"  {OUT_TRANS.name}",
    f"  {OUT_WHITE.name}",
    "",
    "Stats (rembg cut):",
    f"  Opaque:      {100*opaque/total:.1f}%",
    f"  Transparent: {100*trans_px/total:.1f}%",
    f"  Semi-alpha:  {100*semi/total:.1f}%",
    f"  Corners A:   {corner_a}",
    f"  Seg bbox:    {bbox}",
    "",
    "Recommendation:",
    "Try transparent first; if a cloud",
    "tool rejects alpha (some need RGB),",
    "switch to the white-bg version.",
]
yy = LBL_H + 10
for line in notes_lines:
    nd.text((10, yy), line, fill=(190,190,190))
    yy += 15

# Compose: 4 panels in a row + notes column
GAP, OUTER = 8, 10
panels = [p1, p2, p3, p4, notes]
total_w = OUTER * 2 + sum(p.width for p in panels) + GAP * (len(panels) - 1)
total_h = OUTER * 2 + max(p.height for p in panels)
sheet = Image.new("RGB", (total_w, total_h), (15, 15, 15))
x = OUTER
for p in panels:
    sheet.paste(p.convert("RGB"), (x, OUTER))
    x += p.width + GAP
sheet.save(OUT_QC)
print(f"QC sheet -> {OUT_QC}  ({sheet.width}x{sheet.height})")
print("DONE")
