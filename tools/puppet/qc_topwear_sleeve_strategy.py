"""
QC ONLY — compare 4 sleeve-integration strategies for the CoPainter topwear split.

A: CoPainter jacket + shirt+tie + promoted belt + promoted hands. NO See-through handwear.
B: Same as A + See-through handwear unmodified. Exposes the known black-strip failure.
C: Same as A + See-through handwear MASKED to keep only pixels inside/below the jacket
   silhouette (hides lateral overhang, preserves any cuff support).
D: Original See-through merged topwear + promoted belt + promoted hands (baseline).

Outputs (assets/puppet/layers_staging/topwear_r1/sleeve_strategy_qc/):
  jack_topwear_sleeve_strategy_qc.png
  jack_topwear_sleeve_strategy_zoom_qc.png
  sleeve_strategy_manifest.json
  sleeve_strategy_notes.md (written separately)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import json

PROJECT  = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
STAG_TOP = PROJECT / r"assets\puppet\layers_staging\topwear_r1"
JACKET   = STAG_TOP / "jack_jacket_r1.png"
SHIRT    = STAG_TOP / "jack_shirt_tie_r1.png"
TOP_MAN  = STAG_TOP / "topwear_r1_manifest.json"
SEETHRU  = PROJECT / r"assets\puppet\cloud_layer_tests\see_through\extracted"
ST_MAN   = SEETHRU / "layer_manifest.json"
BELT_PNG = PROJECT / r"assets\puppet\layers\belt\jack_belt.png"
BELT_MAN = PROJECT / r"assets\puppet\layers\belt\manifest.json"
HAND_L   = PROJECT / r"assets\puppet\layers\hands\jack_hand_left.png"
HAND_R   = PROJECT / r"assets\puppet\layers\hands\jack_hand_right.png"
HANDS_MAN = PROJECT / r"assets\puppet\layers\hands\manifest.json"

OUT = STAG_TOP / "sleeve_strategy_qc"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load all assets ─────────────────────────────────────────────────────────
top_mani = json.loads(TOP_MAN.read_text())
st_mani  = json.loads(ST_MAN.read_text())
CW, CH = st_mani["canvas"]

def L(name):
    return next((x for x in st_mani["layers"] if x.get("name") == name), None)

def place_st(name):
    info = L(name)
    if info is None or not info.get("png"): return None, None
    img = Image.open(SEETHRU / info["png"]).convert("RGBA")
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    canvas.alpha_composite(img, (info["bbox"][0], info["bbox"][1]))
    return canvas, info["bbox"]

jacket_src = Image.open(JACKET).convert("RGBA")
shirt_src  = Image.open(SHIRT).convert("RGBA")
belt_src   = Image.open(BELT_PNG).convert("RGBA")
hand_L_src = Image.open(HAND_L).convert("RGBA")
hand_R_src = Image.open(HAND_R).convert("RGBA")

# Pull placement from topwear staging manifest
fc = top_mani["full_canvas_test"]
JACKET_TL = tuple(fc["jacket_topleft_on_canvas"])
JACKET_SZ = tuple(fc["jacket_size_on_canvas"])
SHIRT_TL  = tuple(fc["shirt_tie_topleft_on_canvas"])
SHIRT_SZ  = tuple(fc["shirt_tie_size_on_canvas"])
jacket_scaled = jacket_src.resize(JACKET_SZ, Image.LANCZOS)
shirt_scaled  = shirt_src.resize(SHIRT_SZ,  Image.LANCZOS)

# Belt from production manifest
belt_mani = json.loads(BELT_MAN.read_text())
BELT_TL = tuple(belt_mani["anchor"]["topleft_in_canvas"])
BELT_SZ = tuple(belt_mani["anchor"]["scaled_size_on_canvas"])
belt_scaled = belt_src.resize(BELT_SZ, Image.LANCZOS)

# Hands: scale and anchor at sleeve cuff zones on See-through canvas.
# Topwear bottom = JACKET_TL[1] + JACKET_SZ[1] = 152 + 276 = 428
# Hand scale for See-through canvas: 0.42 (consistent with prior composite QC)
HAND_SCALE = 0.42
hand_L_scaled = hand_L_src.resize((int(hand_L_src.width * HAND_SCALE), int(hand_L_src.height * HAND_SCALE)), Image.LANCZOS)
hand_R_scaled = hand_R_src.resize((int(hand_R_src.width * HAND_SCALE), int(hand_R_src.height * HAND_SCALE)), Image.LANCZOS)
# Anchor: just inside jacket left/right edges, top at sleeve cuff line ≈ jacket bottom
JACKET_RIGHT = JACKET_TL[0] + JACKET_SZ[0]   # 505
JACKET_BOT   = JACKET_TL[1] + JACKET_SZ[1]   # 428
CUFF_Y       = JACKET_BOT - 18               # 410 — hand top sits ~18px above jacket bottom (slight overlap)
HAND_R_POS = (JACKET_TL[0] - hand_R_scaled.width // 2 + 10,  CUFF_Y - 6)   # char-R hand, image-LEFT side
HAND_L_POS = (JACKET_RIGHT - hand_L_scaled.width // 2 - 10, CUFF_Y - 6)   # char-L hand, image-RIGHT side

# ── Pre-build See-through "core" body without handwear and without topwear ──
ST_BODY_NO_TOP_NO_HW = ["back hair", "ears", "face", "eyebrow", "eyewhite", "irides",
                        "legwear", "footwear"]
def core_body():
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for n in ST_BODY_NO_TOP_NO_HW:
        layer, _ = place_st(n)
        if layer is not None: canvas.alpha_composite(layer)
    return canvas

# ── Option A: CoPainter top + belt + hands, NO See-through handwear ────────
def option_A():
    c = core_body()
    c.alpha_composite(shirt_scaled,  SHIRT_TL)
    c.alpha_composite(jacket_scaled, JACKET_TL)
    c.alpha_composite(belt_scaled,   BELT_TL)
    c.alpha_composite(hand_R_scaled, HAND_R_POS)
    c.alpha_composite(hand_L_scaled, HAND_L_POS)
    return c

# ── Option B: same + See-through handwear UNMODIFIED ───────────────────────
def option_B():
    c = core_body()
    hw_canvas, _ = place_st("handwear")
    if hw_canvas is not None:
        c.alpha_composite(hw_canvas)
    c.alpha_composite(shirt_scaled,  SHIRT_TL)
    c.alpha_composite(jacket_scaled, JACKET_TL)
    c.alpha_composite(belt_scaled,   BELT_TL)
    c.alpha_composite(hand_R_scaled, HAND_R_POS)
    c.alpha_composite(hand_L_scaled, HAND_L_POS)
    return c

# ── Option C: See-through handwear MASKED ──────────────────────────────────
# Strategy: keep handwear pixels ONLY where the jacket silhouette covers them OR
# they sit below the jacket bottom (cuff support). This deterministic mask hides
# any lateral overhang.
def option_C():
    c = core_body()
    hw_canvas, _ = place_st("handwear")
    if hw_canvas is not None:
        # Build jacket silhouette on full canvas
        jkt_alpha_canvas = Image.new("L", (CW, CH), 0)
        jkt_alpha_canvas.paste(jacket_scaled.split()[3], JACKET_TL)
        jkt_arr = np.array(jkt_alpha_canvas)
        # Allow a small horizontal pad inside jacket silhouette
        # Build a "below jacket bottom" mask too
        below_mask = np.zeros((CH, CW), dtype=np.uint8)
        below_mask[JACKET_BOT - 4:] = 255
        # keep = jacket_alpha > 50  OR  y > jacket_bottom-4
        keep_mask = ((jkt_arr > 50) | (below_mask > 50)).astype(np.uint8) * 255
        # Apply mask to handwear alpha
        hw_arr = np.array(hw_canvas)
        hw_alpha = hw_arr[..., 3].copy()
        hw_alpha = np.where(keep_mask > 0, hw_alpha, 0).astype(np.uint8)
        hw_arr[..., 3] = hw_alpha
        hw_masked = Image.fromarray(hw_arr, mode="RGBA")
        c.alpha_composite(hw_masked)
    c.alpha_composite(shirt_scaled,  SHIRT_TL)
    c.alpha_composite(jacket_scaled, JACKET_TL)
    c.alpha_composite(belt_scaled,   BELT_TL)
    c.alpha_composite(hand_R_scaled, HAND_R_POS)
    c.alpha_composite(hand_L_scaled, HAND_L_POS)
    return c

# ── Option D: pure See-through baseline + belt + hands (no CoPainter top) ──
def option_D():
    c = core_body()
    for n in ["handwear", "topwear"]:
        layer, _ = place_st(n)
        if layer is not None: c.alpha_composite(layer)
    c.alpha_composite(belt_scaled,   BELT_TL)
    c.alpha_composite(hand_R_scaled, HAND_R_POS)
    c.alpha_composite(hand_L_scaled, HAND_L_POS)
    return c

print("Building Option A…")
A = option_A()
print("Building Option B…")
B = option_B()
print("Building Option C (masked handwear)…")
C = option_C()
print("Building Option D (See-through baseline)…")
D = option_D()

# ── Diff metric: count strip pixels (handwear-only pixels outside jacket) ──
def count_overhang(option_img):
    # Count opaque pixels in the area where See-through handwear extends past
    # the jacket silhouette (lateral overhang zone).
    jkt_alpha_canvas = Image.new("L", (CW, CH), 0)
    jkt_alpha_canvas.paste(jacket_scaled.split()[3], JACKET_TL)
    jkt_arr = np.array(jkt_alpha_canvas)
    hw_canvas, _ = place_st("handwear")
    if hw_canvas is None: return 0
    hw_arr = np.array(hw_canvas)[..., 3]
    # Lateral overhang region: handwear opaque AND jacket transparent AND y in jacket range
    overhang_zone = (hw_arr > 50) & (jkt_arr <= 50) & \
                    (np.arange(CH)[:, None] >= JACKET_TL[1]) & \
                    (np.arange(CH)[:, None] < JACKET_BOT - 4)
    # Now measure how many of those pixels survive in each option
    opt_arr = np.array(option_img)[..., 3]
    surviving = int(((opt_arr > 50) & overhang_zone).sum())
    total_overhang = int(overhang_zone.sum())
    return surviving, total_overhang

A_surv, OV_TOT = count_overhang(A)
B_surv, _      = count_overhang(B)
C_surv, _      = count_overhang(C)
D_surv, _      = count_overhang(D)
print(f"Overhang zone has {OV_TOT} px total. Surviving pixels per option:")
print(f"  A={A_surv}  B={B_surv}  C={C_surv}  D={D_surv}")

# ── QC sheet 1 (full body comparison) ───────────────────────────────────────
PAD, LBL_H = 10, 24

def panel(img, label, bg=(210,210,210,255), max_w=None):
    if max_w and img.width > max_w:
        s = max_w / img.width
        img = img.resize((max_w, int(img.height * s)), Image.LANCZOS)
    p = Image.new("RGBA", (img.width + 20, img.height + LBL_H + 16), bg)
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 5), label, fill=(220,220,220))
    p.alpha_composite(img, (10, LBL_H + 8))
    return p

# Full body thumbs
FB_W = 320
def fb_thumb(img):
    return img.resize((FB_W, int(CH * FB_W / CW)), Image.LANCZOS)

pA = panel(fb_thumb(A), f"A. CoPainter top + hands + belt. NO ST handwear. overhang_surv={A_surv}/{OV_TOT}")
pB = panel(fb_thumb(B), f"B. Same + ST handwear unmodified. overhang_surv={B_surv}/{OV_TOT}")
pC = panel(fb_thumb(C), f"C. Same + ST handwear masked to jacket+below. overhang_surv={C_surv}/{OV_TOT}")
pD = panel(fb_thumb(D), f"D. See-through baseline topwear + handwear. overhang_surv={D_surv}/{OV_TOT}")

# Verdict line
sheet1 = Image.new("RGB", (FB_W*2 + PAD*3 + 40, pA.height*2 + PAD*3 + 40), (15,15,15))
sd = ImageDraw.Draw(sheet1)
sd.text((PAD, 8), "Sleeve strategy QC - 4 composites on 768x768 See-through canvas", fill=(220,220,220))
sheet1.paste(pA.convert("RGB"), (PAD, 30))
sheet1.paste(pB.convert("RGB"), (PAD + pA.width + PAD, 30))
sheet1.paste(pC.convert("RGB"), (PAD, 30 + pA.height + PAD))
sheet1.paste(pD.convert("RGB"), (PAD + pA.width + PAD, 30 + pA.height + PAD))
sheet1.save(OUT / "jack_topwear_sleeve_strategy_qc.png")
print(f"QC sheet 1 -> {sheet1.size}")

# ── QC sheet 2 (zoom comparisons) ───────────────────────────────────────────
# Three zoom regions
LEFT_WRIST  = (JACKET_TL[0] - 60, JACKET_BOT - 60, JACKET_TL[0] + 60, JACKET_BOT + 80)
RIGHT_WRIST = (JACKET_RIGHT - 60, JACKET_BOT - 60, JACKET_RIGHT + 60, JACKET_BOT + 80)
WAIST       = (JACKET_TL[0] - 10, JACKET_BOT - 80, JACKET_RIGHT + 10, JACKET_BOT + 20)

def zoom(img, box, scale=3):
    crop = img.crop(box)
    return crop.resize((crop.width*scale, crop.height*scale), Image.NEAREST)

def zoom_row(box, label):
    panels_z = []
    for name, im in [("A", A), ("B", B), ("C", C), ("D", D)]:
        z = zoom(im, box)
        panels_z.append(panel(z, f"{name} - {label}"))
    # Compose row
    rw = sum(p.width for p in panels_z) + PAD*(len(panels_z)-1)
    rh = max(p.height for p in panels_z)
    row = Image.new("RGB", (rw, rh), (15,15,15))
    x = 0
    for p in panels_z:
        row.paste(p.convert("RGB"), (x, 0))
        x += p.width + PAD
    return row

row_lw = zoom_row(LEFT_WRIST,  "left wrist (char R)")
row_rw = zoom_row(RIGHT_WRIST, "right wrist (char L)")
row_wb = zoom_row(WAIST,       "waist/belt/jacket bottom")

sheet2_w = max(row_lw.width, row_rw.width, row_wb.width) + PAD*2
sheet2_h = row_lw.height + row_rw.height + row_wb.height + PAD*4 + 40
sheet2 = Image.new("RGB", (sheet2_w, sheet2_h), (15,15,15))
sd2 = ImageDraw.Draw(sheet2)
sd2.text((PAD, 8), "Sleeve strategy ZOOM QC - 3x zoom on critical regions for A/B/C/D", fill=(220,220,220))
sheet2.paste(row_lw, (PAD, 35))
sheet2.paste(row_rw, (PAD, 35 + row_lw.height + PAD))
sheet2.paste(row_wb, (PAD, 35 + row_lw.height + PAD + row_rw.height + PAD))
sheet2.save(OUT / "jack_topwear_sleeve_strategy_zoom_qc.png")
print(f"QC sheet 2 -> {sheet2.size}")

# ── Manifest ───────────────────────────────────────────────────────────────
manifest = {
    "qc_type": "sleeve_integration_strategy",
    "purpose": "Decide how to integrate CoPainter topwear split with See-through handwear before promoting topwear.",
    "canvas": [CW, CH],
    "anchors_used": {
        "jacket_tl": list(JACKET_TL), "jacket_size": list(JACKET_SZ),
        "shirt_tl":  list(SHIRT_TL),  "shirt_size":  list(SHIRT_SZ),
        "belt_tl":   list(BELT_TL),   "belt_size":   list(BELT_SZ),
        "hand_scale": HAND_SCALE,
        "hand_R_pos": list(HAND_R_POS), "hand_R_size": list(hand_R_scaled.size),
        "hand_L_pos": list(HAND_L_POS), "hand_L_size": list(hand_L_scaled.size),
        "cuff_y": CUFF_Y, "jacket_right": JACKET_RIGHT, "jacket_bottom": JACKET_BOT,
    },
    "options": {
        "A": {
            "description": "CoPainter jacket + shirt+tie + promoted belt + promoted hands. NO See-through handwear.",
            "overhang_surviving_px": A_surv,
            "overhang_zone_total_px": OV_TOT,
        },
        "B": {
            "description": "Same as A + See-through handwear unmodified.",
            "overhang_surviving_px": B_surv,
            "overhang_zone_total_px": OV_TOT,
        },
        "C": {
            "description": "Same as A + See-through handwear masked to (jacket silhouette OR y > jacket_bottom-4).",
            "mask_method": "deterministic numpy mask: keep_handwear = (jacket_alpha > 50) | (y >= jacket_bottom-4)",
            "overhang_surviving_px": C_surv,
            "overhang_zone_total_px": OV_TOT,
        },
        "D": {
            "description": "See-through baseline: original See-through merged topwear + handwear + promoted belt + hands. CoPainter topwear NOT used.",
            "overhang_surviving_px": D_surv,
            "overhang_zone_total_px": OV_TOT,
        },
    },
    "metric_note": "overhang_surviving_px counts opaque pixels in the 'lateral overhang zone' = where See-through handwear extends past the jacket silhouette within the jacket's y-range. Lower = cleaner. 0 = no strip-overhang visible.",
}
(OUT / "sleeve_strategy_manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Manifest -> sleeve_strategy_manifest.json")
print("DONE")
