"""
Stage CoPainter topwear split for the Jack puppet rig.

Sources:
  layer_71.png (269x390) = jacket
  layer_75.png (239x311) = shirt + tie

Outputs (assets/puppet/layers_staging/topwear_r1/):
  jack_jacket_r1.png                     byte-identical to layer_71.png
  jack_shirt_tie_r1.png                  byte-identical to layer_75.png
  jack_topwear_r1_full_canvas_test.png   both placed on See-through 768x768 canvas at derived torso anchor
  jack_topwear_r1_visual_qc.png          7-panel QC
  jack_topwear_r1_composite_qc.png       rough full-body composite
  topwear_r1_manifest.json               anchors / scales / alpha / SHA
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, hashlib, shutil

PROJECT  = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
CO_DIR   = PROJECT / r"assets\puppet\cloud_layer_tests\copainter\extracted_layers_1779216312185"
SRC_JKT  = CO_DIR / "layer_71.png"
SRC_ST   = CO_DIR / "layer_75.png"
OUT      = PROJECT / r"assets\puppet\layers_staging\topwear_r1"
SEETHRU  = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
ST_MAN   = SEETHRU / "layer_manifest.json"
BELT_PROD = PROJECT / r"assets\puppet\layers\belt\jack_belt.png"
BELT_MAN  = PROJECT / r"assets\puppet\layers\belt\manifest.json"
OUT.mkdir(parents=True, exist_ok=True)

# ── Sources ─────────────────────────────────────────────────────────────────
jkt_src = Image.open(SRC_JKT).convert("RGBA")
st_src  = Image.open(SRC_ST).convert("RGBA")
JW, JH = jkt_src.size
SW, SH = st_src.size
jkt_sha = hashlib.sha256(SRC_JKT.read_bytes()).hexdigest()
st_sha  = hashlib.sha256(SRC_ST.read_bytes()).hexdigest()
print(f"jacket  src: {JW}x{JH}  sha {jkt_sha[:16]}…")
print(f"shirt+tie src: {SW}x{SH}  sha {st_sha[:16]}…")

# Pixel-identical copies
DST_JKT = OUT / "jack_jacket_r1.png"
DST_ST  = OUT / "jack_shirt_tie_r1.png"
shutil.copyfile(SRC_JKT, DST_JKT)
shutil.copyfile(SRC_ST,  DST_ST)
dst_jkt_sha = hashlib.sha256(DST_JKT.read_bytes()).hexdigest()
dst_st_sha  = hashlib.sha256(DST_ST.read_bytes()).hexdigest()
assert jkt_sha == dst_jkt_sha and st_sha == dst_st_sha
print(f"Bbox copies: byte-identical")

# ── See-through geometry ───────────────────────────────────────────────────
mani = json.loads(ST_MAN.read_text())
CW, CH = mani["canvas"]
def L(name): return next((x for x in mani["layers"] if x.get("name") == name), None)
tw_meta = L("topwear")
lw_meta = L("legwear")
hw_meta = L("handwear")
TW_BBOX = tw_meta["bbox"]   # (314, 152, 505, 423)
LW_BBOX = lw_meta["bbox"]
TW_W = TW_BBOX[2] - TW_BBOX[0]   # 191
TW_H = TW_BBOX[3] - TW_BBOX[1]   # 271
TW_CX = (TW_BBOX[0] + TW_BBOX[2]) / 2
TW_TOP = TW_BBOX[1]               # 152
TW_BOT = TW_BBOX[3]               # 423
print(f"See-through canvas {CW}x{CH}  topwear bbox {TW_BBOX}  size {TW_W}x{TW_H}")

# Scale CoPainter → See-through: jacket width (269) -> See-through topwear width (191) = 0.71
JACKET_SCALE = TW_W / JW
print(f"Jacket scale (CoPainter -> ST): {JACKET_SCALE:.4f}")

# For shirt+tie, use the SAME scale (consistent torso scale)
SHIRT_SCALE = JACKET_SCALE
print(f"Shirt+tie scale: {SHIRT_SCALE:.4f}")

# Scaled sizes
jkt_w = max(1, int(JW * JACKET_SCALE)); jkt_h = max(1, int(JH * JACKET_SCALE))
sht_w = max(1, int(SW * SHIRT_SCALE));  sht_h = max(1, int(SH * SHIRT_SCALE))
jkt_scaled = jkt_src.resize((jkt_w, jkt_h), Image.LANCZOS)
sht_scaled = st_src.resize((sht_w, sht_h), Image.LANCZOS)
print(f"Scaled jacket: {jkt_w}x{jkt_h}   shirt+tie: {sht_w}x{sht_h}")

# Anchor: jacket centered horizontally on body centerline, top aligned to See-through topwear top.
# Belt manifest says waist centerline (408, 394), placed top-left (347, 379), size 123x31.
# Jacket should sit so its bottom aligns with belt top (≈ 394-15 = 379) and width matches torso.
JACKET_TL = (round(TW_CX - jkt_w / 2), TW_TOP)
# Shirt+tie sits BEHIND jacket — should be slightly narrower and centered, top slightly below collar
# Use vertical alignment: shirt+tie top a bit below jacket top so the collar shows
SHIRT_TOP_OFFSET = 12  # px below jacket top, so the collar V is visible
SHIRT_TL = (round(TW_CX - sht_w / 2), TW_TOP + SHIRT_TOP_OFFSET)
print(f"Placement on ST canvas:  jacket TL={JACKET_TL}   shirt TL={SHIRT_TL}")

# ── Full-canvas test composite (shirt under, jacket over) ──────────────────
fc = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
fc.alpha_composite(sht_scaled, SHIRT_TL)
fc.alpha_composite(jkt_scaled, JACKET_TL)
DST_FC = OUT / "jack_topwear_r1_full_canvas_test.png"
fc.save(DST_FC)
print(f"Full-canvas test -> {DST_FC.name}")

# ── See-through full body for context ──────────────────────────────────────
def place_st(name):
    info = L(name)
    if info is None or not info.get("png"): return None
    img = Image.open(SEETHRU / info["png"]).convert("RGBA")
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    c.alpha_composite(img, (info["bbox"][0], info["bbox"][1]))
    return c

# Build See-through body WITHOUT topwear (so we can drop CoPainter topwear in)
ST_DRAW_NO_TOP = ["back hair", "ears", "face", "eyebrow", "eyewhite", "irides",
                  "legwear", "footwear", "handwear"]
st_no_top = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
for n in ST_DRAW_NO_TOP:
    layer = place_st(n)
    if layer is not None: st_no_top.alpha_composite(layer)

# Build with CoPainter topwear (shirt+jacket)
st_with_co_top = st_no_top.copy()
st_with_co_top.alpha_composite(sht_scaled, SHIRT_TL)
st_with_co_top.alpha_composite(jkt_scaled, JACKET_TL)

# Build with See-through original topwear (baseline)
st_with_st_top = st_no_top.copy()
orig_top = place_st("topwear")
if orig_top is not None: st_with_st_top.alpha_composite(orig_top)

# Add belt overlay to both for full-body realism (read from production)
belt_img = Image.open(BELT_PROD).convert("RGBA")
belt_mani = json.loads(BELT_MAN.read_text())
BELT_TL = belt_mani["anchor"]["topleft_in_canvas"]      # (347, 379)
BELT_SZ = belt_mani["anchor"]["scaled_size_on_canvas"]  # (123, 31)
belt_scaled = belt_img.resize(tuple(BELT_SZ), Image.LANCZOS)
st_with_co_top.alpha_composite(belt_scaled, tuple(BELT_TL))
st_with_st_top.alpha_composite(belt_scaled, tuple(BELT_TL))

# ── QC panels ──────────────────────────────────────────────────────────────
PAD, LBL_H = 10, 22

def panel(img, label, bg=(210,210,210,255), max_w=None):
    if max_w and img.width > max_w:
        s = max_w / img.width
        img = img.resize((max_w, int(img.height * s)), Image.LANCZOS)
    p = Image.new("RGBA", (img.width + 20, img.height + LBL_H + 16), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    p.alpha_composite(img, (10, LBL_H + 8))
    return p

# 1: isolated jacket on light + dark
def pair_on_bgs(img, w_max=None):
    if w_max and img.width > w_max:
        s = w_max / img.width
        img = img.resize((w_max, int(img.height * s)), Image.LANCZOS)
    light = Image.new("RGBA", img.size, (210,210,210,255)); light.alpha_composite(img)
    dark  = Image.new("RGBA", img.size, (40,40,40,255));    dark.alpha_composite(img)
    gap = 10
    p = Image.new("RGBA", (light.width + gap + dark.width, light.height), (15,15,15,255))
    p.alpha_composite(light, (0,0)); p.alpha_composite(dark, (light.width + gap, 0))
    return p
p1 = panel(pair_on_bgs(jkt_src, w_max=280), "1. Isolated jacket (light | dark)")
p2 = panel(pair_on_bgs(st_src,  w_max=280), "2. Isolated shirt+tie (light | dark)")

# 3: CoPainter jacket + shirt+tie recomposed (shirt under, jacket over) at native CoPainter scale
recomp_w = max(jkt_src.width, st_src.width)
recomp_h = max(jkt_src.height, st_src.height) + 40
recomp = Image.new("RGBA", (recomp_w, recomp_h), (210, 210, 210, 255))
# Center horizontally, top-align
sx_pos = (recomp_w - st_src.width) // 2
jx_pos = (recomp_w - jkt_src.width) // 2
recomp.alpha_composite(st_src, (sx_pos, 20))
recomp.alpha_composite(jkt_src, (jx_pos, 0))
p3 = panel(recomp, "3. CoPainter recomposed: shirt+tie BEHIND jacket")

# 4: CoPainter recompose placed over See-through torso baseline (zoom)
# Compute torso zoom bbox
zoom_box = (max(0, TW_BBOX[0]-30), max(0, TW_BBOX[1]-20),
            min(CW, TW_BBOX[2]+30), min(CH, TW_BBOX[3]+90))
co_zoom = st_with_co_top.crop(zoom_box).resize(((zoom_box[2]-zoom_box[0])*2, (zoom_box[3]-zoom_box[1])*2), Image.NEAREST)
p4 = panel(co_zoom, "4. CoPainter topwear over See-through (torso zoom, 2x)")

# 5: full-body composite
fb_w = 360
fb_thumb = st_with_co_top.resize((fb_w, int(CH * fb_w / CW)), Image.LANCZOS)
fb_bg = Image.new("RGBA", fb_thumb.size, (210, 210, 210, 255)); fb_bg.alpha_composite(fb_thumb)
p5 = panel(fb_bg, "5. Full-body composite (See-through + CoPainter topwear + belt)")

# 6: zoomed collar/tie/belt alignment
zoom6 = (max(0, TW_BBOX[0]+30), max(0, TW_BBOX[1]+60),
         min(CW, TW_BBOX[2]-30), min(CH, TW_BBOX[3]+30))
co_zoom6 = st_with_co_top.crop(zoom6).resize(((zoom6[2]-zoom6[0])*3, (zoom6[3]-zoom6[1])*3), Image.NEAREST)
p6 = panel(co_zoom6, "6. Collar/tie/belt alignment (3x zoom)")

# 7: before/after — See-through merged topwear vs CoPainter split topwear
def torso_thumb(canvas):
    crop = canvas.crop(zoom_box)
    return crop.resize(((zoom_box[2]-zoom_box[0])*2, (zoom_box[3]-zoom_box[1])*2), Image.NEAREST)
before = torso_thumb(st_with_st_top)
after  = torso_thumb(st_with_co_top)
ba_w = before.width + after.width + 20
ba = Image.new("RGBA", (ba_w, before.height), (210, 210, 210, 255))
ba.alpha_composite(before, (0, 0))
ba.alpha_composite(after,  (before.width + 20, 0))
bd = ImageDraw.Draw(ba)
bd.text((10, 6),  "BEFORE: See-through merged topwear",  fill=(160, 30, 30))
bd.text((before.width + 30, 6), "AFTER: CoPainter split (jacket + shirt+tie)", fill=(30, 130, 30))
p7 = panel(ba, "7. Before/after — See-through merged vs CoPainter split")

# Notes column
NW = 420
NH = max(p5.height, 380)
notes = Image.new("RGBA", (NW, NH), (28,28,28,255))
nd = ImageDraw.Draw(notes)
nd.rectangle([(0,0),(NW-1, LBL_H-1)], fill=(50,50,50,255))
nd.text((5, 4), "Anchor / scale notes", fill=(220,220,220))
jkt_alpha_max = int(np.array(jkt_src)[...,3].max())
sht_alpha_max = int(np.array(st_src)[...,3].max())
notes_lines = [
    f"Source 1: layer_71.png (jacket)",
    f"  size: {JW} x {JH}   alpha_max: {jkt_alpha_max}",
    f"  sha[:16]: {jkt_sha[:16]}",
    f"Source 2: layer_75.png (shirt+tie)",
    f"  size: {SW} x {SH}   alpha_max: {sht_alpha_max}",
    f"  sha[:16]: {st_sha[:16]}",
    "",
    f"See-through canvas: {CW} x {CH}",
    f"Topwear bbox: {TW_BBOX}",
    f"Topwear size: {TW_W} x {TW_H}",
    f"Body centerline X: {round(TW_CX)}",
    "",
    f"Scale (CoPainter -> ST): {JACKET_SCALE:.4f}",
    f"  basis: CoPainter jacket 269 -> ST topwear 191",
    f"  same scale for shirt+tie (torso-consistent)",
    "",
    f"Scaled sizes:",
    f"  jacket    {jkt_w} x {jkt_h}",
    f"  shirt+tie {sht_w} x {sht_h}",
    "",
    f"Placement on ST canvas (top-left):",
    f"  jacket    {JACKET_TL}",
    f"  shirt+tie {SHIRT_TL}  (offset {SHIRT_TOP_OFFSET}px down)",
    "",
    f"Belt overlay (locked production):",
    f"  TL {BELT_TL}, size {BELT_SZ}",
    "",
    "Pixel-identical bbox PNGs:",
    f"  jacket sha[:16]: {dst_jkt_sha[:16]}",
    f"  shirt  sha[:16]: {dst_st_sha[:16]}",
]
yy = LBL_H + 8
for line in notes_lines:
    nd.text((10, yy), line, fill=(190,190,190))
    yy += 13

# Compose Visual QC sheet
GAP, OUTER = 10, 12
rows = [
    [p1, p2],
    [p3, p4],
    [p5, notes],
    [p6],
    [p7],
]
sheet_w = OUTER*2 + max(sum(p.width for p in r) + GAP*(len(r)-1) for r in rows)
sheet_h = OUTER*2 + sum(max(p.height for p in r) for r in rows) + GAP*(len(rows)-1)
sheet = Image.new("RGB", (sheet_w, sheet_h), (15,15,15))
y = OUTER
for r in rows:
    x = OUTER
    for p in r:
        sheet.paste(p.convert("RGB"), (x, y))
        x += p.width + GAP
    y += max(p.height for p in r) + GAP
sheet.save(OUT / "jack_topwear_r1_visual_qc.png")
print(f"Visual QC -> {sheet.size}")

# Composite QC (full body, larger)
big_w = 600
big = st_with_co_top.resize((big_w, int(CH * big_w / CW)), Image.LANCZOS)
big_bg = Image.new("RGB", big.size, (210, 210, 210))
big_bg.paste(big.convert("RGBA"), (0,0), big.split()[3])
big_bg.save(OUT / "jack_topwear_r1_composite_qc.png")
print(f"Composite QC -> {big_bg.size}")

# ── Manifest ──────────────────────────────────────────────────────────────
def stats_of(img):
    a = np.array(img)[..., 3]
    total = a.size
    return {
        "max_alpha": int(a.max()),
        "alpha_gt_0_pct": round(100*(a > 0).sum() / total, 2),
        "alpha_ge_200_pct": round(100*(a >= 200).sum() / total, 2),
    }

manifest = {
    "category": "topwear",
    "revision": "r1",
    "status": "STAGING_ONLY",
    "split": ["jacket", "shirt_tie"],
    "sources": {
        "jack_jacket_r1.png": {
            "copainter_zip_layer": "../../cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_71.png",
            "size": [JW, JH],
            "sha256": jkt_sha,
            **stats_of(jkt_src),
            "is_byte_identical_copy_of_source": True
        },
        "jack_shirt_tie_r1.png": {
            "copainter_zip_layer": "../../cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_75.png",
            "size": [SW, SH],
            "sha256": st_sha,
            **stats_of(st_src),
            "is_byte_identical_copy_of_source": True
        }
    },
    "copainter_alpha_quirk": "Max alpha across CoPainter ZIP ~254 (never 255). Pixel content preserved; no thresholding or recolour applied during staging.",
    "copainter_origin_metadata": {
        "present": False,
        "note": "CoPainter ZIP ships loose bbox-cropped PNGs with no per-layer origin/offset. Anchors derived visually against See-through topwear bbox."
    },
    "anchor_derivation": {
        "reference_canvas": "See-through full canvas (768x768)",
        "see_through_topwear_bbox": list(TW_BBOX),
        "body_centerline_x": round(TW_CX),
        "topwear_top_y": TW_TOP,
        "scale_factor_copainter_to_seethrough": round(JACKET_SCALE, 4),
        "scale_basis": "CoPainter jacket width 269 px -> See-through topwear width 191 px",
        "shirt_tie_offset_below_jacket_top_px": SHIRT_TOP_OFFSET
    },
    "full_canvas_test": {
        "file": "jack_topwear_r1_full_canvas_test.png",
        "canvas_size": [CW, CH],
        "draw_order_back_to_front": ["jack_shirt_tie_r1.png", "jack_jacket_r1.png"],
        "shirt_tie_topleft_on_canvas": list(SHIRT_TL),
        "shirt_tie_size_on_canvas": [sht_w, sht_h],
        "jacket_topleft_on_canvas": list(JACKET_TL),
        "jacket_size_on_canvas": [jkt_w, jkt_h]
    },
    "promoted_dependencies_used_in_qc": {
        "belt": {
            "file": "../../layers/belt/jack_belt.png",
            "topleft_on_canvas": BELT_TL,
            "size_on_canvas": BELT_SZ
        }
    },
    "do_not": [
        "modify pixel content (bbox crops are byte-identical to CoPainter source)",
        "promote to assets/puppet/layers/ until separate explicit task",
        "rebake the alpha to force 255 — keep CoPainter's native semi-alpha edges",
        "change the back-to-front draw order — shirt+tie BEHIND jacket"
    ]
}
(OUT / "topwear_r1_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest -> topwear_r1_manifest.json")
print("DONE")
