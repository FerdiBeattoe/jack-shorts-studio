"""
Audit-only export of the See-through cloud PSD.

Input:  assets/puppet/cloud_layer_tests/see_through/seethrough_output.psd
Output: assets/puppet/cloud_layer_tests/see_through/extracted/
        - one PNG per leaf layer (transparent where applicable)
        - layer_manifest.json
        - see_through_contact_sheet.png
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import re
import sys

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
ROOT    = PROJECT / r"assets\puppet\cloud_layer_tests\see_through"
PSD     = ROOT / "seethrough_output.psd"
OUT     = ROOT / "extracted"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = OUT / "layer_manifest.json"
CONTACT  = ROOT / "see_through_contact_sheet.png"

if not PSD.exists():
    sys.exit(f"ERROR: {PSD} not found")

from psd_tools import PSDImage

print(f"Opening {PSD}…")
psd = PSDImage.open(PSD)
print(f"Canvas: {psd.width} x {psd.height}  mode={psd.color_mode}  layers(top-level)={len(list(psd))}")

# Walk the layer tree (depth-first, leaves only)
def walk(layers, path=()):
    for layer in layers:
        new_path = path + (layer.name or f"<unnamed_{layer.layer_id}>",)
        if layer.is_group():
            yield from walk(layer, new_path)
        else:
            yield new_path, layer

def slugify(parts):
    s = "__".join(parts)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:120] or "layer"

leaves = list(walk(psd))
print(f"Leaf layers: {len(leaves)}")

manifest = {
    "source_psd": str(PSD),
    "canvas": [psd.width, psd.height],
    "color_mode": str(psd.color_mode),
    "leaf_count": len(leaves),
    "layers": [],
}

exports = []  # (slug, png_path, layer_info)
for i, (path_tuple, layer) in enumerate(leaves):
    slug = f"{i:02d}_{slugify(path_tuple)}"
    out_png = OUT / f"{slug}.png"
    info = {
        "index": i,
        "path": list(path_tuple),
        "name": layer.name,
        "visible": layer.visible,
        "opacity": layer.opacity,
        "blend_mode": str(layer.blend_mode),
        "kind": layer.kind,
        "bbox": list(layer.bbox) if layer.bbox else None,
        "size": [layer.width, layer.height],
        "png": out_png.name,
        "error": None,
    }
    try:
        img = layer.composite()  # returns PIL Image, may be None if empty
        if img is None:
            info["error"] = "composite returned None (empty layer)"
        else:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            img.save(out_png)
            info["exported_size"] = list(img.size)
            exports.append((slug, out_png, info, img))
    except Exception as e:
        info["error"] = f"{type(e).__name__}: {e}"
        print(f"  [{i:02d}] {' / '.join(path_tuple)}  → ERROR: {info['error']}")
        continue
    print(f"  [{i:02d}] {' / '.join(path_tuple):<60} bbox={info['bbox']} mode={img.mode}")
    manifest["layers"].append(info)

# Also include layers with errors in manifest
for i, (path_tuple, layer) in enumerate(leaves):
    if not any(m["index"] == i for m in manifest["layers"]):
        manifest["layers"].append({
            "index": i,
            "path": list(path_tuple),
            "name": layer.name,
            "visible": layer.visible,
            "blend_mode": str(layer.blend_mode),
            "kind": layer.kind,
            "bbox": list(layer.bbox) if layer.bbox else None,
            "exported": False,
        })

MANIFEST.write_text(json.dumps(manifest, indent=2))
print(f"Manifest: {MANIFEST}")

# ── Contact sheet ────────────────────────────────────────────────────────────
# Each panel: canvas-sized layer on light grey, with label and small notes.
# To keep the sheet readable, downscale each layer to fit in a thumbnail cell.
THUMB_W = 320
COLS    = 4
PAD     = 10
LBL_H   = 30

# Filter: skip layers with no bbox (empty) for the sheet
valid = [e for e in exports if e[3].size != (0, 0)]
print(f"Exports for contact sheet: {len(valid)}")

# Compute thumb size keeping aspect = canvas aspect (the layer image we get is canvas-sized in psd-tools >=1.10)
canvas_w, canvas_h = psd.width, psd.height
aspect = canvas_h / canvas_w
THUMB_H = int(THUMB_W * aspect)

CELL_W = THUMB_W + PAD * 2
CELL_H = THUMB_H + PAD * 2 + LBL_H

rows = (len(valid) + COLS - 1) // COLS or 1
sheet_w = CELL_W * COLS + PAD
sheet_h = CELL_H * rows + PAD + 40  # +40 for header
sheet = Image.new("RGB", (sheet_w, sheet_h), (20, 20, 20))
sd = ImageDraw.Draw(sheet)
sd.text((PAD, 10), f"See-through PSD audit · {PSD.name} · canvas {canvas_w}x{canvas_h} · {len(valid)} layers shown",
        fill=(220, 220, 220))

LIGHT = (200, 200, 200, 255)
for i, (slug, png_path, info, img) in enumerate(valid):
    r, c = divmod(i, COLS)
    cx = PAD + c * CELL_W
    cy = 40 + r * CELL_H
    cell = Image.new("RGBA", (CELL_W, CELL_H), (32, 32, 32, 255))
    cd = ImageDraw.Draw(cell)
    cd.rectangle([(0, 0), (CELL_W - 1, LBL_H - 1)], fill=(50, 50, 50, 255))
    label = f"[{info['index']:02d}] {' / '.join(info['path'])}"
    if len(label) > 52:
        label = label[:49] + "…"
    cd.text((6, 5), label, fill=(220, 220, 220))
    bbox_str = f"bbox={info.get('bbox')}  blend={info['blend_mode'].split('.')[-1]}"
    cd.text((6, 16), bbox_str[:60], fill=(170, 170, 170))

    # Composite layer thumb on light grey
    thumb_bg = Image.new("RGBA", (THUMB_W, THUMB_H), LIGHT)
    layer_thumb = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
    thumb_bg.alpha_composite(layer_thumb)
    cell.alpha_composite(thumb_bg, (PAD, LBL_H + PAD))
    sheet.paste(cell.convert("RGB"), (cx, cy))

sheet.save(CONTACT)
print(f"Contact sheet -> {CONTACT}  ({sheet.width}x{sheet.height})")
print("DONE")
