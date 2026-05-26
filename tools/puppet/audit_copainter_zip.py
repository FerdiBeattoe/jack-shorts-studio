"""
Audit CoPainter ZIP output — probe each layer, build contact sheet + recompose QC.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, os

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
ROOT = PROJECT / r"assets\puppet\cloud_layer_tests\copainter"
EXTR = ROOT / "extracted_layers_1779216312185"
CONTACT = ROOT / "copainter_layers_1779216312185_contact_sheet.png"
RECOMP  = ROOT / "copainter_layers_1779216312185_recompose_qc.png"
MANIFEST = ROOT / "copainter_layers_1779216312185_audit.json"

files = sorted(EXTR.glob("*.png"))
print(f"Layer files: {len(files)}")

layers = []
for p in files:
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    a = arr[..., 3]
    total = a.size
    op = int((a == 255).sum())
    tr = int((a == 0).sum())
    bbox = im.getbbox()
    if (a > 0).any():
        sel = arr[a > 0, :3]
        med = np.median(sel, axis=0).astype(int).tolist()
        mean = sel.mean(axis=0).astype(int).tolist()
    else:
        med = mean = None
    info = {
        "file": p.name,
        "size": list(im.size),
        "mode": im.mode,
        "bbox": list(bbox) if bbox else None,
        "opaque_pct": round(100*op/total, 2),
        "transparent_pct": round(100*tr/total, 2),
        "semi_alpha_pct": round(100*(total-op-tr)/total, 2),
        "median_rgb_opaque": med,
        "mean_rgb_opaque": mean,
        "_img": im,
    }
    layers.append(info)
    print(f"  {p.name:<14} {im.size}  bbox={bbox}  opaque={info['opaque_pct']}% med={med}")

# Heuristic semantic mapping by median colour + bbox position + size
def classify(L):
    med = L["median_rgb_opaque"]
    bbox = L["bbox"]
    if bbox is None or med is None: return "empty"
    w, h = L["size"]
    bx0, by0, bx1, by1 = bbox
    bw = bx1-bx0; bh = by1-by0
    bcy = (by0+by1)/2  # bbox vertical center
    bcx = (bx0+bx1)/2
    r, g, b = med
    # Background (huge area, plain colour)
    if L["opaque_pct"] > 50 and bw > w*0.8 and bh > h*0.8:
        return "background"
    # Golden fur (head, face, ears)
    if r > 180 and g > 120 and g < 220 and b < 160:
        if bh < h*0.2 and bcy < h*0.4: return "fur_top (back hair / ears / head crown)"
        if bcy < h*0.4: return "fur_head"
        return "fur_body"
    # Black / very dark (jacket, pants, shoes, tie)
    if r < 50 and g < 50 and b < 50:
        if bcy < h*0.5: return "jacket / top"
        if bcy > h*0.8: return "footwear"
        return "legwear / dark clothing"
    # White / cream (shirt, eyes)
    if r > 220 and g > 200 and b > 170:
        if bh < 30 and bw < 50: return "eye_white_small"
        return "shirt / collar / cream"
    # Pink / muzzle / nose
    if r > 200 and g > 130 and g < 200 and b > 100 and b < 180:
        return "muzzle / nose tip"
    # Iris / eye dark
    if bw < 30 and bh < 30:
        return "eye_detail"
    return f"unclassified (median rgb {med})"

print("\nHeuristic classification:")
for L in layers:
    L["guess"] = classify(L)
    print(f"  {L['file']:<14} -> {L['guess']}")

# ── Determine canvas size (largest) ─────────────────────────────────────────
CW = max(L["size"][0] for L in layers)
CH = max(L["size"][1] for L in layers)
print(f"\nMax canvas: {CW}x{CH}")

# ── Recompose: stack layers in numeric order (as filenames suggest depth) ──
# We'll stack in two orders for QC: by file order (numeric ascending) and reversed
def stack(order):
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for L in order:
        img = L["_img"]
        if img.size == (CW, CH):
            canvas.alpha_composite(img)
        elif L["bbox"]:
            # Place at bbox origin if it's bbox-cropped on a different-sized canvas
            canvas.alpha_composite(img, (0, 0))
    return canvas

stacked_asc = stack(layers)
stacked_desc = stack(list(reversed(layers)))

# ── Contact sheet ──────────────────────────────────────────────────────────
TILE_W = 360
PAD, LBL_H = 10, 28
def tile_for(L):
    img = L["_img"]
    bb = L["bbox"]
    crop = img.crop(bb) if bb else img
    s = TILE_W / max(crop.width, 1)
    nh = max(1, int(crop.height * s))
    rs = crop.resize((TILE_W, nh), Image.LANCZOS)
    # Tile on light grey
    h = nh + LBL_H + 16
    t = Image.new("RGBA", (TILE_W + 20, h + 30), (210, 210, 210, 255))
    d = ImageDraw.Draw(t)
    d.rectangle([(0,0),(t.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), f"{L['file']}", fill=(220, 220, 220))
    d.text((5, 14), f"bbox={L['bbox']} med={L['median_rgb_opaque']}", fill=(220, 220, 220))
    t.alpha_composite(rs, (10, LBL_H + 8))
    d.text((5, h + 4), f"-> {L['guess']}", fill=(20, 20, 20))
    return t

tiles = [tile_for(L) for L in layers]
COLS = 4
rows = (len(tiles) + COLS - 1) // COLS
tw, th = tiles[0].size
SW = tw * COLS + PAD * (COLS + 1)
SH = th * rows + PAD * (rows + 1) + 30
sheet = Image.new("RGB", (SW, SH), (15, 15, 15))
sd = ImageDraw.Draw(sheet)
sd.text((PAD, 8), f"CoPainter audit - {len(layers)} layers from layers_1779216312185.zip - canvas {CW}x{CH}", fill=(220,220,220))
for i, t in enumerate(tiles):
    r, c = divmod(i, COLS)
    sheet.paste(t.convert("RGB"), (PAD + c*(tw + PAD), 30 + PAD + r*(th + PAD)))
sheet.save(CONTACT)
print(f"\nContact sheet: {CONTACT}  ({sheet.size})")

# ── Recompose QC sheet ─────────────────────────────────────────────────────
def label_panel(img, text, w=None):
    iw = w or img.width
    p = Image.new("RGBA", (iw + 20, img.height + LBL_H + 16), (28, 28, 28, 255))
    d = ImageDraw.Draw(p)
    d.rectangle([(0,0),(p.width-1, LBL_H-1)], fill=(50,50,50,255))
    d.text((5, 4), text, fill=(220,220,220))
    p.alpha_composite(img.convert("RGBA"), (10, LBL_H + 8))
    return p

# Scale stacked images
def to_thumb(im, w):
    s = w / im.width
    return im.resize((w, int(im.height * s)), Image.LANCZOS)

asc_thumb  = to_thumb(stacked_asc.convert("RGBA"),  600)
desc_thumb = to_thumb(stacked_desc.convert("RGBA"), 600)
# Add a light-grey backdrop variant
def on_bg(im, bg):
    canvas = Image.new("RGBA", im.size, bg)
    canvas.alpha_composite(im)
    return canvas

asc_light  = on_bg(asc_thumb,  (210,210,210,255))
desc_light = on_bg(desc_thumb, (210,210,210,255))
asc_dark   = on_bg(asc_thumb,  (40,40,40,255))

p1 = label_panel(asc_light,  "Stacked numerical ascending (01 -> 80) on light")
p2 = label_panel(desc_light, "Stacked descending (80 -> 01) on light")
p3 = label_panel(asc_dark,   "Stacked ascending on dark")

# Compose recompose sheet
RC_W = max(p.width for p in [p1,p2,p3]) + PAD*2
RC_H = sum(p.height for p in [p1,p2,p3]) + PAD*4 + 30
rc = Image.new("RGB", (RC_W, RC_H), (15,15,15))
rd = ImageDraw.Draw(rc)
rd.text((PAD, 8), "CoPainter recompose QC - stack tests", fill=(220,220,220))
y = 30
for p in [p1, p2, p3]:
    rc.paste(p.convert("RGB"), (PAD, y))
    y += p.height + PAD
rc.save(RECOMP)
print(f"Recompose QC: {RECOMP}  ({rc.size})")

# ── Write manifest ─────────────────────────────────────────────────────────
out = {
    "zip_source": "layers_1779216312185.zip (CoPainter export)",
    "extracted_to": str(EXTR),
    "layer_count": len(layers),
    "canvas": [CW, CH],
    "layers": [{k:v for k,v in L.items() if not k.startswith("_")} for L in layers],
}
MANIFEST.write_text(json.dumps(out, indent=2))
print(f"Audit manifest: {MANIFEST}")
print("DONE")
