"""
Full-body integration QC using locked production assets + See-through baseline
for unapproved categories.

Layer order (back to front), per topwear Option B:
  1. back hair       (See-through baseline)
  2. ears            (See-through baseline)
  3. face            (See-through baseline)
  4. eyebrow         (See-through baseline)
  5. eyewhite        (See-through baseline)
  6. irides          (See-through baseline)
  7. mouth           (PRODUCTION — over face)
  8. legwear         (See-through baseline)
  9. footwear        (See-through baseline)
  10. handwear       (See-through baseline, UNMODIFIED — shoulder/arm bulk)
  11. shirt+tie      (PRODUCTION)
  12. jacket         (PRODUCTION)
  13. belt           (PRODUCTION)
  14. hand_left/right (PRODUCTION — at cuffs)
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json

P = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
SEETHRU = P / r"assets\puppet\cloud_layer_tests\see_through\extracted"
ST_MAN  = SEETHRU / "layer_manifest.json"
LAYERS = P / r"assets\puppet\layers"
OUT = P / r"assets\puppet\layers_staging\full_body_integration_qc_r1"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load See-through canvas geometry ──────────────────────────────────────
mani = json.loads(ST_MAN.read_text())
CW, CH = mani["canvas"]
def L(name): return next((x for x in mani["layers"] if x.get("name") == name), None)
def place_st(name):
    info = L(name)
    if info is None or not info.get("png"): return None
    img = Image.open(SEETHRU / info["png"]).convert("RGBA")
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    c.alpha_composite(img, (info["bbox"][0], info["bbox"][1]))
    return c
print(f"See-through canvas: {CW}x{CH}")

# ── Load production-locked manifests for anchor truth ─────────────────────
top_man   = json.loads((LAYERS / "topwear" / "manifest.json").read_text())
belt_man  = json.loads((LAYERS / "belt"    / "manifest.json").read_text())
mouth_man = json.loads((LAYERS / "mouth"   / "manifest.json").read_text())

# Topwear anchors (from production manifest)
top_anchors = top_man["placement_on_seethrough_canvas"]
JACKET_TL = tuple(top_anchors["jacket_topleft_on_canvas"])
JACKET_SZ = tuple(top_anchors["jacket_scaled_size_on_canvas"])
SHIRT_TL  = tuple(top_anchors["shirt_tie_topleft_on_canvas"])
SHIRT_SZ  = tuple(top_anchors["shirt_tie_scaled_size_on_canvas"])
JACKET_BOT  = JACKET_TL[1] + JACKET_SZ[1]
JACKET_RIGHT = JACKET_TL[0] + JACKET_SZ[0]
print(f"Jacket TL={JACKET_TL} size={JACKET_SZ}  bottom={JACKET_BOT}")

# Belt anchors
BELT_TL = tuple(belt_man["anchor"]["topleft_in_canvas"])
BELT_SZ = tuple(belt_man["anchor"]["scaled_size_on_canvas"])

# Mouth anchors (primary See-through face)
ST_MOUTH_XY = tuple(mouth_man["composite_placement"]["primary"]["muzzle_anchor_xy"])
MOUTH_SCALE = mouth_man["composite_placement"]["primary"]["scale_factor_for_mouth_canvas"]
MOUTH_INTRINSIC_ANCHOR = tuple(mouth_man["canvas_convention"]["intrinsic_anchor_xy"])
print(f"Mouth anchor on ST: {ST_MOUTH_XY}  scale={MOUTH_SCALE}")

# Hand placement (from sleeve_strategy_qc) — same recipe used in promotion
HAND_SCALE = 0.42
CUFF_Y    = JACKET_BOT - 18

# ── Load production assets ────────────────────────────────────────────────
def img(rel): return Image.open(LAYERS / rel).convert("RGBA")
jacket    = img("topwear/jack_jacket.png").resize(JACKET_SZ, Image.LANCZOS)
shirt_tie = img("topwear/jack_shirt_tie.png").resize(SHIRT_SZ, Image.LANCZOS)
belt      = img("belt/jack_belt.png").resize(BELT_SZ, Image.LANCZOS)
hand_L    = img("hands/jack_hand_left.png")
hand_R    = img("hands/jack_hand_right.png")
hand_L_s  = hand_L.resize((int(hand_L.width * HAND_SCALE), int(hand_L.height * HAND_SCALE)), Image.LANCZOS)
hand_R_s  = hand_R.resize((int(hand_R.width * HAND_SCALE), int(hand_R.height * HAND_SCALE)), Image.LANCZOS)
HAND_R_POS = (JACKET_TL[0] - hand_R_s.width // 2 + 10, CUFF_Y - 6)
HAND_L_POS = (JACKET_RIGHT - hand_L_s.width // 2 - 10, CUFF_Y - 6)

mouth_neutral = img("mouth/jack_mouth_neutral.png")
mouth_smirk   = img("mouth/jack_mouth_slight_smirk.png")
def scale_mouth(m):
    nw = max(8, int(m.width * MOUTH_SCALE))
    nh = max(8, int(m.height * MOUTH_SCALE))
    return m.resize((nw, nh), Image.LANCZOS)
mouth_neutral_s = scale_mouth(mouth_neutral)
mouth_smirk_s   = scale_mouth(mouth_smirk)
def mouth_pos(m_scaled):
    ax = int(MOUTH_INTRINSIC_ANCHOR[0] * MOUTH_SCALE)
    ay = int(MOUTH_INTRINSIC_ANCHOR[1] * MOUTH_SCALE)
    return (ST_MOUTH_XY[0] - ax, ST_MOUTH_XY[1] - ay)
MOUTH_POS = mouth_pos(mouth_neutral_s)
print(f"Mouth placement: {MOUTH_POS}")

# ── Composite builder ─────────────────────────────────────────────────────
def composite(mouth_layer=None):
    c = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    # Head + body baseline from See-through
    for n in ["back hair", "ears", "face", "eyebrow", "eyewhite", "irides"]:
        layer = place_st(n)
        if layer is not None: c.alpha_composite(layer)
    # Mouth — production, sits on face
    if mouth_layer is not None:
        c.alpha_composite(mouth_layer, MOUTH_POS)
    # Lower body
    for n in ["legwear", "footwear"]:
        layer = place_st(n)
        if layer is not None: c.alpha_composite(layer)
    # Handwear (See-through unmodified) — provides shoulder/arm bulk per Option B
    hw = place_st("handwear")
    if hw is not None: c.alpha_composite(hw)
    # Shirt+tie BEHIND jacket
    c.alpha_composite(shirt_tie, SHIRT_TL)
    # Jacket
    c.alpha_composite(jacket, JACKET_TL)
    # Belt over topwear
    c.alpha_composite(belt, BELT_TL)
    # Hands at cuffs
    c.alpha_composite(hand_R_s, HAND_R_POS)
    c.alpha_composite(hand_L_s, HAND_L_POS)
    return c

print("Building composites…")
fb_no_mouth = composite(mouth_layer=None)
fb_neutral  = composite(mouth_layer=mouth_neutral_s)
fb_smirk    = composite(mouth_layer=scale_mouth(mouth_smirk))

# ── QC sheets ─────────────────────────────────────────────────────────────
PAD, LBL_H = 10, 24

def panel(img, label, bg=(210,210,210,255)):
    p = Image.new("RGBA", (img.width + 20, img.height + LBL_H + 16), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 5), label, fill=(220,220,220))
    p.alpha_composite(img.convert("RGBA"), (10, LBL_H + 8))
    return p

# Stack QC: three full-body composites side-by-side
FB_W = 360
def thumb(img):
    return img.resize((FB_W, int(CH * FB_W / CW)), Image.LANCZOS)

p_no_mouth = panel(thumb(fb_no_mouth), "1. no-mouth baseline")
p_neutral  = panel(thumb(fb_neutral),  "2. + neutral mouth")
p_smirk    = panel(thumb(fb_smirk),    "3. + slight_smirk mouth")

stack_w = (p_no_mouth.width + PAD) * 3 + PAD
stack_h = p_no_mouth.height + 40
stack_sheet = Image.new("RGB", (stack_w, stack_h), (15,15,15))
sd = ImageDraw.Draw(stack_sheet)
sd.text((PAD, 8), "Full-body locked stack QC - 768x768 See-through canvas - locked: hands+belt+mouth+topwear", fill=(220,220,220))
x = PAD
for p in [p_no_mouth, p_neutral, p_smirk]:
    stack_sheet.paste(p.convert("RGB"), (x, 30))
    x += p.width + PAD
stack_sheet.save(OUT / "jack_full_body_locked_stack_qc.png")
print(f"Stack QC -> {stack_sheet.size}")

# Zoom QC: 4 critical zones × 2 mouths (neutral + smirk for face zoom)
FACE_BOX  = (360, 30, 460, 160)
WAIST_BOX = (290, 350, 530, 460)
LCUFF_BOX = (290, 380, 380, 480)   # char R hand (image-left)
RCUFF_BOX = (440, 380, 530, 480)   # char L hand (image-right)
ZOOM = 3

def zoom_panel(img, box, label, scale=ZOOM):
    crop = img.crop(box)
    z = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
    return panel(z, label)

z_face_n = zoom_panel(fb_neutral, FACE_BOX, "face zoom - neutral")
z_face_s = zoom_panel(fb_smirk,   FACE_BOX, "face zoom - slight_smirk")
z_waist  = zoom_panel(fb_neutral, WAIST_BOX, "waist/belt/collar/tie zoom")
z_lcuff  = zoom_panel(fb_neutral, LCUFF_BOX, "left cuff (char R hand) zoom")
z_rcuff  = zoom_panel(fb_neutral, RCUFF_BOX, "right cuff (char L hand) zoom")

zoom_rows = [
    [z_face_n, z_face_s],
    [z_waist],
    [z_lcuff, z_rcuff],
]
row_widths = [sum(p.width for p in r) + PAD*(len(r)-1) for r in zoom_rows]
zoom_sheet_w = max(row_widths) + PAD*2
zoom_sheet_h = sum(max(p.height for p in r) for r in zoom_rows) + PAD*(len(zoom_rows)-1) + 40
zoom_sheet = Image.new("RGB", (zoom_sheet_w, zoom_sheet_h), (15,15,15))
zd = ImageDraw.Draw(zoom_sheet)
zd.text((PAD, 8), "Full-body locked stack ZOOM QC", fill=(220,220,220))
y = 30
for r in zoom_rows:
    x = PAD
    for p in r:
        zoom_sheet.paste(p.convert("RGB"), (x, y))
        x += p.width + PAD
    y += max(p.height for p in r) + PAD
zoom_sheet.save(OUT / "jack_full_body_locked_stack_zoom_qc.png")
print(f"Zoom QC -> {zoom_sheet.size}")

# Layer-order labelled stack preview: render each layer in turn cumulatively
ORDER = [
    ("back hair",  lambda c: c.alpha_composite(place_st("back hair")) if place_st("back hair") else None),
    ("ears",       lambda c: c.alpha_composite(place_st("ears")) if place_st("ears") else None),
    ("face",       lambda c: c.alpha_composite(place_st("face")) if place_st("face") else None),
    ("eyebrow",    lambda c: c.alpha_composite(place_st("eyebrow")) if place_st("eyebrow") else None),
    ("eyewhite",   lambda c: c.alpha_composite(place_st("eyewhite")) if place_st("eyewhite") else None),
    ("irides",     lambda c: c.alpha_composite(place_st("irides")) if place_st("irides") else None),
    ("mouth(neutral)", lambda c: c.alpha_composite(mouth_neutral_s, MOUTH_POS)),
    ("legwear",    lambda c: c.alpha_composite(place_st("legwear")) if place_st("legwear") else None),
    ("footwear",   lambda c: c.alpha_composite(place_st("footwear")) if place_st("footwear") else None),
    ("handwear (ST unmodified)", lambda c: c.alpha_composite(place_st("handwear")) if place_st("handwear") else None),
    ("shirt+tie",  lambda c: c.alpha_composite(shirt_tie, SHIRT_TL)),
    ("jacket",     lambda c: c.alpha_composite(jacket, JACKET_TL)),
    ("belt",       lambda c: c.alpha_composite(belt, BELT_TL)),
    ("hand R",     lambda c: c.alpha_composite(hand_R_s, HAND_R_POS)),
    ("hand L",     lambda c: c.alpha_composite(hand_L_s, HAND_L_POS)),
]
# Render cumulative snapshots
cumulative = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
snapshots = []
SOURCE_TAG = {
    "back hair": "ST", "ears": "ST", "face": "ST", "eyebrow": "ST", "eyewhite": "ST",
    "irides": "ST", "mouth(neutral)": "PROD", "legwear": "ST", "footwear": "ST",
    "handwear (ST unmodified)": "ST", "shirt+tie": "PROD", "jacket": "PROD",
    "belt": "PROD", "hand R": "PROD", "hand L": "PROD",
}
for name, fn in ORDER:
    fn(cumulative)
    snapshots.append((name, cumulative.copy()))

# Layout: 5 cols, ceil(15/5)=3 rows
THUMB_W = 190
N_COLS = 5
N_ROWS = (len(snapshots) + N_COLS - 1) // N_COLS

def stack_thumb(snap, name, idx):
    t = snap.resize((THUMB_W, int(CH * THUMB_W / CW)), Image.LANCZOS)
    bg = Image.new("RGBA", t.size, (210, 210, 210, 255))
    bg.alpha_composite(t)
    src = SOURCE_TAG.get(name, "?")
    src_col = (30, 140, 30) if src == "PROD" else (160, 100, 30)
    p = Image.new("RGBA", (THUMB_W + 16, bg.height + LBL_H + 14), (28, 28, 28, 255))
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((4, 5), f"#{idx+1:02d} {name}", fill=(220,220,220))
    d.text((p.width - 35, 5), src, fill=src_col)
    p.alpha_composite(bg, (8, LBL_H + 6))
    return p

thumbs = [stack_thumb(s, n, i) for i, (n, s) in enumerate(snapshots)]
tw, th = thumbs[0].size
order_w = tw * N_COLS + PAD * (N_COLS + 1)
order_h = th * N_ROWS + PAD * (N_ROWS + 1) + 40
order_sheet = Image.new("RGB", (order_w, order_h), (15, 15, 15))
od = ImageDraw.Draw(order_sheet)
od.text((PAD, 8), "Layer-order test - cumulative back-to-front. Green=PROD, Orange=ST baseline (See-through)", fill=(220,220,220))
for i, p in enumerate(thumbs):
    r, c = divmod(i, N_COLS)
    order_sheet.paste(p.convert("RGB"), (PAD + c*(tw + PAD), 30 + r*(th + PAD)))
order_sheet.save(OUT / "jack_full_body_layer_order_test.png")
print(f"Order test -> {order_sheet.size}")

# ── Manifest ──────────────────────────────────────────────────────────────
manifest = {
    "qc_type": "full_body_integration",
    "revision": "r1",
    "canvas": [CW, CH],
    "production_assets_used": {
        "hands":    ["jack_hand_left.png", "jack_hand_right.png"],
        "belt":     ["jack_belt.png"],
        "mouth":    ["jack_mouth_neutral.png", "jack_mouth_slight_smirk.png"],
        "topwear":  ["jack_jacket.png", "jack_shirt_tie.png"],
    },
    "baseline_assets_used": {
        "see_through_extracted": ["back hair", "ears", "face", "eyebrow", "eyewhite",
                                  "irides", "legwear", "footwear", "handwear"]
    },
    "layer_order_back_to_front": [n for n, _ in ORDER],
    "anchors": {
        "jacket_tl":   list(JACKET_TL),
        "jacket_size": list(JACKET_SZ),
        "shirt_tl":    list(SHIRT_TL),
        "shirt_size":  list(SHIRT_SZ),
        "belt_tl":     list(BELT_TL),
        "belt_size":   list(BELT_SZ),
        "mouth_pos_on_canvas": list(MOUTH_POS),
        "mouth_scale_factor":  MOUTH_SCALE,
        "hand_R_pos":  list(HAND_R_POS), "hand_R_size": list(hand_R_s.size),
        "hand_L_pos":  list(HAND_L_POS), "hand_L_size": list(hand_L_s.size),
        "hand_scale":  HAND_SCALE,
        "cuff_y":      CUFF_Y,
    },
    "rules_followed": {
        "see_through_handwear_unmodified": True,
        "no_copainter_arms": True,
        "shirt_behind_jacket": True,
        "belt_over_topwear": True,
        "hands_at_cuffs": True,
        "mouth_over_face": True,
    },
    "categories_still_baseline_not_production": [
        "head (back hair, ears, face, eyebrow, eyewhite, irides)",
        "lower body (legwear, footwear)",
        "handwear (See-through used unmodified)"
    ],
}
(OUT / "full_body_integration_qc_r1_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest -> full_body_integration_qc_r1_manifest.json")
print("DONE")
