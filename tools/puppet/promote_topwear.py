"""One-shot promotion of topwear_r1 → production. Byte-copy + manifest."""
import json, hashlib, shutil
from pathlib import Path

P = Path(r"C:\Users\ferdi\Desktop\jack-shorts-studio")
STAG = P / r"assets\puppet\layers_staging\topwear_r1"
DEST = P / r"assets\puppet\layers\topwear"
DEST.mkdir(parents=True, exist_ok=True)

NAMES = {
    "jack_jacket_r1.png":    "jack_jacket.png",
    "jack_shirt_tie_r1.png": "jack_shirt_tie.png",
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

replaced = {}
for s, d in NAMES.items():
    dst = DEST / d
    if dst.exists():
        replaced[d] = {"size_bytes": dst.stat().st_size, "sha256": sha(dst)}
        print(f"WILL REPLACE: {d}  size={dst.stat().st_size}  sha={replaced[d]['sha256'][:16]}...")
    else:
        print(f"NEW (no prior): {d}")

files_written = {}
for s, d in NAMES.items():
    src = STAG / s; dst = DEST / d
    shutil.copyfile(src, dst)
    sshs = sha(src); dshs = sha(dst)
    assert sshs == dshs, f"sha mismatch {d}"
    files_written[d] = {
        "source_staging": f"../../layers_staging/topwear_r1/{s}",
        "size_bytes": dst.stat().st_size,
        "sha256": dshs,
        "byte_identical_to_staging_r1": True,
    }
    print(f"  {d:<22} bytes={dst.stat().st_size}  sha={dshs[:16]}...  OK")

stag = json.loads((STAG / "topwear_r1_manifest.json").read_text())
ss  = stag["sources"]
anc = stag["anchor_derivation"]
fc  = stag["full_canvas_test"]

manifest = {
    "category": "topwear",
    "promoted_at": "2026-05-19",
    "promotion_status": "PRODUCTION",
    "approval": {
        "approved_via": "topwear_r1 visual/composite QC + sleeve_strategy_qc Option B",
        "topwear_qc_visual":    "../../layers_staging/topwear_r1/jack_topwear_r1_visual_qc.png",
        "topwear_qc_composite": "../../layers_staging/topwear_r1/jack_topwear_r1_composite_qc.png",
        "topwear_qc_notes":     "../../layers_staging/topwear_r1/topwear_r1_notes.md",
        "topwear_qc_manifest":  "../../layers_staging/topwear_r1/topwear_r1_manifest.json",
        "sleeve_qc_full_body":  "../../layers_staging/topwear_r1/sleeve_strategy_qc/jack_topwear_sleeve_strategy_qc.png",
        "sleeve_qc_zoom":       "../../layers_staging/topwear_r1/sleeve_strategy_qc/jack_topwear_sleeve_strategy_zoom_qc.png",
        "sleeve_qc_notes":      "../../layers_staging/topwear_r1/sleeve_strategy_qc/sleeve_strategy_notes.md",
        "sleeve_qc_manifest":   "../../layers_staging/topwear_r1/sleeve_strategy_qc/sleeve_strategy_manifest.json",
        "summary": "CoPainter topwear split passed staging QC and beats See-through merged on rig addressability (separable jacket + shirt/tie). Sleeve strategy QC chose Option B - keep See-through handwear unmodified in future composites for shoulder/arm bulk, no Krita cleanup, no mask logic. Max-254 alpha quirk reviewed and accepted visually.",
    },
    "sources": {
        "copainter_zip": "../../cloud_layer_tests/copainter/layers_1779216312185.zip",
        "jacket": {
            "copainter_zip_layer": "../../cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_71.png",
            "maps_to": "jacket",
            "native_size": ss["jack_jacket_r1.png"]["size"],
            "source_sha256": ss["jack_jacket_r1.png"]["sha256"],
            "max_alpha_observed": ss["jack_jacket_r1.png"]["max_alpha"],
        },
        "shirt_tie": {
            "copainter_zip_layer": "../../cloud_layer_tests/copainter/extracted_layers_1779216312185/layer_75.png",
            "maps_to": "shirt + tie",
            "native_size": ss["jack_shirt_tie_r1.png"]["size"],
            "source_sha256": ss["jack_shirt_tie_r1.png"]["sha256"],
            "max_alpha_observed": ss["jack_shirt_tie_r1.png"]["max_alpha"],
        },
        "donor_status": "DONOR_ONLY - extracted from CoPainter ZIP; full ZIP set is not the master design",
        "staging_script":   "../../../../tools/puppet/stage_topwear_r1.py",
        "sleeve_qc_script": "../../../../tools/puppet/qc_topwear_sleeve_strategy.py",
    },
    "asset_format": {
        "type": "bbox-cropped transparent PNG",
        "mode": "RGBA",
        "no_background": True,
        "max_alpha_note": "CoPainter never produces alpha=255 across the ZIP; max observed is 254. Pixel content preserved as-is (no thresholding or recolour). Visually clean in composite - no halo or fringe at edges.",
    },
    "copainter_origin_metadata": {
        "present": False,
        "note": "CoPainter ZIP ships loose bbox-cropped PNGs with no per-layer origin/offset. Anchors below were derived manually using See-through topwear bbox geometry.",
    },
    "placement_on_seethrough_canvas": {
        "reference_canvas": anc["reference_canvas"],
        "canvas_size": [768, 768],
        "see_through_topwear_bbox": anc["see_through_topwear_bbox"],
        "scale_factor_copainter_to_seethrough": anc["scale_factor_copainter_to_seethrough"],
        "scale_basis": anc["scale_basis"],
        "jacket_topleft_on_canvas": fc["jacket_topleft_on_canvas"],
        "jacket_scaled_size_on_canvas": fc["jacket_size_on_canvas"],
        "shirt_tie_topleft_on_canvas": fc["shirt_tie_topleft_on_canvas"],
        "shirt_tie_scaled_size_on_canvas": fc["shirt_tie_size_on_canvas"],
        "shirt_tie_offset_below_jacket_top_px": anc["shirt_tie_offset_below_jacket_top_px"],
        "draw_order_back_to_front": ["jack_shirt_tie.png", "jack_jacket.png"],
    },
    "sleeve_strategy_option_b": {
        "decision_source": "sleeve_strategy_qc",
        "recommendation": "Keep See-through handwear UNMODIFIED in future composites for shoulder/arm bulk under the CoPainter jacket.",
        "do_not_clip_or_mask_seethrough_handwear": True,
        "do_not_use_copainter_arms": True,
        "krita_cleanup_required": False,
        "why": "When promoted hands are present at the cuff anchors, the lateral handwear pixels that extend past the jacket silhouette read visually as proper shoulder/arm volume - not as overhang strips. The 8303-px raw overhang metric is overridden by visual QC.",
    },
    "files": files_written,
    "replaced_previous_assets": replaced,
    "do_not": [
        "modify pixel content (each PNG is byte-identical to its staging r1 source, sha256 verified)",
        "promote CoPainter arms (layer_76 / layer_78 - extended-pose, not Jack at-side)",
        "promote eyes/blinks from CoPainter (eyes_blink_r1 rejected for production blink/closed use)",
        "rename or recolour these assets without a fresh QC pass",
        "apply alpha thresholding to force max=255 - keep CoPainter native semi-alpha edges",
        "change the draw order - shirt/tie BEHIND jacket",
        "mask or clip See-through handwear in future composites (Option B was chosen explicitly)",
        "start PSD assembly from this manifest",
        "delete project-root ZIP duplicates",
    ],
}

(DEST / "manifest.json").write_text(json.dumps(manifest, indent=2))
print()
print(f"Manifest written: {DEST / 'manifest.json'}")
