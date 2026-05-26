"""
Stage CoPainter eye/blink assets (from layer_43.png).

layer_43 structure (152x249 RGBA):
  y= 12- 29   eyebrows (left + right)
  y= 30- 94   open eyes pair (Jack's deadpan open look, with iris + sclera)
  y= 95-150   closed/squinted eyes pair (heavy-lidded sleepy)
  y=160-249   snout / jaw fragment (ignore — out of scope)

Outputs (assets/puppet/layers_staging/eyes_blink_r1/):
  jack_eye_left_closed_r1.png    bottom-pair LEFT eye (heavy-lidded squint)
  jack_eye_right_closed_r1.png   bottom-pair RIGHT eye
  (half_r1 NOT produced - see notes for why)
  jack_eye_blink_r1_visual_qc.png
  jack_eye_blink_r1_composite_qc.png
  eyes_blink_r1_manifest.json
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, hashlib

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
SRC     = PROJECT / r"assets\puppet\cloud_layer_tests\copainter\extracted_layers_1779216312185\layer_43.png"
OUT     = PROJECT / r"assets\puppet\layers_staging\eyes_blink_r1"
SEETHRU = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
ST_MAN  = SEETHRU / "layer_manifest.json"
HEAD    = PROJECT / r"assets\puppet\layers\head\jack_head_front_base.png"
EXIST_EYES = PROJECT / r"assets\puppet\layers\eyes"
OUT.mkdir(parents=True, exist_ok=True)

assert SRC.exists(), f"{SRC} not found"

# ── Source probe ────────────────────────────────────────────────────────────
src = Image.open(SRC).convert("RGBA")
SW, SH = src.size
print(f"layer_43 source: {SW}x{SH}")
src_sha = hashlib.sha256(SRC.read_bytes()).hexdigest()

# ── Closed-eye crops (bottom pair) ──────────────────────────────────────────
# Dark-linework analysis gave: closed-row y=95-150, left eye centroid x≈58,
# right eye centroid x≈125. Use 60x55 crops centered on each.
LEFT_BOX  = (28, 95, 88, 150)   # 60x55
RIGHT_BOX = (92, 95, 152, 150)  # 60x55

def crop_and_save(box, name):
    c = src.crop(box).copy()
    p = OUT / name
    c.save(p)
    return c, p

eye_left_closed,  p_left  = crop_and_save(LEFT_BOX,  "jack_eye_left_closed_r1.png")
eye_right_closed, p_right = crop_and_save(RIGHT_BOX, "jack_eye_right_closed_r1.png")
print(f"Closed-L bbox={LEFT_BOX}  -> {p_left.name}  size={eye_left_closed.size}")
print(f"Closed-R bbox={RIGHT_BOX} -> {p_right.name} size={eye_right_closed.size}")

# Stats
def stats_of(img):
    a = np.array(img)[..., 3]
    total = a.size
    nz = int((a > 0).sum())
    high = int((a >= 200).sum())
    return {
        "size": list(img.size),
        "max_alpha": int(a.max()),
        "alpha_gt_0_pct":  round(100*nz/total,2),
        "alpha_ge_200_pct": round(100*high/total,2),
        "bbox":  list(img.getbbox()) if img.getbbox() else None,
    }

# ── Half: not produced — explain why in manifest ────────────────────────────
# Top-pair eyes are Jack's NORMAL open deadpan; not distinct from existing
# production jack_eye_*_open / _half assets. CoPainter doesn't add a new state.

# ── See-through canvas geometry for composite QC ───────────────────────────
mani = json.loads(ST_MAN.read_text())
CW, CH = mani["canvas"]
def st_layer(name):
    L = next((x for x in mani["layers"] if x.get("name") == name), None)
    if L is None or not L.get("png"): return None, None
    img = Image.open(SEETHRU / L["png"]).convert("RGBA")
    return img, L["bbox"]
face_img, face_bbox = st_layer("face")
print(f"See-through face bbox: {face_bbox}")

# Build See-through full body for composite
def place(name):
    img, bbox = st_layer(name)
    if img is None: return None
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    c.alpha_composite(img, (bbox[0], bbox[1]))
    return c
st_full = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
for n in ["back hair","ears","face","eyebrow","eyewhite","irides",
          "legwear","footwear","handwear","topwear"]:
    layer = place(n)
    if layer is not None: st_full.alpha_composite(layer)

# Derive eye anchor on See-through face.
# Existing See-through 'eyewhite' bbox (380, 79, 447, 94) and 'irides' (388, 78, 441, 87)
# give us the two-eye target. Use those bbox extents to find left/right eye centers.
ew_img, ew_bbox = st_layer("eyewhite")
ir_img, ir_bbox = st_layer("irides")
print(f"See-through eyewhite bbox: {ew_bbox}, irides bbox: {ir_bbox}")
# Combine — eye row centroid
EYE_ROW_Y = (ew_bbox[1] + ew_bbox[3]) / 2  # ≈ 86
# The two eyes are inside x_range 380-447 (eyewhite extent). Split mid:
EYE_MIDX = (ew_bbox[0] + ew_bbox[2]) / 2  # ≈ 413
# Left eye center (image-left on See-through, char-RIGHT): between ew_bbox[0] and EYE_MIDX
EYE_L_X = (ew_bbox[0] + EYE_MIDX) / 2
EYE_R_X = (ew_bbox[2] + EYE_MIDX) / 2
print(f"See-through eye anchors: L={EYE_L_X:.0f},{EYE_ROW_Y:.0f}  R={EYE_R_X:.0f},{EYE_ROW_Y:.0f}")

# Scale CoPainter eye to See-through face scale
# Existing See-through eye widths (eyewhite_w=67) — our eye crops are 60 wide
# So scale = 60 / 60-or-so → ~0.5-0.6 to match See-through eye size
ST_FACE_W = face_bbox[2] - face_bbox[0]      # 87
EYE_SCALE = (ew_bbox[2] - ew_bbox[0]) / 67 * 0.45  # rough match — about 0.45 of crop width
# Simpler approach: scale by face-width ratio (See-through face vs CoPainter face width)
# CoPainter head layer (layer_01) is 253 wide. See-through face is 87 wide. Ratio = 87/253 ≈ 0.34
COPAINTER_HEAD_W = 253
ST_FACE_TO_CO_SCALE = ST_FACE_W / COPAINTER_HEAD_W
print(f"CoPainter -> See-through face scale: {ST_FACE_TO_CO_SCALE:.4f}")

def scale_eye(img, s):
    nw = max(8, int(img.width * s))
    nh = max(8, int(img.height * s))
    return img.resize((nw, nh), Image.LANCZOS)

eye_L_st = scale_eye(eye_left_closed,  ST_FACE_TO_CO_SCALE)
eye_R_st = scale_eye(eye_right_closed, ST_FACE_TO_CO_SCALE)
print(f"Eyes at See-through scale: L {eye_L_st.size}  R {eye_R_st.size}")

# Place on See-through full canvas
def with_closed_eyes(base):
    out = base.copy()
    # Cover the existing open eyes by drawing closed eyes on top
    pos_L = (int(EYE_L_X - eye_L_st.width / 2), int(EYE_ROW_Y - eye_L_st.height / 2))
    pos_R = (int(EYE_R_X - eye_R_st.width / 2), int(EYE_ROW_Y - eye_R_st.height / 2))
    out.alpha_composite(eye_L_st, pos_L)
    out.alpha_composite(eye_R_st, pos_R)
    return out

st_blink = with_closed_eyes(st_full)

# ── Composite on production head (secondary) ───────────────────────────────
head = Image.open(HEAD).convert("RGBA")
HW, HH = head.size
# Existing head eye anchors — sample from production eye assets if possible
# Otherwise pick sensible defaults based on the head image (1024x1024).
# From earlier head probe: nose centroid ≈ (489, 587). Eyes sit higher: y≈420.
# Eye horizontal centers approx x=420 (left/char-right) and x=560 (right/char-left)
HEAD_EYE_Y = 420
HEAD_EYE_L_X = 420
HEAD_EYE_R_X = 565
# Scale CoPainter eyes for head: head is ~760 tall, See-through face ~99 tall.
# Just scale by ratio of nose width or eye width: rough head eye dim ~80px.
HEAD_SCALE = 80 / 60  # eye crop is 60px wide, target ~80px on head
eye_L_head = scale_eye(eye_left_closed, HEAD_SCALE)
eye_R_head = scale_eye(eye_right_closed, HEAD_SCALE)

head_blink = head.copy()
head_blink.alpha_composite(eye_L_head, (HEAD_EYE_L_X - eye_L_head.width//2, HEAD_EYE_Y - eye_L_head.height//2))
head_blink.alpha_composite(eye_R_head, (HEAD_EYE_R_X - eye_R_head.width//2, HEAD_EYE_Y - eye_R_head.height//2))

# ── Visual QC (6 panels) ──────────────────────────────────────────────────
PAD, LBL_H = 10, 22

def panel(img, label, bg=(210,210,210,255)):
    p = Image.new("RGBA", (img.width + 20, img.height + LBL_H + 16), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), label, fill=(220,220,220))
    p.alpha_composite(img, (10, LBL_H + 8))
    return p

# Panel 1: source layer_43 (full) with crop bboxes overlaid
src_show = src.copy().resize((SW*3, SH*3), Image.NEAREST)
sd = ImageDraw.Draw(src_show)
def scale_box(b, s):
    return (b[0]*s, b[1]*s, b[2]*s, b[3]*s)
sd.rectangle(scale_box(LEFT_BOX, 3),  outline=(80, 255, 80), width=3)
sd.rectangle(scale_box(RIGHT_BOX, 3), outline=(255, 80, 80), width=3)
sd.text((6, 6), "source layer_43 - GREEN=L crop, RED=R crop", fill=(255,255,255))
p1 = panel(src_show, "1. Source layer_43 with crop bboxes")

# Panel 2: isolated extracted eyes (4x zoom on light + dark)
def isolated_pair(bg):
    L = eye_left_closed.resize((eye_left_closed.width*4, eye_left_closed.height*4), Image.NEAREST)
    R = eye_right_closed.resize((eye_right_closed.width*4, eye_right_closed.height*4), Image.NEAREST)
    w = L.width + R.width + 20
    p = Image.new("RGBA", (w, max(L.height, R.height)), bg)
    p.alpha_composite(L, (0, 0))
    p.alpha_composite(R, (L.width + 20, 0))
    return p

iso_light = isolated_pair((210,210,210,255))
iso_dark  = isolated_pair((40,40,40,255))
p2_light = panel(iso_light, "2a. Isolated closed eyes (light, 4x zoom)  L | R")
p2_dark  = panel(iso_dark,  "2b. Isolated closed eyes (dark, 4x zoom)")

# Panel 3: composite on See-through face (head zoom)
st_blink_zoom = st_blink.crop((max(0, face_bbox[0]-30), max(0, face_bbox[1]-20),
                                min(CW, face_bbox[2]+30), min(CH, face_bbox[3]+50)))
st_blink_zoom_up = st_blink_zoom.resize((st_blink_zoom.width*3, st_blink_zoom.height*3), Image.NEAREST)
p3 = panel(st_blink_zoom_up, "3. CoPainter closed eyes on See-through face (3x zoom)")

# Panel 4: composite on production head
head_thumb_w = 360
head_thumb = head_blink.resize((head_thumb_w, int(HH * head_thumb_w / HW)), Image.LANCZOS)
p4 = panel(head_thumb, "4. CoPainter closed eyes on production head")

# Panel 5: comparison vs existing eye assets (left side only — close + half + open)
existing_paths = {
    "open":   EXIST_EYES / "jack_eye_left_open.png",
    "half":   EXIST_EYES / "jack_eye_left_half.png",
    "closed": EXIST_EYES / "jack_eye_left_closed.png",
}
existing_imgs = {k: Image.open(v).convert("RGBA") for k,v in existing_paths.items() if v.exists()}
# Build comparison row: existing_open | existing_half | existing_closed | new closed_r1
cmp_h = 200
def fit_to_h(im, h):
    s = h / im.height
    return im.resize((int(im.width*s), h), Image.LANCZOS)
cmp_imgs = [
    (fit_to_h(existing_imgs["open"],   cmp_h), "existing open"),
    (fit_to_h(existing_imgs["half"],   cmp_h), "existing half"),
    (fit_to_h(existing_imgs["closed"], cmp_h), "existing closed"),
    (fit_to_h(eye_left_closed.resize((eye_left_closed.width*3, eye_left_closed.height*3), Image.LANCZOS), cmp_h), "r1 closed (CoPainter)"),
]
cmp_w = sum(im[0].width for im in cmp_imgs) + (len(cmp_imgs)-1)*16 + 20
cmp_panel = Image.new("RGBA", (cmp_w, cmp_h + LBL_H*2 + 10), (210,210,210,255))
cd = ImageDraw.Draw(cmp_panel)
cd.rectangle([(0,0),(cmp_w-1, LBL_H-1)], fill=(50,50,50,255))
cd.text((5, 4), "5. Left-eye comparison: existing open | half | closed | new r1 closed (CoPainter)", fill=(220,220,220))
xx = 10
for im, label in cmp_imgs:
    cmp_panel.alpha_composite(im, (xx, LBL_H + 8))
    cd.text((xx + 4, LBL_H + 8 + cmp_h + 4), label, fill=(50, 50, 50))
    xx += im.width + 16
p5 = panel(cmp_panel, "5. Comparison vs existing eye assets (left eye)", bg=(28,28,28,255))

# Panel 6: 1:1 zoom of eye area on production head
zoom_box = (HEAD_EYE_L_X - 80, HEAD_EYE_Y - 50, HEAD_EYE_R_X + 80, HEAD_EYE_Y + 60)
zoom6 = head_blink.crop(zoom_box).resize(((zoom_box[2]-zoom_box[0])*2, (zoom_box[3]-zoom_box[1])*2), Image.NEAREST)
p6 = panel(zoom6, "6. Production head eye area at 2x zoom (with r1 closed applied)")

# Compose visual QC sheet
GAP, OUTER = 10, 12
rows = [
    [p1],
    [p2_light, p2_dark],
    [p3, p4],
    [p5],
    [p6],
]
row_widths = [sum(p.width for p in r) + GAP*(len(r)-1) for r in rows]
sheet_w = OUTER*2 + max(row_widths)
sheet_h = OUTER*2 + sum(max(p.height for p in r) for r in rows) + GAP*(len(rows)-1)
sheet = Image.new("RGB", (sheet_w, sheet_h), (15,15,15))
y = OUTER
for r in rows:
    x = OUTER
    for p in r:
        sheet.paste(p.convert("RGB"), (x, y))
        x += p.width + GAP
    y += max(p.height for p in r) + GAP
sheet.save(OUT / "jack_eye_blink_r1_visual_qc.png")
print(f"Visual QC -> {sheet.size}")

# Composite QC (See-through and head side-by-side)
st_thumb_w = 500
st_thumb = st_blink.resize((st_thumb_w, int(CH * st_thumb_w / CW)), Image.LANCZOS)
head_thumb2_w = 500
head_thumb2 = head_blink.resize((head_thumb2_w, int(HH * head_thumb2_w / HW)), Image.LANCZOS)
cw = st_thumb.width + head_thumb2.width + 20
ch = max(st_thumb.height, head_thumb2.height) + 30
comp = Image.new("RGB", (cw, ch), (210, 210, 210))
comp.paste(st_thumb.convert("RGBA"), (0, 30), st_thumb.split()[3])
comp.paste(head_thumb2.convert("RGBA"), (st_thumb.width + 20, 30), head_thumb2.split()[3])
cdc = ImageDraw.Draw(comp)
cdc.text((5, 5), "See-through full body with closed eyes  |  Production head with closed eyes", fill=(20, 20, 20))
comp.save(OUT / "jack_eye_blink_r1_composite_qc.png")
print(f"Composite QC -> {comp.size}")

# ── Manifest ──────────────────────────────────────────────────────────────
manifest = {
    "category": "eyes_blink",
    "revision": "r1",
    "status": "STAGING_ONLY",
    "source": {
        "file": "assets/puppet/cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_43.png",
        "size": [SW, SH],
        "sha256": src_sha,
        "structure_y_bands": {
            "12-29":  "eyebrows (ignored - out of scope)",
            "30-94":  "open eyes pair (top, ignored - duplicates existing 'open')",
            "95-150": "closed/squinted eyes pair (extracted as _closed_r1)",
            "160-249": "snout / jaw fragment (ignored)"
        },
        "max_alpha_observed": int(np.array(src)[..., 3].max()),
        "copainter_alpha_quirk": "max alpha across ZIP is ~254, never 255; pixel content preserved as-is"
    },
    "extracted_assets": {
        "jack_eye_left_closed_r1.png": {
            "source_bbox_in_layer_43": list(LEFT_BOX),
            **stats_of(eye_left_closed),
            "represents": "character LEFT eye, image-LEFT in layer_43 - sleepy/heavy-lidded squint"
        },
        "jack_eye_right_closed_r1.png": {
            "source_bbox_in_layer_43": list(RIGHT_BOX),
            **stats_of(eye_right_closed),
            "represents": "character RIGHT eye, image-RIGHT in layer_43 - sleepy/heavy-lidded squint"
        }
    },
    "half_variants_rejected": {
        "reason": "Top eye pair in layer_43 (y=30-94) is Jack's normal OPEN deadpan look - matches existing jack_eye_*_open.png in style; CoPainter does NOT add a distinct half-state worth staging. Bottom pair was already taken as 'closed' for r1."
    },
    "naming_convention": {
        "rule": "filenames use CHARACTER anatomy (left=character left=image-LEFT in this layer's frame)",
        "note": "layer_43 internally already shows left/right as character-anatomy correct"
    },
    "composite_anchor_seethrough": {
        "canvas": [CW, CH],
        "eye_row_y": int(EYE_ROW_Y),
        "left_eye_center_x":  round(EYE_L_X, 1),
        "right_eye_center_x": round(EYE_R_X, 1),
        "scale_copainter_to_seethrough": round(ST_FACE_TO_CO_SCALE, 4),
        "scale_basis": f"CoPainter head width 253 px maps to See-through face width 87 px -> {ST_FACE_TO_CO_SCALE:.4f}"
    },
    "composite_anchor_production_head": {
        "canvas": [HW, HH],
        "eye_row_y": HEAD_EYE_Y,
        "left_eye_center_x":  HEAD_EYE_L_X,
        "right_eye_center_x": HEAD_EYE_R_X,
        "scale_copainter_to_head": round(HEAD_SCALE, 4),
        "scale_basis": "rough match — eye crop 60 px wide -> target ~80 px on production head"
    },
    "do_not": [
        "modify pixel content (crops are byte-identical pixel extractions of the source region)",
        "promote to assets/puppet/layers/eyes/ without a fresh QC comparing the squint look to the existing 'closed' full-lid-down convention",
        "rename or recolour - keep CoPainter's native semi-alpha edges"
    ]
}
(OUT / "eyes_blink_r1_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest -> eyes_blink_r1_manifest.json")
print("DONE")
