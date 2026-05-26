"""
Deterministic procedural mouth/viseme generator for Jack's puppet rig.

Style target: simple black lineart on transparent, tired/deadpan, dog-stylised
not anime, not cute, not realistic. Matches production canvas convention:
  - 512x512 RGBA
  - mouth artwork centered around (256, 270)
  - line weight ~5 px at final res
  - interior fill (open mouths) = dark muted maroon-brown

Outputs (assets/puppet/layers_staging/mouth_r1/):
  jack_mouth_neutral_r1.png
  jack_mouth_slight_frown_r1.png
  jack_mouth_slight_smirk_r1.png
  jack_mouth_open_small_r1.png
  jack_mouth_open_medium_r1.png
  jack_mouth_oo_r1.png
  jack_mouth_ee_r1.png
  jack_mouth_fv_r1.png
  jack_mouth_mbp_r1.png
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT = PROJECT / r"assets\puppet\layers_staging\mouth_r1"
OUT.mkdir(parents=True, exist_ok=True)

# ── Canvas / style constants ─────────────────────────────────────────────────
W = H = 512
ANCHOR = (256, 270)    # mouth-centroid anchor matching existing production set
SS = 4                  # supersample factor for anti-aliasing
WW, HH = W * SS, H * SS
AX, AY = ANCHOR[0] * SS, ANCHOR[1] * SS

LINE = (20, 20, 20, 255)            # black lineart (slightly off-pure-black to feel hand-drawn)
INTERIOR = (88, 36, 32, 255)        # dark maroon dog-mouth interior
TONGUE = (160, 70, 78, 255)         # warmer tongue accent
TOOTH = (240, 235, 220, 255)        # off-white teeth (matches Jack's shirt cream tone)
LINE_W_REL = 5                      # final-res line weight in px
LINE_W = LINE_W_REL * SS

# ── Helpers ──────────────────────────────────────────────────────────────────
def new_canvas():
    return Image.new("RGBA", (WW, HH), (0, 0, 0, 0))

def downsample(img):
    return img.resize((W, H), Image.LANCZOS)

def quad_bezier(p0, p1, p2, steps=64):
    ts = np.linspace(0, 1, steps)
    xs = (1-ts)**2 * p0[0] + 2*(1-ts)*ts*p1[0] + ts**2 * p2[0]
    ys = (1-ts)**2 * p0[1] + 2*(1-ts)*ts*p1[1] + ts**2 * p2[1]
    return list(zip(xs.tolist(), ys.tolist()))

def cubic_bezier(p0, p1, p2, p3, steps=80):
    ts = np.linspace(0, 1, steps)
    xs = (1-ts)**3*p0[0] + 3*(1-ts)**2*ts*p1[0] + 3*(1-ts)*ts**2*p2[0] + ts**3*p3[0]
    ys = (1-ts)**3*p0[1] + 3*(1-ts)**2*ts*p1[1] + 3*(1-ts)*ts**2*p2[1] + ts**3*p3[1]
    return list(zip(xs.tolist(), ys.tolist()))

def stroke(draw, pts, color=LINE, width=LINE_W):
    draw.line(pts, fill=color, width=width, joint="curve")
    # End caps to avoid square ends
    for p in (pts[0], pts[-1]):
        r = width // 2
        draw.ellipse((p[0]-r, p[1]-r, p[0]+r, p[1]+r), fill=color)

def save(img, name):
    out_path = OUT / f"{name}.png"
    img.save(out_path)
    return out_path

# Local coords are relative to anchor (positive x = right, positive y = down).
def L(x, y):  # supersampled absolute pixel
    return (AX + x*SS, AY + y*SS)

# ── 1. neutral ──────────────────────────────────────────────────────────────
# Slightly tired deadpan: wide shallow line with a tiny dip at center
# (mimics existing production neutral.png: corners y=258 → center y=306 → very subtle V).
def make_neutral():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    # Wide shallow curve: left corner up, dips to a flat center, back up to right corner
    pts = cubic_bezier(L(-135, -6), L(-50, 30), L(50, 30), L(135, -6), steps=120)
    stroke(d, pts)
    # Tiny center jaw indicator (very faint) - skip to keep deadpan
    return img

# ── 2. slight_frown ─────────────────────────────────────────────────────────
# Corners droop more, center is slightly lower; still understated
def make_slight_frown():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    pts = cubic_bezier(L(-130, -18), L(-50, 38), L(50, 38), L(130, -18), steps=120)
    stroke(d, pts)
    return img

# ── 3. slight_smirk ─────────────────────────────────────────────────────────
# Asymmetric: left side flat/slightly down, right corner lifts up
def make_slight_smirk():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    # Left half - subtle downward then flat
    left = cubic_bezier(L(-130, -2), L(-70, 18), L(-20, 14), L(20, 4), steps=80)
    # Right half - lifts upward
    right = cubic_bezier(L(20, 4), L(60, -8), L(95, -22), L(130, -32), steps=80)
    stroke(d, left)
    stroke(d, right)
    return img

# ── 4. open_small ───────────────────────────────────────────────────────────
# Small horizontal ellipse, dark interior
def make_open_small():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    # Interior fill first (filled ellipse), then outline
    rx, ry = 55, 16
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=INTERIOR)
    # Outline
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    # Subtle tongue hint at bottom (a small arc inside)
    tx, ty = 30, 8
    d.chord((AX - tx*SS, AY + (ry-12)*SS, AX + tx*SS, AY + (ry+4)*SS), 0, 180, fill=TONGUE)
    return img

# ── 5. open_medium ──────────────────────────────────────────────────────────
def make_open_medium():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    rx, ry = 75, 26
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=INTERIOR)
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    # Tongue fills lower portion
    tx, ty = 50, 14
    d.chord((AX - tx*SS, AY, AX + tx*SS, AY + (ry+6)*SS), 0, 180, fill=TONGUE)
    return img

# ── 6. oo (pursed round) ────────────────────────────────────────────────────
# Small vertical-leaning oval, like saying "ooh"; smaller than open_small
def make_oo():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    rx, ry = 28, 24
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=INTERIOR)
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    return img

# ── 7. ee (wide flat with subtle teeth) ────────────────────────────────────
# Two horizontal lines (upper edge & lower edge) with a thin pale stripe between
# representing front teeth. No individual tooth divisions (style: not realistic).
def make_ee():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    half_w = 100
    upper_y = -10
    lower_y = 8
    # Pale tooth strip
    d.polygon([L(-half_w+6, upper_y+2), L(half_w-6, upper_y+2),
               L(half_w-6, lower_y-2), L(-half_w+6, lower_y-2)], fill=TOOTH)
    # Upper line
    upper = cubic_bezier(L(-half_w, upper_y), L(-30, upper_y-2), L(30, upper_y-2), L(half_w, upper_y), steps=80)
    stroke(d, upper)
    # Lower line
    lower = cubic_bezier(L(-half_w, lower_y), L(-30, lower_y+3), L(30, lower_y+3), L(half_w, lower_y), steps=80)
    stroke(d, lower)
    # Corner connectors (small)
    d.line([L(-half_w, upper_y), L(-half_w+4, lower_y)], fill=LINE, width=LINE_W)
    d.line([L( half_w, upper_y), L( half_w-4, lower_y)], fill=LINE, width=LINE_W)
    return img

# ── 8. fv (upper teeth on lower lip) ────────────────────────────────────────
# Flat lower-lip line with a row of upper teeth resting on it
def make_fv():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    half_w = 70
    lip_y = 12
    teeth_top_y = -10
    # Teeth rectangle: pale tooth band on top of lip line
    d.polygon([L(-half_w+8, teeth_top_y), L(half_w-8, teeth_top_y),
               L(half_w-8, lip_y-2),    L(-half_w+8, lip_y-2)], fill=TOOTH)
    # Lip line below
    lip = cubic_bezier(L(-half_w-12, lip_y+2), L(-40, lip_y+5), L(40, lip_y+5), L(half_w+12, lip_y+2), steps=80)
    stroke(d, lip)
    # Upper teeth outline (chord-like)
    teeth_outline = [
        L(-half_w+8, teeth_top_y), L(half_w-8, teeth_top_y),
        L(half_w-8, lip_y-2), L(-half_w+8, lip_y-2), L(-half_w+8, teeth_top_y),
    ]
    d.line(teeth_outline, fill=LINE, width=LINE_W, joint="curve")
    # Two faint tooth dividers (very subtle)
    for x in (-22, 22):
        d.line([L(x, teeth_top_y+4), L(x, lip_y-4)], fill=(60,60,60,170), width=max(1, LINE_W // 2))
    return img

# ── 9. mbp (tight closed) ──────────────────────────────────────────────────
# Short tight flat horizontal line; lips pressed
def make_mbp():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    pts = cubic_bezier(L(-80, 0), L(-30, 3), L(30, 3), L(80, 0), steps=80)
    stroke(d, pts, width=LINE_W + 2*SS)  # slightly thicker - lips compressed
    return img

# ── Build all ───────────────────────────────────────────────────────────────
VISEMES = {
    "jack_mouth_neutral_r1":       ("neutral",       make_neutral),
    "jack_mouth_slight_frown_r1":  ("slight_frown",  make_slight_frown),
    "jack_mouth_slight_smirk_r1":  ("slight_smirk",  make_slight_smirk),
    "jack_mouth_open_small_r1":    ("open_small",    make_open_small),
    "jack_mouth_open_medium_r1":   ("open_medium",   make_open_medium),
    "jack_mouth_oo_r1":            ("oo",            make_oo),
    "jack_mouth_ee_r1":            ("ee",            make_ee),
    "jack_mouth_fv_r1":            ("fv",            make_fv),
    "jack_mouth_mbp_r1":           ("mbp",           make_mbp),
}

results = {}
for name, (label, fn) in VISEMES.items():
    print(f"Building {label}…")
    raw = fn()
    final = downsample(raw)
    p = save(final, name)
    arr = np.array(final)
    a = arr[..., 3]
    total = a.size
    opaque = int((a == 255).sum())
    transp = int((a == 0).sum())
    semi = total - opaque - transp
    bbox = final.getbbox()
    # Centroid of opaque pixels
    if (a > 50).any():
        ys, xs = np.where(a > 50)
        cy, cx = float(ys.mean()), float(xs.mean())
    else:
        cy = cx = None
    results[name] = {
        "label": label,
        "file":  p.name,
        "size":  [final.width, final.height],
        "alpha_bbox": list(bbox) if bbox else None,
        "centroid": [round(cx, 1) if cx else None, round(cy, 1) if cy else None],
        "opaque_pct": round(100*opaque/total, 3),
        "transparent_pct": round(100*transp/total, 3),
        "semi_alpha_pct": round(100*semi/total, 3),
    }
    print(f"  -> {p.name}  bbox={bbox}  centroid=({cx:.0f},{cy:.0f})  opaque={results[name]['opaque_pct']}%")

print("\nAll visemes built.")
# Persist a partial manifest; the QC script will extend.
(OUT / "_build_results.json").write_text(json.dumps(results, indent=2))
print("DONE")
