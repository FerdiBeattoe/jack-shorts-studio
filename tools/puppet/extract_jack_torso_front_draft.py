from pathlib import Path
from PIL import Image, ImageDraw

PROJECT = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
OUTPUT_DIR = PROJECT / r"assets\puppet\layers_staging\body_r1"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_ASSET = OUTPUT_DIR / "jack_torso_front_draft.png"
OUT_QC    = OUTPUT_DIR / "jack_torso_front_draft_qc.png"

matches = list(PROJECT.rglob("jack_character_sheet_master.png"))
if not matches:
    raise FileNotFoundError("Could not find jack_character_sheet_master.png under project folder.")

src_path = matches[0]
img = Image.open(src_path).convert("RGBA")
w, h = img.size


def sx(x):
    return int(x / 1536 * w)


def sy(y):
    return int(y / 864 * h)


# Crop window: 5-unit headroom above polygon top; 5-unit margin below belt.
# ry=190→225px (actual), ry=437→517px (actual) — excludes chin fur and trousers.
crop_box = (
    sx(82),
    sy(190),
    sx(315),
    sy(437),
)

crop = img.crop(crop_box)
cw, ch = crop.size

# Polygon coordinates derived from pixel sampling of the character sheet:
#
#   Left jacket shoulder edge:  x≈135 at ry=195, x≈100 at ry=221
#   Right jacket shoulder edge: x≈270 at ry=195, x≈292 at ry=222
#   Belt level:                 ry≈429–431 (belt-buckle transition observed)
#
# The previous V-neck shape (neck 75px → shoulders 188px over 54 ry units)
# created a cape-like flare.  This polygon starts at actual jacket-fabric
# level and expands over only 27 ry units, matching the true shoulder slope.
polygon_abs = [
    (sx(133), sy(195)),   # left jacket shoulder top (jacket fabric starts here)
    (sx(270), sy(195)),   # right jacket shoulder top
    (sx(292), sy(222)),   # right shoulder — jacket body reaches full width
    (sx(291), sy(355)),   # right jacket side
    (sx(268), sy(430)),   # right waist / belt cut-off
    (sx(127), sy(430)),   # left waist / belt cut-off
    (sx(100), sy(355)),   # left jacket side
    (sx(100), sy(222)),   # left shoulder — jacket body reaches full width
]

polygon = [(x - crop_box[0], y - crop_box[1]) for x, y in polygon_abs]

mask = Image.new("L", (cw, ch), 0)
ImageDraw.Draw(mask).polygon(polygon, fill=255)

asset = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
asset.paste(crop, (0, 0), mask)

asset.save(OUT_ASSET)

qc = Image.new("RGBA", asset.size, (180, 180, 180, 255))
qc.alpha_composite(asset)
qc.save(OUT_QC)

print("DONE")
print(f"Source:           {src_path}")
print(f"Transparent PNG:  {OUT_ASSET}")
print(f"QC preview:       {OUT_QC}")
print(f"Crop size:        {cw}x{ch}")
print(f"Mode:             {asset.mode}  |  has alpha: {asset.mode == 'RGBA'}")
