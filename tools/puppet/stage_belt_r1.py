"""
Stage CoPainter belt (layer_77.png) for the Jack puppet rig.

Source:
  assets/puppet/cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_77.png

Outputs (assets/puppet/layers_staging/belt_r1/):
  jack_belt_r1.png                       bbox-cropped RGBA (pixel-identical to source)
  jack_belt_r1_full_canvas_test.png      placed on See-through 768x768 canvas at derived waist anchor
  jack_belt_r1_visual_qc.png             5-panel visual QC
  jack_belt_r1_composite_qc.png          rough full-body composite using See-through + belt
  belt_r1_manifest.json                  anchor / scale / alpha / SHA
  belt_r1_notes.md                       (written by separate notes step)

Anchor derivation:
  CoPainter ZIP has no origin metadata, so we anchor visually using See-through
  layer geometry: topwear bbox (314,152,505,423) and legwear bbox (310,364,504,641)
  overlap in y=364-423 — Jack's waist. Body centerline x = midpoint of those
  bboxes. The belt is placed centered horizontally and at the midpoint of the
  jacket/pants overlap.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, hashlib

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
SRC     = PROJECT / r"assets\puppet\cloud_layer_tests\copainter\extracted_layers_1779216312185\layer_77.png"
OUT     = PROJECT / r"assets\puppet\layers_staging\belt_r1"
SEETHRU = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
ST_MAN  = SEETHRU / "layer_manifest.json"
OUT.mkdir(parents=True, exist_ok=True)

assert SRC.exists(), f"{SRC} not found"

# ── Load source belt (pixel-preserve copy) ──────────────────────────────────
belt_src = Image.open(SRC).convert("RGBA")
BW, BH = belt_src.size
print(f"Source belt: {BW}x{BH}")

# Pixel-identical copy out (no resave path round-trip): use bytes copy
import shutil
DST_BBOX = OUT / "jack_belt_r1.png"
shutil.copyfile(SRC, DST_BBOX)
src_sha = hashlib.sha256(SRC.read_bytes()).hexdigest()
dst_sha = hashlib.sha256(DST_BBOX.read_bytes()).hexdigest()
assert src_sha == dst_sha, "byte-identity check failed"
print(f"Bbox-cropped belt -> {DST_BBOX.name}  sha256={dst_sha[:16]}... (byte-identical)")

# ── See-through canvas geometry → derive waist anchor ──────────────────────
mani = json.loads(ST_MAN.read_text())
CW, CH = mani["canvas"]
def L(name): return next((x for x in mani["layers"] if x.get("name") == name), None)
tw = L("topwear"); lw = L("legwear"); hw = L("handwear")
print(f"See-through canvas {CW}x{CH}  topwear bbox {tw['bbox']}  legwear bbox {lw['bbox']}")

# Body centerline (avg of topwear + legwear bbox horizontal centers)
tx_c = (tw["bbox"][0] + tw["bbox"][2]) / 2
lx_c = (lw["bbox"][0] + lw["bbox"][2]) / 2
WAIST_CX = round((tx_c + lx_c) / 2)
# Waist Y = midpoint of the overlap between topwear bottom and legwear top
overlap_top    = lw["bbox"][1]   # legwear y0 = 364
overlap_bottom = tw["bbox"][3]   # topwear y1 = 423
WAIST_CY = round((overlap_top + overlap_bottom) / 2)
print(f"Waist centerline (See-through canvas): ({WAIST_CX}, {WAIST_CY})  overlap y={overlap_top}-{overlap_bottom}")

# Belt scale from CoPainter → See-through:
# CoPainter jacket (269x390) maps to See-through topwear bbox (191x271).
# Use that ratio (≈0.71) for all CoPainter→See-through transfers.
COPAINTER_JACKET_W = 269
SEETHRU_TOPWEAR_W  = tw["bbox"][2] - tw["bbox"][0]   # 191
BELT_SCALE = SEETHRU_TOPWEAR_W / COPAINTER_JACKET_W
print(f"Belt scale (CoPainter -> See-through): {BELT_SCALE:.4f}")

BELT_W_SCALED = max(1, int(BW * BELT_SCALE))
BELT_H_SCALED = max(1, int(BH * BELT_SCALE))
print(f"Belt at See-through scale: {BELT_W_SCALED}x{BELT_H_SCALED}")
belt_scaled = belt_src.resize((BELT_W_SCALED, BELT_H_SCALED), Image.LANCZOS)

# Place on See-through 768 canvas (full-canvas test)
BELT_TL = (WAIST_CX - BELT_W_SCALED // 2, WAIST_CY - BELT_H_SCALED // 2)
fc_canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
fc_canvas.alpha_composite(belt_scaled, BELT_TL)
DST_FC = OUT / "jack_belt_r1_full_canvas_test.png"
fc_canvas.save(DST_FC)
print(f"Full-canvas test -> {DST_FC.name}  belt at TL={BELT_TL}")

# ── Build See-through full body (back-to-front) for context ────────────────
def place_st(name):
    info = L(name)
    if info is None or not info.get("png"): return None
    img = Image.open(SEETHRU / info["png"]).convert("RGBA")
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    c.alpha_composite(img, (info["bbox"][0], info["bbox"][1]))
    return c

ST_DRAW = ["back hair", "ears", "face", "eyebrow", "eyewhite", "irides",
           "legwear", "footwear", "handwear", "topwear"]
st_body = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
for n in ST_DRAW:
    layer = place_st(n)
    if layer is not None: st_body.alpha_composite(layer)

# Body + belt composite
st_body_belt = st_body.copy()
st_body_belt.alpha_composite(belt_scaled, BELT_TL)
print("Body + belt composite built")

# Body topwear + belt only (for QC panel 2)
topwear_canvas = place_st("topwear")
topwear_belt = topwear_canvas.copy()
topwear_belt.alpha_composite(belt_scaled, BELT_TL)

# Legwear + belt only (panel 3)
legwear_canvas = place_st("legwear")
legwear_belt = legwear_canvas.copy()
legwear_belt.alpha_composite(belt_scaled, BELT_TL)

# ── QC panels ──────────────────────────────────────────────────────────────
PAD, LBL_H = 10, 22

def panel(img, label, bg=(210, 210, 210, 255), max_w=None):
    if max_w and img.width > max_w:
        s = max_w / img.width
        img = img.resize((max_w, int(img.height * s)), Image.LANCZOS)
    p = Image.new("RGBA", (img.width + 20, img.height + LBL_H + 16), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    p.alpha_composite(img, (10, LBL_H + 8))
    return p

# Panel 1: isolated belt (zoomed)
zoom = 4
belt_zoom = belt_src.resize((BW * zoom, BH * zoom), Image.NEAREST)
# Place on light grey + dark grey side-by-side for alpha sanity
belt_light = Image.new("RGBA", belt_zoom.size, (210, 210, 210, 255))
belt_light.alpha_composite(belt_zoom)
belt_dark  = Image.new("RGBA", belt_zoom.size, (40, 40, 40, 255))
belt_dark.alpha_composite(belt_zoom)
belt_pair  = Image.new("RGBA", (belt_zoom.width * 2 + 10, belt_zoom.height), (15,15,15,255))
belt_pair.alpha_composite(belt_light, (0, 0))
belt_pair.alpha_composite(belt_dark,  (belt_zoom.width + 10, 0))
p1 = panel(belt_pair, f"1. Isolated belt (4x zoom, light | dark) - {BW}x{BH} RGBA  max_alpha={np.array(belt_src)[...,3].max()}")

# Panel 2: belt over See-through topwear (waist crop)
zoom_box = (max(0, tw["bbox"][0]-30), max(0, tw["bbox"][3]-60),
            min(CW, tw["bbox"][2]+30), min(CH, lw["bbox"][1]+90))
tw_belt_crop = topwear_belt.crop(zoom_box)
tw_belt_crop_up = tw_belt_crop.resize((tw_belt_crop.width * 2, tw_belt_crop.height * 2), Image.NEAREST)
p2 = panel(tw_belt_crop_up, "2. Belt over See-through topwear (waist zoom)")

# Panel 3: belt over See-through legwear
lw_belt_crop = legwear_belt.crop(zoom_box)
lw_belt_crop_up = lw_belt_crop.resize((lw_belt_crop.width * 2, lw_belt_crop.height * 2), Image.NEAREST)
p3 = panel(lw_belt_crop_up, "3. Belt over See-through legwear (waist zoom)")

# Panel 4: full body composite with belt (full canvas, scaled to fit)
fb_w = 360
fb_scale = fb_w / CW
fb_thumb = st_body_belt.resize((fb_w, int(CH * fb_scale)), Image.LANCZOS)
fb_bg = Image.new("RGBA", fb_thumb.size, (210, 210, 210, 255))
fb_bg.alpha_composite(fb_thumb)
p4 = panel(fb_bg, "4. Full body composite (See-through + belt)")

# Panel 5: zoomed waist before/after belt
before = topwear_canvas.copy()
before.alpha_composite(legwear_canvas)
before_crop = before.crop(zoom_box)
after_crop = st_body_belt.crop(zoom_box)
zoom2 = 3
before_up = before_crop.resize((before_crop.width * zoom2, before_crop.height * zoom2), Image.NEAREST)
after_up  = after_crop.resize((after_crop.width  * zoom2, after_crop.height  * zoom2), Image.NEAREST)
ba_w = before_up.width + after_up.width + 10
ba = Image.new("RGBA", (ba_w, before_up.height), (210, 210, 210, 255))
ba.alpha_composite(before_up, (0, 0))
ba.alpha_composite(after_up,  (before_up.width + 10, 0))
# Label divider
bd = ImageDraw.Draw(ba)
bd.text((10, 6), "BEFORE", fill=(180, 30, 30))
bd.text((before_up.width + 16, 6), "AFTER", fill=(30, 130, 30))
p5 = panel(ba, "5. Waist zoom: before | after belt placement")

# Notes column
NW, NH = 380, max(p2.height, 300)
notes_panel = Image.new("RGBA", (NW, NH), (28, 28, 28, 255))
nd = ImageDraw.Draw(notes_panel)
nd.rectangle([(0,0),(NW-1, LBL_H-1)], fill=(50,50,50,255))
nd.text((5, 4), "Anchor / scale notes", fill=(220,220,220))
arr = np.array(belt_src); ach = arr[...,3]
notes_lines = [
    f"Source: layer_77.png (CoPainter)",
    f"Bbox size: {BW} x {BH}",
    f"Max alpha: {ach.max()} (CoPainter max ~254)",
    f"a>=200: {100*(ach>=200).sum()/ach.size:.1f}%",
    "",
    f"See-through canvas: {CW} x {CH}",
    f"Topwear bbox: {tw['bbox']}",
    f"Legwear bbox: {lw['bbox']}",
    f"Overlap y: {overlap_top}-{overlap_bottom}",
    "",
    f"Waist anchor (canvas):",
    f"  x = {WAIST_CX}  (body centerline)",
    f"  y = {WAIST_CY}  (overlap midpoint)",
    "",
    f"Belt scale (CoPainter -> ST):",
    f"  {BELT_SCALE:.4f}",
    f"  scaled size {BELT_W_SCALED}x{BELT_H_SCALED}",
    f"  placed at TL = {BELT_TL}",
    "",
    "Pixel-identical bbox PNG:",
    f"  sha256[:16] = {dst_sha[:16]}",
]
yy = LBL_H + 10
for line in notes_lines:
    nd.text((10, yy), line, fill=(190,190,190))
    yy += 14

# Compose Visual QC sheet
visual_row1 = p1
visual_row2 = [p2, p3, p5]
visual_row3 = [p4, notes_panel]

GAP, OUTER = 10, 12
r1_w = visual_row1.width
r2_w = sum(p.width for p in visual_row2) + GAP*(len(visual_row2)-1)
r3_w = sum(p.width for p in visual_row3) + GAP*(len(visual_row3)-1)
sheet_w = OUTER*2 + max(r1_w, r2_w, r3_w)
r2_h = max(p.height for p in visual_row2)
r3_h = max(p.height for p in visual_row3)
sheet_h = OUTER*2 + visual_row1.height + GAP + r2_h + GAP + r3_h

vsheet = Image.new("RGB", (sheet_w, sheet_h), (15,15,15))
vsheet.paste(visual_row1.convert("RGB"), (OUTER, OUTER))
x = OUTER; y = OUTER + visual_row1.height + GAP
for p in visual_row2:
    vsheet.paste(p.convert("RGB"), (x, y)); x += p.width + GAP
x = OUTER; y = OUTER + visual_row1.height + GAP + r2_h + GAP
for p in visual_row3:
    vsheet.paste(p.convert("RGB"), (x, y)); x += p.width + GAP
vsheet.save(OUT / "jack_belt_r1_visual_qc.png")
print(f"Visual QC -> jack_belt_r1_visual_qc.png  ({vsheet.size})")

# Composite QC (just the full-body composite, larger)
fb_big_w = 600
fb_big_scale = fb_big_w / CW
fb_big = st_body_belt.resize((fb_big_w, int(CH * fb_big_scale)), Image.LANCZOS)
fb_big_bg = Image.new("RGB", fb_big.size, (210, 210, 210))
fb_big_bg.paste(fb_big.convert("RGBA"), (0,0), fb_big.split()[3])
fb_big_bg.save(OUT / "jack_belt_r1_composite_qc.png")
print(f"Composite QC -> jack_belt_r1_composite_qc.png  ({fb_big_bg.size})")

# ── Manifest ──────────────────────────────────────────────────────────────
manifest = {
    "category": "belt",
    "revision": "r1",
    "status": "STAGING_ONLY",
    "source": {
        "file": "assets/puppet/cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_77.png",
        "size": [BW, BH],
        "sha256": src_sha,
        "max_alpha_observed": int(np.array(belt_src)[...,3].max()),
        "note": "CoPainter never produces alpha=255; max observed ~254 across the ZIP. Pixel content preserved as-is — no thresholding or recolour applied during staging."
    },
    "bbox_crop_asset": {
        "file": "jack_belt_r1.png",
        "size": [BW, BH],
        "sha256": dst_sha,
        "is_byte_identical_copy_of_source": True
    },
    "full_canvas_test": {
        "file": "jack_belt_r1_full_canvas_test.png",
        "canvas_size": [CW, CH],
        "canvas_origin": "See-through layer canvas (768x768)",
        "belt_topleft_on_canvas": list(BELT_TL),
        "belt_size_on_canvas": [BELT_W_SCALED, BELT_H_SCALED],
        "scale_applied": round(BELT_SCALE, 4)
    },
    "anchor_derivation": {
        "method": "manual visual — CoPainter ZIP has no origin metadata; anchor derived from See-through topwear/legwear bbox overlap",
        "see_through_canvas": [CW, CH],
        "topwear_bbox": tw["bbox"],
        "legwear_bbox": lw["bbox"],
        "topwear_legwear_overlap_y": [overlap_top, overlap_bottom],
        "waist_centerline_xy": [WAIST_CX, WAIST_CY],
        "scale_basis": f"CoPainter jacket width {COPAINTER_JACKET_W}px maps to See-through topwear width {SEETHRU_TOPWEAR_W}px -> scale {BELT_SCALE:.4f}"
    },
    "do_not": [
        "modify pixel content (the bbox crop is byte-identical to source)",
        "promote to assets/puppet/layers/ until separate explicit task",
        "rebake the alpha to force 255 — keep CoPainter's native semi-alpha edges"
    ]
}
(OUT / "belt_r1_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest -> belt_r1_manifest.json")
print("DONE")
