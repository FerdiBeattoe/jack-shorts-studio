"""
Mouth r2 — smaller, subtler, line-first visemes.

Lessons from r1 rejection:
  - r1 was too big (270-290 px wide) and visually pasted rather than drawn.
  - r1 used big maroon fills and visible teeth — out of character for Jack.
  - r1 used pure black (20,20,20); Jack's actual face lineart is warm dark brown.

r2 changes:
  - Mouths are smaller: ~140-180 px wide in the 512 canvas.
  - Linework only by default. Open mouths may have a faint dark hint inside
    the line, never a saturated fill.
  - Lineart colour = RGB(40, 35, 28) sampled from production head face outline.
  - No teeth at all. EE/FV are represented by line-shape approximations only.
  - No tongue. No cream-cream colour. No tooth dividers.

Outputs (assets/puppet/layers_staging/mouth_r2/):
  jack_mouth_neutral_r2.png
  jack_mouth_slight_frown_r2.png
  jack_mouth_slight_smirk_r2.png
  jack_mouth_open_small_r2.png
  jack_mouth_open_medium_r2.png
  jack_mouth_oo_r2.png
  jack_mouth_ee_r2.png
  jack_mouth_fv_r2.png
  jack_mouth_mbp_r2.png
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUT = PROJECT / r"assets\puppet\layers_staging\mouth_r2"
OUT.mkdir(parents=True, exist_ok=True)

W = H = 512
ANCHOR = (256, 270)
SS = 4
WW, HH = W * SS, H * SS
AX, AY = ANCHOR[0] * SS, ANCHOR[1] * SS

# Style constants — chosen to match Jack's actual face palette
LINE = (40, 35, 28, 255)        # warm dark brown, sampled from head outline
FAINT_FILL = (40, 35, 28, 90)   # same hue, semi-transparent (used sparingly inside open mouths only)
LINE_W_REL = 4                  # final-res line weight (down from r1's 5)
LINE_W = LINE_W_REL * SS

def new_canvas(): return Image.new("RGBA", (WW, HH), (0, 0, 0, 0))
def downsample(img): return img.resize((W, H), Image.LANCZOS)
def L(x, y): return (AX + x*SS, AY + y*SS)

def cubic(p0, p1, p2, p3, steps=80):
    ts = np.linspace(0, 1, steps)
    xs = (1-ts)**3*p0[0] + 3*(1-ts)**2*ts*p1[0] + 3*(1-ts)*ts**2*p2[0] + ts**3*p3[0]
    ys = (1-ts)**3*p0[1] + 3*(1-ts)**2*ts*p1[1] + 3*(1-ts)*ts**2*p2[1] + ts**3*p3[1]
    return list(zip(xs.tolist(), ys.tolist()))

def stroke(d, pts, color=LINE, width=LINE_W):
    d.line(pts, fill=color, width=width, joint="curve")
    r = width // 2
    for p in (pts[0], pts[-1]):
        d.ellipse((p[0]-r, p[1]-r, p[0]+r, p[1]+r), fill=color)

def save(img, name): img.save(OUT / f"{name}.png"); return OUT / f"{name}.png"

# ─── 1. neutral ─────────────────────────────────────────────────────────────
# Short shallow curve, slight downward droop at corners. Width ~140 px.
def make_neutral():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    pts = cubic(L(-70, -2), L(-25, 12), L(25, 12), L(70, -2), steps=80)
    stroke(d, pts)
    return img

# ─── 2. slight_frown ────────────────────────────────────────────────────────
# Same width, deeper droop. Subtle, not exaggerated.
def make_slight_frown():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    pts = cubic(L(-72, -12), L(-25, 18), L(25, 18), L(72, -12), steps=80)
    stroke(d, pts)
    return img

# ─── 3. slight_smirk ────────────────────────────────────────────────────────
# Asymmetric: left flat-ish, right corner lifts slightly. Width ~155 px.
def make_slight_smirk():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    # Left half: very subtle dip
    left  = cubic(L(-78, -2), L(-40, 8), L(-15, 6), L(10, 2), steps=60)
    # Right half: lifts up
    right = cubic(L(10, 2), L(35, -6), L(60, -14), L(80, -18), steps=60)
    stroke(d, left)
    stroke(d, right)
    return img

# ─── 4. open_small ─────────────────────────────────────────────────────────
# Tight horizontal oval, line only with a very faint inner shadow. Width ~50.
def make_open_small():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    rx, ry = 24, 7
    # Faint hint of darkness inside (semi-transparent same brown)
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=FAINT_FILL)
    # Line outline
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    return img

# ─── 5. open_medium ────────────────────────────────────────────────────────
# Slightly larger oval, still subtle.
def make_open_medium():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    rx, ry = 38, 12
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=FAINT_FILL)
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    return img

# ─── 6. oo ─────────────────────────────────────────────────────────────────
# Small round circle outline.
def make_oo():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    rx, ry = 14, 12
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), fill=FAINT_FILL)
    d.ellipse((AX - rx*SS, AY - ry*SS, AX + rx*SS, AY + ry*SS), outline=LINE, width=LINE_W)
    return img

# ─── 7. ee ─────────────────────────────────────────────────────────────────
# Two parallel horizontal lines (lip line + faint line below). NO teeth.
def make_ee():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    half_w = 70
    upper = cubic(L(-half_w, -4), L(-20, -3), L(20, -3), L(half_w, -4), steps=60)
    lower = cubic(L(-half_w+4, 6), L(-20, 8), L(20, 8), L(half_w-4, 6), steps=60)
    stroke(d, upper)
    stroke(d, lower, width=max(1, LINE_W - SS))  # slightly thinner secondary line
    return img

# ─── 8. fv ─────────────────────────────────────────────────────────────────
# Single lip line with a faint upper inflection (suggesting upper-teeth-on-lip)
# but no actual teeth shapes.
def make_fv():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    half_w = 65
    # Lower lip — slightly higher than neutral
    lip = cubic(L(-half_w, 4), L(-25, 10), L(25, 10), L(half_w, 4), steps=60)
    stroke(d, lip)
    # Tiny inflection line above the lip (just a hint, very thin and short)
    inf = cubic(L(-30, -4), L(-10, -2), L(10, -2), L(30, -4), steps=40)
    stroke(d, inf, width=max(1, LINE_W - 2*SS))
    return img

# ─── 9. mbp ────────────────────────────────────────────────────────────────
# Tight short flat line, slightly thicker — pressed lips.
def make_mbp():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    pts = cubic(L(-50, 0), L(-15, 2), L(15, 2), L(50, 0), steps=60)
    stroke(d, pts, width=LINE_W + SS)
    return img

VISEMES = {
    "jack_mouth_neutral_r2":       ("neutral",       make_neutral),
    "jack_mouth_slight_frown_r2":  ("slight_frown",  make_slight_frown),
    "jack_mouth_slight_smirk_r2":  ("slight_smirk",  make_slight_smirk),
    "jack_mouth_open_small_r2":    ("open_small",    make_open_small),
    "jack_mouth_open_medium_r2":   ("open_medium",   make_open_medium),
    "jack_mouth_oo_r2":            ("oo",            make_oo),
    "jack_mouth_ee_r2":            ("ee",            make_ee),
    "jack_mouth_fv_r2":            ("fv",            make_fv),
    "jack_mouth_mbp_r2":           ("mbp",           make_mbp),
}

results = {}
for name, (label, fn) in VISEMES.items():
    img = downsample(fn())
    p = save(img, name)
    arr = np.array(img)
    a = arr[..., 3]
    total = a.size
    opaque = int((a == 255).sum())
    transp = int((a == 0).sum())
    bbox = img.getbbox()
    if (a > 50).any():
        ys, xs = np.where(a > 50)
        cy, cx = float(ys.mean()), float(xs.mean())
        bbox_w = bbox[2] - bbox[0] if bbox else 0
        bbox_h = bbox[3] - bbox[1] if bbox else 0
    else:
        cx = cy = None
        bbox_w = bbox_h = 0
    results[name] = {
        "label": label,
        "size":  [img.width, img.height],
        "alpha_bbox": list(bbox) if bbox else None,
        "bbox_wh": [bbox_w, bbox_h],
        "centroid": [round(cx, 1) if cx else None, round(cy, 1) if cy else None],
        "opaque_pct": round(100*opaque/total, 3),
        "transparent_pct": round(100*transp/total, 3),
        "semi_alpha_pct": round(100*(total-opaque-transp)/total, 3),
    }
    print(f"{label:<14} bbox={bbox} wh=({bbox_w}x{bbox_h}) centroid=({cx:.0f},{cy:.0f}) opaque={results[name]['opaque_pct']}%")

(OUT / "_build_results.json").write_text(json.dumps(results, indent=2))
print("DONE")
