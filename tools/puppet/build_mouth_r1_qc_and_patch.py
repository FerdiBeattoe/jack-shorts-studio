"""
Mouth r1 QC + face patch builder.

Anchor convention (per spec):
  PRIMARY anchor reference = See-through face layer (07_face.png, bbox in 768x768)
  Secondary reference = production head (jack_head_front_base.png, 1024x1024)

Both placements are documented in the manifest. Visemes themselves are 512x512
RGBA with intrinsic anchor at (256, 270) — they scale to either canvas
deterministically using the documented anchor mapping.

Generates:
  jack_face_mouth_patch_r1.png                 (bbox-cropped soft fur patch, sized for head canvas)
  jack_face_mouth_patch_test_composite_r1.png  (head + patch test composite)
  jack_mouth_r1_visual_qc.png                  (visemes isolated, on light/dark grey)
  jack_mouth_r1_composite_qc.png               (See-through + head composites)
  mouth_r1_manifest.json
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import json

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT     = PROJECT / r"assets\puppet\layers_staging\mouth_r1"
HEAD    = PROJECT / r"assets\puppet\layers\head\jack_head_front_base.png"
SEETHRU_DIR = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
SEETHRU_FACE = SEETHRU_DIR / "07_face.png"
SEETHRU_MANIFEST = SEETHRU_DIR / "layer_manifest.json"

assert OUT.exists(), f"{OUT} missing — run build_mouth_r1.py first"
assert HEAD.exists(), f"{HEAD} missing"
assert SEETHRU_MANIFEST.exists(), f"{SEETHRU_MANIFEST} missing"

# ── Load See-through canvas data ────────────────────────────────────────────
st_mani = json.loads(SEETHRU_MANIFEST.read_text())
ST_CW, ST_CH = st_mani["canvas"]  # 768 x 768

def place_st_layer(name):
    L = next((x for x in st_mani["layers"] if x.get("name") == name and x.get("png")), None)
    if L is None: return None
    img = Image.open(SEETHRU_DIR / L["png"]).convert("RGBA")
    canvas = Image.new("RGBA", (ST_CW, ST_CH), (0, 0, 0, 0))
    canvas.alpha_composite(img, (L["bbox"][0], L["bbox"][1]))
    return canvas

# Build full See-through reference (all 11 layers, back-to-front)
ST_DRAW_ORDER = ["back hair", "ears", "face", "eyebrow", "eyewhite", "irides",
                 "legwear", "footwear", "handwear", "topwear"]
st_full = Image.new("RGBA", (ST_CW, ST_CH), (0, 0, 0, 0))
for n in ST_DRAW_ORDER:
    layer = place_st_layer(n)
    if layer is not None:
        st_full.alpha_composite(layer)
print(f"See-through full canvas built: {st_full.size}")

# See-through face layer specifics (probed in this conversation)
ST_FACE_BBOX = next(L["bbox"] for L in st_mani["layers"] if L.get("name") == "face")
ST_FACE_W = ST_FACE_BBOX[2] - ST_FACE_BBOX[0]
ST_FACE_H = ST_FACE_BBOX[3] - ST_FACE_BBOX[1]
# Muzzle anchor (snout bottom-center): face narrows from y=125 to y=145; pick (405, 142)
ST_MOUTH_XY = (405, 142)
print(f"See-through face bbox: {ST_FACE_BBOX}  size {ST_FACE_W}x{ST_FACE_H}")
print(f"See-through muzzle anchor: {ST_MOUTH_XY}")

# ── Load production head (secondary reference) ──────────────────────────────
head = Image.open(HEAD).convert("RGBA")
HW, HH = head.size
print(f"Head canvas: {HW}x{HH}")
HEAD_MOUTH_XY = (489, 745)  # tucked just below nose tip, above baked chin split

# ── Face patch (sized for production head where baked chin split exists) ────
# See-through face has NO baked mouth (28 dark pixels, all in brow area), so no
# patch is needed for the See-through composite. Patch only addresses the head.
PATCH_BBOX_HEAD = (380, 740, 600, 820)
patch_w = PATCH_BBOX_HEAD[2] - PATCH_BBOX_HEAD[0]
patch_h = PATCH_BBOX_HEAD[3] - PATCH_BBOX_HEAD[1]

def sample_head_fur():
    arr = np.array(head)
    samples = []
    for (y0,y1,x0,x1) in [(722,740, 400,580), (820,840, 400,580)]:
        region = arr[y0:y1, x0:x1]
        a=region[...,3]; r,g,b=region[...,0],region[...,1],region[...,2]
        mask = (a>200) & ~((r<80)&(g<80)&(b<80))
        if mask.any():
            samples.append(np.median(region[mask, :3], axis=0))
    return tuple(int(c) for c in np.median(np.array(samples), axis=0))
FUR_RGB = sample_head_fur()

SS = 4
pw, ph = patch_w * SS, patch_h * SS
patch_hi = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
pd = ImageDraw.Draw(patch_hi)
cx1 = int((489 - PATCH_BBOX_HEAD[0]) * SS)
cy1 = int((765 - PATCH_BBOX_HEAD[1]) * SS)
r1x, r1y = int(28 * SS), int(22 * SS)
pd.ellipse((cx1 - r1x, cy1 - r1y, cx1 + r1x, cy1 + r1y), fill=(*FUR_RGB, 200))
cx2 = pw // 2
cy2 = int((805 - PATCH_BBOX_HEAD[1]) * SS)
r2x, r2y = int(95 * SS), int(14 * SS)
pd.ellipse((cx2 - r2x, cy2 - r2y, cx2 + r2x, cy2 + r2y), fill=(*FUR_RGB, 170))
patch_hi = patch_hi.filter(ImageFilter.GaussianBlur(radius=10 * SS / 4))
patch = patch_hi.resize((patch_w, patch_h), Image.LANCZOS)
patch.save(OUT / "jack_face_mouth_patch_r1.png")
print(f"Patch (head canvas): {patch.size}  bbox_in_head={PATCH_BBOX_HEAD}  fur_rgb={FUR_RGB}")

head_patched = head.copy()
head_patched.alpha_composite(patch, (PATCH_BBOX_HEAD[0], PATCH_BBOX_HEAD[1]))
head_patched.save(OUT / "jack_face_mouth_patch_test_composite_r1.png")

# ── Visemes (already written by build_mouth_r1.py — load only) ──────────────
VISEMES = [
    ("neutral",       "jack_mouth_neutral_r1.png"),
    ("slight_frown",  "jack_mouth_slight_frown_r1.png"),
    ("slight_smirk",  "jack_mouth_slight_smirk_r1.png"),
    ("open_small",    "jack_mouth_open_small_r1.png"),
    ("open_medium",   "jack_mouth_open_medium_r1.png"),
    ("oo",            "jack_mouth_oo_r1.png"),
    ("ee",            "jack_mouth_ee_r1.png"),
    ("fv",            "jack_mouth_fv_r1.png"),
    ("mbp",           "jack_mouth_mbp_r1.png"),
]
loaded = [(label, fn, Image.open(OUT / fn).convert("RGBA")) for label, fn in VISEMES]
# Mouth canvas intrinsic anchor
MOUTH_ANCHOR = (256, 270)
MOUTH_CW, MOUTH_CH = loaded[0][2].size  # 512 x 512

# ── Compute placement scales ────────────────────────────────────────────────
# For See-through: scale 512-canvas mouth to fit on See-through face (~99 px tall).
# Production head face occupies ~760 px tall; mouth intrinsic ~50px tall artwork.
# See-through face ~99 px tall → mouth should be ~ 50 * 99/760 ≈ 6.5 px — too small.
# Better mapping: scale by face-bbox width ratio.
HEAD_FACE_WIDTH_REF = 760   # approximate visible face width on production head
ST_SCALE = ST_FACE_W / HEAD_FACE_WIDTH_REF * 1.6  # 1.6 factor: the relevant ratio is mouth width vs face width, not full mouth-canvas vs face
print(f"See-through scale factor: {ST_SCALE:.3f}")

def scale_mouth_for_st(img):
    nw = max(8, int(img.width * ST_SCALE))
    nh = max(8, int(img.height * ST_SCALE))
    return img.resize((nw, nh), Image.LANCZOS)

# ── QC 1: isolated visemes on light + dark grey ─────────────────────────────
TILE_W, TILE_H = 320, 200
PAD, LBL_H = 10, 22

def viseme_tile(img, label, bg):
    bb = img.getbbox()
    crop = img if bb is None else img.crop((max(0, bb[0]-8), max(0, bb[1]-8), min(512, bb[2]+8), min(512, bb[3]+8)))
    cw, ch = crop.size
    s = min((TILE_W - PAD*2) / cw, (TILE_H - LBL_H - PAD*2) / ch, 2.0)
    rs = crop.resize((max(1,int(cw*s)), max(1,int(ch*s))), Image.LANCZOS)
    tile = Image.new("RGBA", (TILE_W, TILE_H), bg)
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(TILE_W-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    tile.alpha_composite(rs, ((TILE_W-rs.width)//2, LBL_H + (TILE_H - LBL_H - rs.height)//2))
    return tile

COLS_VIS = 4
rows = (len(loaded) + COLS_VIS - 1) // COLS_VIS
qc_light = Image.new("RGBA", (TILE_W * COLS_VIS + 2*PAD, TILE_H * rows + 2*PAD + 30), (15, 15, 15, 255))
qc_dark  = Image.new("RGBA", (TILE_W * COLS_VIS + 2*PAD, TILE_H * rows + 2*PAD + 30), (15, 15, 15, 255))
ImageDraw.Draw(qc_light).text((PAD, 8), "Mouth r1 - visemes on LIGHT grey", fill=(220, 220, 220))
ImageDraw.Draw(qc_dark).text((PAD, 8),  "Mouth r1 - visemes on DARK grey",  fill=(220, 220, 220))
for i, (label, _, img) in enumerate(loaded):
    r, c = divmod(i, COLS_VIS)
    pos = (PAD + c * TILE_W, 30 + r * TILE_H)
    qc_light.alpha_composite(viseme_tile(img, label, (210, 210, 210, 255)), pos)
    qc_dark.alpha_composite(viseme_tile(img,  label, (40,  40,  40, 255)),  pos)
visual_sheet = Image.new("RGB", (qc_light.width, qc_light.height + qc_dark.height + PAD), (10, 10, 10))
visual_sheet.paste(qc_light.convert("RGB"), (0, 0))
visual_sheet.paste(qc_dark.convert("RGB"),  (0, qc_light.height + PAD))
visual_sheet.save(OUT / "jack_mouth_r1_visual_qc.png")
print(f"Visual QC: {visual_sheet.size}")

# ── QC 2: composite on See-through (primary) + head (secondary) ─────────────
# A) See-through composite tile: full SeeThrough body with each scaled mouth
def st_with_mouth(mouth_img, label):
    base = st_full.copy()
    sm = scale_mouth_for_st(mouth_img)
    # Anchor inside scaled mouth = original anchor scaled
    ax = int(MOUTH_ANCHOR[0] * ST_SCALE)
    ay = int(MOUTH_ANCHOR[1] * ST_SCALE)
    pos = (ST_MOUTH_XY[0] - ax, ST_MOUTH_XY[1] - ay)
    base.alpha_composite(sm, pos)
    # Zoom into head area for readability
    crop = base.crop((max(0, ST_FACE_BBOX[0]-30), max(0, ST_FACE_BBOX[1]-20),
                      min(ST_CW, ST_FACE_BBOX[2]+30), min(ST_CH, ST_FACE_BBOX[3]+50)))
    # Scale up for visibility
    scale_up = 3
    cu = crop.resize((crop.width * scale_up, crop.height * scale_up), Image.NEAREST)
    tile = Image.new("RGBA", (cu.width + 20, cu.height + LBL_H + 16), (28, 28, 28, 255))
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(tile.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), f"ST: {label}", fill=(220,220,220))
    tile.alpha_composite(cu, (10, LBL_H + 8))
    return tile

# B) Head composite tile (production head, secondary reference)
HEAD_THUMB_W = 360
def head_with_mouth(mouth_img, label, with_patch=False):
    base = head_patched.copy() if with_patch else head.copy()
    pos = (HEAD_MOUTH_XY[0] - MOUTH_ANCHOR[0], HEAD_MOUTH_XY[1] - MOUTH_ANCHOR[1])
    base.alpha_composite(mouth_img, pos)
    scale = HEAD_THUMB_W / HW
    thumb = base.resize((HEAD_THUMB_W, int(HH * scale)), Image.LANCZOS)
    suffix = "  + patch" if with_patch else ""
    tile = Image.new("RGBA", (HEAD_THUMB_W + 20, thumb.height + LBL_H + 16), (28, 28, 28, 255))
    d = ImageDraw.Draw(tile)
    d.rectangle([(0,0),(tile.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), f"HEAD: {label}{suffix}", fill=(220,220,220))
    tile.alpha_composite(thumb, (10, LBL_H + 8))
    return tile

# Patch comparison strip (head, open_medium - worst case)
demo = loaded[4][2]  # open_medium
patch_no  = head_with_mouth(demo, "open_medium", with_patch=False)
patch_yes = head_with_mouth(demo, "open_medium", with_patch=True)

# Build composite QC: top row = patch comparison
#                     middle rows = See-through (primary anchor) for all 9 visemes
#                     bottom rows = head (secondary) for all 9 visemes
st_tiles   = [st_with_mouth(img, label)   for label, _, img in loaded]
head_tiles = [head_with_mouth(img, label) for label, _, img in loaded]

COLS_ST = 3
COLS_HD = 3
rows_st = (len(st_tiles)   + COLS_ST - 1) // COLS_ST
rows_hd = (len(head_tiles) + COLS_HD - 1) // COLS_HD
tile_st_w, tile_st_h = st_tiles[0].width, st_tiles[0].height
tile_hd_w, tile_hd_h = head_tiles[0].width, head_tiles[0].height

# Layout
top_h = patch_no.height + 30  # header + patch strip
st_block_w = tile_st_w * COLS_ST + PAD * (COLS_ST + 1)
hd_block_w = tile_hd_w * COLS_HD + PAD * (COLS_HD + 1)
sheet_w = max(st_block_w, hd_block_w, patch_no.width * 2 + PAD * 3) + PAD * 2
sheet_h = top_h + 30 + rows_st * tile_st_h + 40 + rows_hd * tile_hd_h + PAD * 4

comp_sheet = Image.new("RGB", (sheet_w, sheet_h), (10, 10, 10))
cd = ImageDraw.Draw(comp_sheet)
cd.text((PAD, 8), "Mouth r1 composite QC  -  PRIMARY anchor: See-through face muzzle (405,142)  -  Secondary: head (489,745)", fill=(220, 220, 220))
# Patch comparison
comp_sheet.paste(patch_no.convert("RGB"),  (PAD, 30))
comp_sheet.paste(patch_yes.convert("RGB"), (PAD + patch_no.width + PAD, 30))
cd.text((PAD, 30 + patch_no.height + 4), "[Patch comparison on production head only; See-through face has no baked mouth to hide]", fill=(170, 170, 170))

# See-through row label
y = top_h + 20
cd.text((PAD, y), f"Primary - See-through face composite (scale {ST_SCALE:.3f}, anchor {ST_MOUTH_XY}):", fill=(180, 220, 180))
y += 20
for i, t in enumerate(st_tiles):
    r, c = divmod(i, COLS_ST)
    pos = (PAD + c * (tile_st_w + PAD), y + r * tile_st_h)
    comp_sheet.paste(t.convert("RGB"), pos)
y += rows_st * tile_st_h + 20

cd.text((PAD, y), f"Secondary - Production head composite (anchor {HEAD_MOUTH_XY}):", fill=(220, 200, 180))
y += 20
for i, t in enumerate(head_tiles):
    r, c = divmod(i, COLS_HD)
    pos = (PAD + c * (tile_hd_w + PAD), y + r * tile_hd_h)
    comp_sheet.paste(t.convert("RGB"), pos)

comp_sheet.save(OUT / "jack_mouth_r1_composite_qc.png")
print(f"Composite QC: {comp_sheet.size}")

# ── Manifest ────────────────────────────────────────────────────────────────
manifest = {
    "category": "mouth",
    "revision": "r1",
    "status": "STAGING_ONLY",
    "method": "deterministic Pillow procedural draw (build_mouth_r1.py), 4x supersample + LANCZOS downsample",
    "no_ai_no_cloud": True,
    "mouth_canvas_convention": {
        "size": [MOUTH_CW, MOUTH_CH],
        "is_full_canvas": True,
        "intrinsic_anchor_xy": list(MOUTH_ANCHOR),
        "anchor_name": "mouth_centroid",
        "anchor_rationale": "matches centroid cluster x=255-271, y=252-289 of existing production layers/mouth/* set"
    },
    "composite_placement": {
        "primary": {
            "reference": "See-through face layer (07_face.png in 768x768 canvas)",
            "canvas_size": [ST_CW, ST_CH],
            "face_bbox_in_canvas": list(ST_FACE_BBOX),
            "muzzle_anchor_xy": list(ST_MOUTH_XY),
            "scale_factor_for_mouth_canvas": round(ST_SCALE, 4),
            "scale_rationale": f"See-through face is {ST_FACE_W}x{ST_FACE_H} px - mouth canvas scaled by {ST_SCALE:.3f} to maintain mouth-to-face proportion observed on production head"
        },
        "secondary": {
            "reference": "Production head jack_head_front_base.png",
            "canvas_size": [HW, HH],
            "mouth_anchor_xy": list(HEAD_MOUTH_XY),
            "mouth_canvas_topleft_in_head": [HEAD_MOUTH_XY[0] - MOUTH_ANCHOR[0], HEAD_MOUTH_XY[1] - MOUTH_ANCHOR[1]],
            "no_scale_needed": True
        }
    },
    "style_rules": [
        "black lineart RGB(20,20,20) on transparent",
        "interior fill (open mouths) = dark maroon RGB(88,36,32)",
        "tongue accent = RGB(160,70,78)",
        "teeth = warm off-white RGB(240,235,220)",
        "line weight ~5 px at final 512 resolution",
        "deadpan adult-animation: no anime/kawaii/mascot/realistic detail"
    ],
    "face_patch": {
        "required_for_seethrough": False,
        "reason_seethrough":
            "See-through face layer has only 28 dark pixels (eyebrow region); no baked mouth/chin line to hide.",
        "required_for_production_head": False,
        "reason_head":
            "At mouth y=745 (above baked chin split y=748-820), the chin split reads as a faint chin-shadow under the mouth; patch is optional. Audit-only support asset retained.",
        "file": "jack_face_mouth_patch_r1.png",
        "bbox_in_head_canvas": list(PATCH_BBOX_HEAD),
        "fur_rgb_sampled": list(FUR_RGB),
        "method": "two soft elliptical fills + 10-px Gaussian feather; fur sampled from y=722-740 and y=820-840 immediately adjacent to patch zone"
    },
    "visemes": {},
}
for label, fn, img in loaded:
    a = np.array(img)[:, :, 3]
    total = a.size
    opaque = int((a == 255).sum())
    transp = int((a == 0).sum())
    bbox = img.getbbox()
    if (a > 50).any():
        ys, xs = np.where(a > 50)
        cy, cx = float(ys.mean()), float(xs.mean())
    else:
        cx = cy = None
    manifest["visemes"][label] = {
        "file": fn,
        "size": [img.width, img.height],
        "alpha_bbox": list(bbox) if bbox else None,
        "centroid": [round(cx, 1) if cx else None, round(cy, 1) if cy else None],
        "opaque_pct": round(100*opaque/total, 3),
        "transparent_pct": round(100*transp/total, 3),
        "semi_alpha_pct": round(100*(total-opaque-transp)/total, 3),
    }

(OUT / "mouth_r1_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest: {OUT / 'mouth_r1_manifest.json'}")
print("DONE")
