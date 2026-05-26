# Jack — Cloud Layer Splitter Manual Test Checklist

**Goal:** Evaluate 5 cloud tools for puppet layer extraction. You upload manually; this doc tells you what to upload, where to drop the result, and what to look for.

## Canonical upload input

- **File to upload:** `assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test.png` (white background, 310 × 990, PNG)
- **Backup transparent version:** `assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test_transparent.png` — only use if a tool explicitly wants alpha; rembg's anti-aliasing left ~58% semi-alpha pixels, so the white-bg version is the safer default.
- **QC preview:** `assets/puppet/cloud_layer_tests/inputs/jack_front_clean_test_qc.png`

> If any tool rejects 310 × 990 (some require ≥ 1024 on the short side), upscale 4× in Photoshop / Affinity with Nearest Neighbor (no resampling artifacts) and rename `…_test_upscale.png`. Do NOT regenerate with a different crop.

---

## 1. See-through (HuggingFace Space)

- **URL:** https://huggingface.co/spaces/24yearsold/see-through-demo
- **Mirror (no HF account needed):** https://modelscope.cn/studios/ljsabc/See-Through
- **Upload:** `jack_front_clean_test.png`
- **Settings:** default resolution 1280; let it run ~2-3 min.
- **Download:** the layered `.psd` file (will contain up to 23 inpainted layers: hair, face, eyes, mouth, eyebrows, clothing, accessories, …).
- **Save to:** `assets/puppet/cloud_layer_tests/see_through/jack_front_seethrough.psd`
- **Also save:** any intermediate depth map or mask preview if the demo exposes them, alongside the PSD.
- **Pass criteria:**
  - PSD opens in Photoshop / Krita / Photopea with > 5 named transparent layers.
  - Head, torso, arms, legs are individually addressable.
  - Style is preserved (no re-rendering — this should be a *decomposition*, not a regeneration).
  - Inpainted areas behind layers (e.g. body behind arm) look usable, not garbage noise.
- **Fail signals:** flat single-layer export, "AI-redrawn" look, layers contain artifacts/halos, only background removed.

## 2. KomikoAI Layer Splitter

- **URL:** https://komiko.app/ (look for "Layer Splitter" / "PSD export" feature)
- **Upload:** `jack_front_clean_test.png`
- **Download:** PSD or ZIP of PNG layers (depends on Komiko's export format).
- **Save to:** `assets/puppet/cloud_layer_tests/komiko/jack_front_komiko.psd` (or `.zip` — keep original extension)
- **Pass criteria:**
  - Distinct layers for at least: background, body, head, eyes, mouth.
  - Transparent layer PNGs (not flat composites).
  - Edges follow Jack's linework, not generic body silhouettes.
- **Fail signals:** only foreground/background split, layer names don't match content, redrawn style.

## 3. ImageToLayers.com

- **URL:** https://imagetolayers.com/
- **Upload:** `jack_front_clean_test.png`
- **Download:** PSD (this tool is PSD-only as far as we know).
- **Save to:** `assets/puppet/cloud_layer_tests/imagetolayers/jack_front_i2l.psd`
- **Pass criteria:**
  - Multiple semantic layers (not just object-instance segmentation).
  - Usable for puppet rig — i.e., parts are split where a joint would go (neck, shoulder, elbow, hip).
- **Fail signals:** crude rectangular splits, layers contain visible seams, color shifts between layers.

## 4. Layer.ai — Spine Component Generator

- **URL:** https://layer.ai/ → Spine component / character rig export.
- **Upload:** `jack_front_clean_test.png`
- **Download:** likely a Spine `.json` + atlas `.png` + per-component PNGs (Spine pipeline).
- **Save to:** `assets/puppet/cloud_layer_tests/layer_ai/` — preserve the full export bundle structure (atlas, json, slices/).
- **Pass criteria:**
  - Per-bone slices exported (head, torso, upper arm L/R, lower arm L/R, upper leg L/R, lower leg L/R, hands, feet).
  - Slices are transparent PNGs aligned to a common origin.
  - Style preserved.
- **Fail signals:** generic humanoid rig with no dog-anatomy adjustment, missing tail, missing snout, slices smaller than visible body parts (clipped).

## 5. Stretchy Studio — **conditional, run last**

- **Run only after at least one of #1-#4 produced a layered PSD / Spine bundle.**
- **URL:** https://stretchy.studio/
- **Upload:** the best output PSD / Spine bundle from the previous tests (NOT the raw Jack PNG).
- **Purpose:** test downstream animation rigging on top of a separated layer set — does it accept the layers, auto-rig, produce a usable puppet?
- **Save to:** `assets/puppet/cloud_layer_tests/stretchy/` — entire export bundle.
- **Pass criteria:**
  - Layers are recognised and auto-rigged into a puppet.
  - Animation preview moves head/limbs independently without ghosting.
- **Fail signals:** layers ignored, rig fails to bind, output requires manual rework that exceeds doing it from scratch.

---

## After uploads — drop-in instructions

1. Save every download into the matching folder above. Keep original filenames as a suffix, e.g. `jack_front_seethrough_2026-05-19.psd`.
2. Don't unzip anything yourself — the audit script will do it.
3. Tell Claude "audit the cloud test outputs" and the audit will:
   - List every file found
   - Extract any ZIPs
   - Export PSD layers to per-layer PNGs (via psd-tools)
   - Build a contact sheet per tool: `<tool>/<tool>_contact_sheet.png`
   - Write `reports/jack_cloud_layer_splitter_output_audit.md` with pass/fail per criterion

## Hard rules during testing

- **Don't** drop any output into `assets/puppet/layers/` — that's production.
- **Don't** modify the source PSD or character sheet.
- **Don't** re-upload Jack to text-to-image tools. Only segmentation / decomposition tools.
- **Do** screenshot the tool's UI showing the layer list before you close the tab — useful if the PSD's layer names are stripped.
