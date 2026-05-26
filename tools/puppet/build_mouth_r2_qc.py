"""
Mouth r2 QC + manifest + notes (no patch in r2 by default per spec).

Produces:
  jack_mouth_r2_visual_qc.png      (isolated visemes + character-sheet expressions + r1 size comparison)
  jack_mouth_r2_composite_qc.png   (See-through primary anchor + production-head secondary anchor)
  mouth_r2_manifest.json
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json

PROJECT      = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT          = PROJECT / r"assets\puppet\layers_staging\mouth_r2"
R1           = PROJECT / r"assets\puppet\layers_staging\mouth_r1"
HEAD         = PROJECT / r"assets\puppet\layers\head\jack_head_front_base.png"
SEETHRU_DIR  = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
SEETHRU_FACE = SEETHRU_DIR / "07_face.png"
SEETHRU_MAN  = SEETHRU_DIR / "layer_manifest.json"
CHAR_SHEET   = PROJECT / r"assets\jack_saas_design_asset_pack_v0_1\jack_saas_design_asset_pack_v0_1\01_character\master_refs\jack_character_sheet_master.png"

# ── Load See-through full canvas (for primary composite reference) ──────────
st_mani = json.loads(SEETHRU_MAN.read_text())
ST_CW, ST_CH = st_mani["canvas"]
def place_st(name):
    L = next((x for x in st_mani["layers"] if x.get("name") == name and x.get("png")), None)
    if L is None: return None
    img = Image.open(SEETHRU_DIR / L["png"]).convert("RGBA")
    c = Image.new("RGBA", (ST_CW, ST_CH), (0, 0, 0, 0))
    c.alpha_composite(img, (L["bbox"][0], L["bbox"][1]))
    return c

ST_FACE_BBOX = next(L["bbox"] for L in st_mani["layers"] if L.get("name") == "face")
ST_FACE_W = ST_FACE_BBOX[2] - ST_FACE_BBOX[0]
ST_FACE_H = ST_FACE_BBOX[3] - ST_FACE_BBOX[1]
ST_MOUTH_XY = (405, 142)  # snout bottom-center on See-through canvas

st_full = Image.new("RGBA", (ST_CW, ST_CH), (0, 0, 0, 0))
for n in ["back hair","ears","face","eyebrow","eyewhite","irides","legwear","footwear","handwear","topwear"]:
    layer = place_st(n)
    if layer is not None: st_full.alpha_composite(layer)

# ── Load production head (secondary) ────────────────────────────────────────
head = Image.open(HEAD).convert("RGBA")
HW, HH = head.size
HEAD_MOUTH_XY = (489, 745)

# ── Load r2 visemes ─────────────────────────────────────────────────────────
VISEMES = [
    ("neutral",       "jack_mouth_neutral_r2.png"),
    ("slight_frown",  "jack_mouth_slight_frown_r2.png"),
    ("slight_smirk",  "jack_mouth_slight_smirk_r2.png"),
    ("open_small",    "jack_mouth_open_small_r2.png"),
    ("open_medium",   "jack_mouth_open_medium_r2.png"),
    ("oo",            "jack_mouth_oo_r2.png"),
    ("ee",            "jack_mouth_ee_r2.png"),
    ("fv",            "jack_mouth_fv_r2.png"),
    ("mbp",           "jack_mouth_mbp_r2.png"),
]
loaded = [(lbl, fn, Image.open(OUT / fn).convert("RGBA")) for lbl, fn in VISEMES]
ANCHOR = (256, 270)
MOUTH_CW, MOUTH_CH = loaded[0][2].size

# r1 counterparts (for size comparison)
def r1_path(label):
    return R1 / f"jack_mouth_{label}_r1.png"
r1_loaded = {lbl: Image.open(r1_path(lbl)).convert("RGBA") if r1_path(lbl).exists() else None
             for lbl, _, _ in loaded}

# ── Crop 4 expression heads from character sheet for reference ──────────────
char = Image.open(CHAR_SHEET).convert("RGBA")
EXPRESSION_BOXES = {
    "deadpan":  (980, 180, 1230, 450),
    "smile":    (1280, 180, 1530, 450),
    "shocked":  (980, 510, 1230, 800),
    "smirk":    (1280, 510, 1530, 800),
}
expressions = {k: char.crop(box) for k, box in EXPRESSION_BOXES.items()}

# ── QC 1: visual sheet (isolated + char-sheet ref + r1 comparison) ─────────
PAD, LBL_H = 10, 22
TILE_W, TILE_H = 300, 180

def viseme_tile(img, label, bg, scale_max=2.5):
    bb = img.getbbox()
    crop = img if bb is None else img.crop((max(0, bb[0]-8), max(0, bb[1]-8),
                                            min(512, bb[2]+8), min(512, bb[3]+8)))
    cw, ch = crop.size
    s = min((TILE_W - PAD*2) / cw, (TILE_H - LBL_H - PAD*2) / ch, scale_max)
    rs = crop.resize((max(1,int(cw*s)), max(1,int(ch*s))), Image.LANCZOS)
    tile = Image.new("RGBA", (TILE_W, TILE_H), bg)
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(TILE_W-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    tile.alpha_composite(rs, ((TILE_W-rs.width)//2, LBL_H + (TILE_H - LBL_H - rs.height)//2))
    return tile

def expression_tile(img, label):
    s = min(TILE_W / img.width, (TILE_H - LBL_H) / img.height)
    rs = img.resize((int(img.width*s), int(img.height*s)), Image.LANCZOS)
    tile = Image.new("RGBA", (TILE_W, TILE_H), (28, 28, 28, 255))
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(TILE_W-1, LBL_H-1)], fill=(70,40,40,255))
    d.text((5, 4), f"REF: {label}", fill=(240, 200, 200))
    tile.alpha_composite(rs, ((TILE_W-rs.width)//2, LBL_H + (TILE_H-LBL_H-rs.height)//2))
    return tile

# Layout: header row of expression refs, then 3 rows of 4 r2 visemes (light bg),
# then a strict size-comparison row showing r1 vs r2 at TRUE relative scale.
COLS = 4
rows_visemes = (len(loaded) + COLS - 1) // COLS

vqc = Image.new("RGBA", (TILE_W * COLS + PAD * 2, TILE_H * (rows_visemes * 2 + 1) + 250 + PAD * 2), (15, 15, 15, 255))
vd = ImageDraw.Draw(vqc)
vd.text((PAD, 8), "Mouth r2 - visual QC", fill=(220,220,220))
# Row 0: 4 expression references
y0 = 30
expr_items = list(expressions.items())
for i, (k, img) in enumerate(expr_items):
    vqc.alpha_composite(expression_tile(img, k), (PAD + i * TILE_W, y0))
# Rows 1-3: r2 visemes on LIGHT then DARK
y1 = y0 + TILE_H + 10
vd.text((PAD, y1 - 16), "r2 visemes on LIGHT grey:", fill=(200, 200, 200))
for i, (lbl, _, img) in enumerate(loaded):
    r, c = divmod(i, COLS)
    vqc.alpha_composite(viseme_tile(img, lbl, (210, 210, 210, 255)), (PAD + c * TILE_W, y1 + r * TILE_H))
y2 = y1 + rows_visemes * TILE_H + 10
vd.text((PAD, y2 - 16), "r2 visemes on DARK grey:", fill=(200, 200, 200))
for i, (lbl, _, img) in enumerate(loaded):
    r, c = divmod(i, COLS)
    vqc.alpha_composite(viseme_tile(img, lbl, (40, 40, 40, 255)), (PAD + c * TILE_W, y2 + r * TILE_H))

# Bottom row: r1 vs r2 size comparison (true relative scale, no crop)
# Place a 256-px grey strip and overlay r1 (red tint) and r2 (green tint) at true 1:1
y3 = y2 + rows_visemes * TILE_H + 10
vd.text((PAD, y3 - 16), "r1 vs r2 size comparison (true 1:1 - r1 grey, r2 black):", fill=(200, 200, 200))
strip = Image.new("RGBA", (TILE_W * COLS + PAD*2, 200), (220, 220, 220, 255))
sd = ImageDraw.Draw(strip)
cmp_visemes = ["neutral", "slight_smirk", "open_medium", "ee"]
for i, label in enumerate(cmp_visemes):
    cx = PAD + i * TILE_W + TILE_W // 2
    cy = 100
    sd.text((PAD + i * TILE_W + 10, 6), label, fill=(50, 50, 50))
    # r1 light grey ghost
    r1im = r1_loaded[label]
    if r1im is not None:
        # Recolour r1 to mid-grey so both can be compared on white
        r1arr = np.array(r1im)
        # Where r1 was colored (any non-zero RGB), set to grey 130
        a1 = r1arr[..., 3]
        grey1 = np.zeros_like(r1arr)
        grey1[..., 0] = 130
        grey1[..., 1] = 130
        grey1[..., 2] = 130
        grey1[..., 3] = a1
        r1g = Image.fromarray(grey1, mode="RGBA")
        bb1 = r1g.getbbox()
        if bb1:
            c1 = r1g.crop(bb1)
            strip.alpha_composite(c1, (cx - c1.width // 2, cy - c1.height // 2))
    # r2 darker black overlay
    r2im = loaded[next(j for j,(l,_,_) in enumerate(loaded) if l == label)][2]
    bb2 = r2im.getbbox()
    if bb2:
        c2 = r2im.crop(bb2)
        strip.alpha_composite(c2, (cx - c2.width // 2, cy - c2.height // 2))
vqc.alpha_composite(strip, (0, y3))

visual_sheet = vqc.convert("RGB")
visual_sheet.save(OUT / "jack_mouth_r2_visual_qc.png")
print(f"Visual QC: {visual_sheet.size}")

# ── QC 2: composite on See-through (primary) and head (secondary) ──────────
# Scale factor for See-through composite (same calc as r1)
HEAD_FACE_WIDTH_REF = 760
ST_SCALE = ST_FACE_W / HEAD_FACE_WIDTH_REF * 1.6
print(f"See-through scale factor: {ST_SCALE:.3f}")

def st_tile(mouth_img, label):
    base = st_full.copy()
    nw = max(8, int(mouth_img.width * ST_SCALE))
    nh = max(8, int(mouth_img.height * ST_SCALE))
    sm = mouth_img.resize((nw, nh), Image.LANCZOS)
    ax = int(ANCHOR[0] * ST_SCALE); ay = int(ANCHOR[1] * ST_SCALE)
    base.alpha_composite(sm, (ST_MOUTH_XY[0] - ax, ST_MOUTH_XY[1] - ay))
    crop = base.crop((max(0, ST_FACE_BBOX[0]-30), max(0, ST_FACE_BBOX[1]-20),
                      min(ST_CW, ST_FACE_BBOX[2]+30), min(ST_CH, ST_FACE_BBOX[3]+50)))
    scale_up = 3
    cu = crop.resize((crop.width * scale_up, crop.height * scale_up), Image.NEAREST)
    tile = Image.new("RGBA", (cu.width + 20, cu.height + LBL_H + 10), (28, 28, 28, 255))
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(tile.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), f"ST: {label}", fill=(220,220,220))
    tile.alpha_composite(cu, (10, LBL_H + 5))
    return tile

HEAD_THUMB_W = 360
def head_tile(mouth_img, label):
    base = head.copy()
    pos = (HEAD_MOUTH_XY[0] - ANCHOR[0], HEAD_MOUTH_XY[1] - ANCHOR[1])
    base.alpha_composite(mouth_img, pos)
    scale = HEAD_THUMB_W / HW
    thumb = base.resize((HEAD_THUMB_W, int(HH * scale)), Image.LANCZOS)
    tile = Image.new("RGBA", (HEAD_THUMB_W + 20, thumb.height + LBL_H + 10), (28, 28, 28, 255))
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(tile.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), f"HEAD: {label}", fill=(220,220,220))
    tile.alpha_composite(thumb, (10, LBL_H + 5))
    return tile

st_tiles   = [st_tile(img, lbl)   for lbl, _, img in loaded]
head_tiles = [head_tile(img, lbl) for lbl, _, img in loaded]
COLS_ST = 3
COLS_HD = 3
tile_st_w, tile_st_h = st_tiles[0].size
tile_hd_w, tile_hd_h = head_tiles[0].size
rows_st = (len(st_tiles)   + COLS_ST - 1) // COLS_ST
rows_hd = (len(head_tiles) + COLS_HD - 1) // COLS_HD
st_block_w = tile_st_w * COLS_ST + PAD * (COLS_ST + 1)
hd_block_w = tile_hd_w * COLS_HD + PAD * (COLS_HD + 1)
sheet_w = max(st_block_w, hd_block_w) + PAD * 2
sheet_h = 60 + rows_st * tile_st_h + 40 + rows_hd * tile_hd_h + PAD * 4

comp = Image.new("RGB", (sheet_w, sheet_h), (10, 10, 10))
cd = ImageDraw.Draw(comp)
cd.text((PAD, 8), "Mouth r2 composite QC - PRIMARY: See-through face (405,142)  /  SECONDARY: head (489,745)", fill=(220, 220, 220))
cd.text((PAD, 28), "No face patch in r2 - mouth y=745 sits above the baked chin split.", fill=(170, 170, 170))
y = 60
cd.text((PAD, y - 16), f"See-through composite (scale {ST_SCALE:.3f}):", fill=(180, 220, 180))
for i, t in enumerate(st_tiles):
    r, c = divmod(i, COLS_ST)
    comp.paste(t.convert("RGB"), (PAD + c * (tile_st_w + PAD), y + r * tile_st_h))
y += rows_st * tile_st_h + 30
cd.text((PAD, y - 16), "Production head composite:", fill=(220, 200, 180))
for i, t in enumerate(head_tiles):
    r, c = divmod(i, COLS_HD)
    comp.paste(t.convert("RGB"), (PAD + c * (tile_hd_w + PAD), y + r * tile_hd_h))
comp.save(OUT / "jack_mouth_r2_composite_qc.png")
print(f"Composite QC: {comp.size}")

# ── Manifest ────────────────────────────────────────────────────────────────
manifest = {
    "category": "mouth",
    "revision": "r2",
    "supersedes": "mouth_r1 (rejected)",
    "status": "STAGING_ONLY",
    "method": "deterministic Pillow procedural draw (build_mouth_r2.py), 4x supersample + LANCZOS downsample",
    "no_ai_no_cloud": True,
    "rejection_of_r1": [
        "r1 mouths were 270-290 px wide; r2 reduced to 140-170 px (closed) / 34-82 px (open)",
        "r1 used pure black RGB(20,20,20); r2 uses warm dark brown RGB(40,35,28) sampled from production head face outline",
        "r1 used saturated maroon mouth interior + red tongue + cream teeth; r2 has line-only with optional faint same-hue inner shadow at 35% alpha",
        "r1 ee/fv had explicit tooth shapes and dividers; r2 ee/fv are line-shape approximations only - no teeth",
        "r1 line weight 5px; r2 line weight 4px (3 for secondary detail lines)"
    ],
    "mouth_canvas_convention": {
        "size": [MOUTH_CW, MOUTH_CH],
        "is_full_canvas": True,
        "intrinsic_anchor_xy": list(ANCHOR),
        "anchor_name": "mouth_centroid"
    },
    "composite_placement": {
        "primary": {
            "reference": "See-through face layer (07_face.png in 768x768 canvas)",
            "canvas_size": [ST_CW, ST_CH],
            "face_bbox_in_canvas": list(ST_FACE_BBOX),
            "muzzle_anchor_xy": list(ST_MOUTH_XY),
            "scale_factor_for_mouth_canvas": round(ST_SCALE, 4)
        },
        "secondary": {
            "reference": "Production head jack_head_front_base.png",
            "canvas_size": [HW, HH],
            "mouth_anchor_xy": list(HEAD_MOUTH_XY),
            "mouth_canvas_topleft_in_head": [HEAD_MOUTH_XY[0] - ANCHOR[0], HEAD_MOUTH_XY[1] - ANCHOR[1]],
            "no_scale_needed": True
        }
    },
    "style_rules": [
        "lineart RGB(40,35,28) - warm dark brown, matches face outline",
        "inner shadow (open mouths) = same hue at 35% alpha, never a saturated fill",
        "no teeth in any viseme",
        "no tongue colour",
        "deadpan / tired / adult-animation; no kawaii/anime/mascot/realistic detail",
        "line weight ~4 px at final 512 resolution; secondary detail lines ~3 px"
    ],
    "face_patch": {
        "required": False,
        "reason":
            "r2 mouths are small enough (closed widths 110-168 px) that they sit cleanly at mouth y=745, above the baked chin split (y=748-820). The chin split reads as a faint chin-shadow under the mouth. No patch generated in r2 - this is intentional per spec ('no face patch in r2 unless absolutely necessary')."
    },
    "visemes": {},
}
for lbl, fn, img in loaded:
    a = np.array(img)[:, :, 3]
    total = a.size
    opaque = int((a == 255).sum())
    transp = int((a == 0).sum())
    bbox = img.getbbox()
    if (a > 50).any():
        ys, xs = np.where(a > 50)
        cy, cx = float(ys.mean()), float(xs.mean())
        bw = bbox[2]-bbox[0] if bbox else 0
        bh = bbox[3]-bbox[1] if bbox else 0
    else:
        cx = cy = None; bw = bh = 0
    manifest["visemes"][lbl] = {
        "file": fn,
        "size": [img.width, img.height],
        "alpha_bbox": list(bbox) if bbox else None,
        "bbox_wh": [bw, bh],
        "centroid": [round(cx, 1) if cx else None, round(cy, 1) if cy else None],
        "opaque_pct": round(100*opaque/total, 3),
        "transparent_pct": round(100*transp/total, 3),
        "semi_alpha_pct": round(100*(total-opaque-transp)/total, 3),
    }

(OUT / "mouth_r2_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest: {OUT / 'mouth_r2_manifest.json'}")
print("DONE")
