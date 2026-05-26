#!/usr/bin/env node
/**
 * build-jack-character-animator-psd-v1.mjs
 *
 * Builds assets/puppet/jack_character_animator_v1.psd from the validated V1
 * puppet layer PNGs, with first-pass deterministic layer positioning.
 * Also writes a flat PNG layout preview for quick visual QC.
 *
 * Prerequisites:
 *   pnpm install   (installs ag-psd + @napi-rs/canvas)
 *   node scripts/validate-jack-puppet-pack.mjs
 *
 * Usage:
 *   node scripts/build-jack-character-animator-psd-v1.mjs
 *
 * Outputs:
 *   assets/puppet/jack_character_animator_v1.psd
 *   assets/puppet/jack_character_animator_v1_layout_preview.png
 *
 * See docs/animation/psd_assembly_runbook_v1.md for next steps.
 */

import { initializeCanvas, writePsd } from "ag-psd";
import { createCanvas, loadImage } from "@napi-rs/canvas";
import { existsSync, writeFileSync, mkdirSync, readFileSync, statSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

// ── Bootstrap ag-psd with @napi-rs/canvas ────────────────────────────────
initializeCanvas(
  createCanvas,
  (w, h) => createCanvas(w, h).getContext("2d").createImageData(w, h)
);

// ── Paths ─────────────────────────────────────────────────────────────────
const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT      = resolve(__dirname, "..");
const a         = (rel) => resolve(ROOT, rel);

const CANVAS_W       = 1920;
const CANVAS_H       = 1920;
const OUTPUT_PSD     = a("assets/puppet/jack_character_animator_v1.psd");
const OUTPUT_PREVIEW = a("assets/puppet/jack_character_animator_v1_layout_preview.png");
const MANIFEST_PATH  = a("manifests/jack_puppet_manifest_v1.json");

// ── LAYOUT MAP ────────────────────────────────────────────────────────────
// Each value is [left, top] in pixels on the 1920×1920 canvas.
// These are first-pass positions — correct structure, not final rigging.
//
// Asset dimensions (measured):
//   head/        1024 × 1024
//   eyes/         512 ×  512
//   eyebrows/    1254 × 1254
//   mouth/        512 ×  512
//   body/        1024 × 1024
//   office_bg    1920 × 1080  (landscape — centred vertically)
//   chair        1200 × 1200
//
// Key reference points:
//   Character centre X  : 960   (canvas_w / 2)
//   Head top-left       : (448, 150)  → head centre (960, 662)
//   Torso top-left      : (448, 750)  → torso centre (960, 1262)
//   Eye level (canvas)  : y ≈ 530
//   Mouth level (canvas): y ≈ 750

const LAYOUT = {
  // ── Environment (bottommost — behind everything) ──────────────────────
  // office_bg is 1920×1080 (landscape). Place centred vertically so
  // the background fills the middle band of the 1920×1920 canvas.
  officeBg : [0,    420],  // (1920-1080)/2 = 420 → y:[420-1500]

  // Chair centred horizontally, sits behind the body group.
  chair    : [360,  680],  // (1920-1200)/2 = 360 → x:[360-1560], y:[680-1880]

  // ── Body (lower centre) ───────────────────────────────────────────────
  // All body layers are 1024×1024. Centre at x=960 → left=448.
  torso    : [448,  750],  // x:[448-1472], y:[750-1774]
  tie      : [448,  750],  // sits on top of torso, same canvas origin

  // Arms flank the torso. Left arm starts at canvas left edge (x=0),
  // right arm ends at canvas right edge (x=1920; 896+1024=1920).
  armLeft  : [0,    750],  // x:[0-1024],   y:[750-1774]
  armRight : [896,  750],  // x:[896-1920], y:[750-1774]
  armRTie  : [896,  750],  // tie-fix arm occupies same area as resting arm

  // ── Head (upper centre) ───────────────────────────────────────────────
  // 1024×1024, centred at x=960 → left=448. Head bottom: y=150+1024=1174.
  // Neck overlap with torso (750-1174): ~424px — intentional for body join.
  headBase : [448,  150],  // head centre (960, 662)

  // ── Face elements (positioned within the head zone) ───────────────────
  // All face assets assume head centre (960, 662) as origin reference.
  //
  // Eyes: 512×512. Eye level at y≈530 (380px into the head image).
  //   Left eye  = Jack's anatomical LEFT = viewer's RIGHT = x > 960.
  //   Right eye = Jack's anatomical RIGHT = viewer's LEFT = x < 960.
  //   Offset ±120px from centre → eye centres at (1080, 530) and (840, 530).
  eyeLeft  : [824,  274],  // centre (1080, 530);  left=1080-256, top=530-256
  eyeRight : [584,  274],  // centre (840,  530);  left=840-256,  top=530-256

  // Pupils: 512×512. Sit exactly over the open-eye layers.
  pupilLeft  : [824, 274],
  pupilRight : [584, 274],

  // Eyebrows: 1254×1254 — full-face-context images larger than the head.
  // Both LB and RB images share the same canvas origin (each contains one brow).
  // Centre the 1254×1254 image on the head centre (960, 662):
  //   left=960-627=333,  top=662-627=35
  // Brow element in image sits above the eye level → appears at ≈ y:300-500.
  browLeft  : [333,  35],
  browRight : [333,  35],

  // Mouth: 512×512. Centred at (960, 750) — muzzle region below eyes.
  //   left=960-256=704,  top=750-256=494
  mouth     : [704, 494],
};

// ── Helpers ───────────────────────────────────────────────────────────────

/** Load a PNG into a canvas. Returns null if the file is missing or fails. */
async function loadLayer(relPath) {
  const full = a(relPath);
  if (!existsSync(full)) return null;
  try {
    const img    = await loadImage(full);
    const canvas = createCanvas(img.width, img.height);
    canvas.getContext("2d").drawImage(img, 0, 0);
    return canvas;
  } catch (err) {
    console.warn(`  ⚠  Could not load ${relPath}: ${err.message}`);
    return null;
  }
}

/**
 * Build a PSD leaf layer.
 * pos is a [left, top] tuple from LAYOUT (defaults to [0,0] for structural groups
 * where position is irrelevant, such as swap-set hidden variants — they share the
 * same position as their visible default anyway).
 */
function lyr(name, canvas, hidden = false, pos = [0, 0]) {
  const [left, top] = pos;
  const layer = { name, hidden, left, top };
  if (canvas) layer.canvas = canvas;
  return layer;
}

/** Build a PSD layer group. */
function grp(name, children, hidden = false) {
  return { name, children, hidden };
}

// ── Main ──────────────────────────────────────────────────────────────────
async function main() {
  console.log("\nJack Character Animator PSD Builder v1  (with layout pass)");
  console.log("─".repeat(58));

  // 1. Pre-flight ──────────────────────────────────────────────────────────
  let manifest;
  try {
    manifest = JSON.parse(readFileSync(MANIFEST_PATH, "utf-8"));
  } catch (err) {
    console.error(`✗  Cannot read manifest: ${err.message}`);
    process.exit(1);
  }

  const v1Required = manifest.assets.filter((a) => a.required_for_v1);
  const missing    = v1Required.filter((a) => !existsSync(resolve(ROOT, a.required_file_path)));

  if (missing.length > 0) {
    console.error(`\n✗  PREFLIGHT FAILED — ${missing.length} V1-required PNG(s) missing:`);
    missing.forEach((a) => console.error(`     ${a.required_file_path}`));
    console.error("\n   Run: node scripts/validate-jack-puppet-pack.mjs");
    process.exit(1);
  }
  console.log(`✓  Pre-flight: all ${v1Required.length} V1-required assets present`);

  // 2. Load all PNG layers in parallel ─────────────────────────────────────
  console.log("   Loading PNG layers...");

  const [
    officeBg, chair,
    torso, tie, armLeft, armRRight, armRTie,
    headBase,
    mNeutral, mSmile, mSmirk, mOpen, mEe, mOh, mOoh, mMbp, mFv, mLl, mS,
    eyeLeftOpen, eyeLeftHalf, eyeLeftClosed, pupilLeft,
    eyeRightOpen, eyeRightHalf, eyeRightClosed, pupilRight,
    lbNeutral, lbConcerned, lbThinking, lbSmug,
    rbNeutral, rbConcerned, rbThinking, rbSmug,
  ] = await Promise.all([
    loadLayer("assets/puppet/layers/environment/office_background_clean.png"),
    loadLayer("assets/puppet/layers/environment/office_chair.png"),
    loadLayer("assets/puppet/layers/body/jack_torso_front.png"),
    loadLayer("assets/puppet/layers/body/jack_tie_straight.png"),
    loadLayer("assets/puppet/layers/body/jack_arm_left_resting.png"),
    loadLayer("assets/puppet/layers/body/jack_arm_right_resting.png"),
    loadLayer("assets/puppet/layers/body/jack_arm_right_tie_fix.png"),
    loadLayer("assets/puppet/layers/head/jack_head_front_base.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_neutral.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_smile.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_smirk.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_ah.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_ee.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_oh.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_oo_w.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_mbp.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_fv.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_l.png"),
    loadLayer("assets/puppet/layers/mouth/jack_mouth_s_dtn.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_left_open.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_left_half.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_left_closed.png"),
    loadLayer("assets/puppet/layers/eyes/jack_pupil_left.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_right_open.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_right_half.png"),
    loadLayer("assets/puppet/layers/eyes/jack_eye_right_closed.png"),
    loadLayer("assets/puppet/layers/eyes/jack_pupil_right.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_left_neutral.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_left_concerned.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_left_thinking.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_left_smug.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_right_neutral.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_right_concerned.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_right_thinking.png"),
    loadLayer("assets/puppet/layers/eyebrows/jack_eyebrow_right_smug.png"),
  ]);

  const all   = [officeBg,chair,torso,tie,armLeft,armRRight,armRTie,headBase,
                  mNeutral,mSmile,mSmirk,mOpen,mEe,mOh,mOoh,mMbp,mFv,mLl,mS,
                  eyeLeftOpen,eyeLeftHalf,eyeLeftClosed,pupilLeft,
                  eyeRightOpen,eyeRightHalf,eyeRightClosed,pupilRight,
                  lbNeutral,lbConcerned,lbThinking,lbSmug,
                  rbNeutral,rbConcerned,rbThinking,rbSmug];
  const loadedCount = all.filter(Boolean).length;
  console.log(`✓  Loaded ${loadedCount} / ${all.length} PNG layers`);

  // 3. Build PSD layer tree with layout positions ───────────────────────────
  //
  // Layer stack: children[0] = topmost in Photoshop panel (rendered in front)
  //
  // All swap-set inactive members share their group's default position.
  // Character Animator names are case-sensitive — do not change them.
  //   "Left/Right" = from the CHARACTER's perspective (not the viewer's).

  const psd = {
    width:          CANVAS_W,
    height:         CANVAS_H,
    bitsPerChannel: 8,
    children: [

      // ── Jack puppet root ───────────────────────────────────────────────
      grp("Jack", [

        // Head sits above Body in the layer panel (rendered in front of Body)
        grp("Head", [

          grp("Face", [

            // ── Mouth (CA Auto Mouth lip sync) ──────────────────────────
            // Sublayer names are the exact phoneme strings CA maps.
            // "Neutral" is the default visible rest position.
            // "Smirk" is trigger-only — NOT used by Auto Mouth.
            // All mouth layers share the same canvas position.
            grp("Mouth", [
              lyr("Neutral", mNeutral, false, LAYOUT.mouth),
              lyr("Smile",   mSmile,   true,  LAYOUT.mouth),
              lyr("Smirk",   mSmirk,   true,  LAYOUT.mouth),
              lyr("Open",    mOpen,    true,  LAYOUT.mouth),
              lyr("Ee",      mEe,      true,  LAYOUT.mouth),
              lyr("Oh",      mOh,      true,  LAYOUT.mouth),
              lyr("Ooh",     mOoh,     true,  LAYOUT.mouth),
              lyr("M B P",   mMbp,     true,  LAYOUT.mouth),
              lyr("F V",     mFv,      true,  LAYOUT.mouth),
              lyr("L",       mLl,      true,  LAYOUT.mouth),
              lyr("S",       mS,       true,  LAYOUT.mouth),
            ]),

            // ── Left Eye (Jack's left = viewer's right, x > 960) ────────
            // Left Upper Lid: CA uses this group for blink warp.
            // Left Lower Lid: empty group, CA's second blink warp handle.
            grp("Left Eye", [
              grp("Left Upper Lid", [
                lyr("Left Eye Open",   eyeLeftOpen,   false, LAYOUT.eyeLeft),
              ]),
              grp("Left Lower Lid", []),
              lyr("Left Eye Half",   eyeLeftHalf,   true,  LAYOUT.eyeLeft),
              lyr("Left Eye Closed", eyeLeftClosed, true,  LAYOUT.eyeLeft),
              lyr("Left Pupil",      pupilLeft,     false, LAYOUT.pupilLeft),
            ]),

            // ── Right Eye (Jack's right = viewer's left, x < 960) ───────
            grp("Right Eye", [
              grp("Right Upper Lid", [
                lyr("Right Eye Open",   eyeRightOpen,   false, LAYOUT.eyeRight),
              ]),
              grp("Right Lower Lid", []),
              lyr("Right Eye Half",   eyeRightHalf,   true,  LAYOUT.eyeRight),
              lyr("Right Eye Closed", eyeRightClosed, true,  LAYOUT.eyeRight),
              lyr("Right Pupil",      pupilRight,     false, LAYOUT.pupilRight),
            ]),

            // ── Left Eyebrow swap set ─────────────────────────────────────
            // LB Neutral is the only visible default.
            // Remaining states are swapped via CA trigger keys.
            grp("Left Eyebrow", [
              lyr("LB Neutral",   lbNeutral,   false, LAYOUT.browLeft),
              lyr("LB Concerned", lbConcerned, true,  LAYOUT.browLeft),
              lyr("LB Thinking",  lbThinking,  true,  LAYOUT.browLeft),
              lyr("LB Smug",      lbSmug,      true,  LAYOUT.browLeft),
            ]),

            // ── Right Eyebrow swap set ─────────────────────────────────────
            grp("Right Eyebrow", [
              lyr("RB Neutral",   rbNeutral,   false, LAYOUT.browRight),
              lyr("RB Concerned", rbConcerned, true,  LAYOUT.browRight),
              lyr("RB Thinking",  rbThinking,  true,  LAYOUT.browRight),
              lyr("RB Smug",      rbSmug,      true,  LAYOUT.browRight),
            ]),

          ]), // end Face

          // Head Base sits at the bottom of the Head group (behind Face)
          lyr("Head Base", headBase, false, LAYOUT.headBase),

        ]), // end Head

        // ── Body (below Head in layer panel) ──────────────────────────────
        grp("Body", [

          // Right Arm: Arm Resting is default visible; Arm Tie Fix is hidden.
          // Both share the same canvas area — swap activated by CA trigger.
          grp("Right Arm", [
            grp("Arm Resting", [
              lyr("Right Arm Resting", armRRight, false, LAYOUT.armRight),
            ]),
            grp("Arm Tie Fix", [
              lyr("Right Arm Raised",  armRTie,   false, LAYOUT.armRTie),
            ], true), // hidden group — CA trigger activates this swap
          ]),

          grp("Left Arm", [
            lyr("Left Arm Resting", armLeft, false, LAYOUT.armLeft),
          ]),

          // Tie is a separate group so CA can apply independent physics
          grp("Tie", [
            lyr("Tie Straight", tie, false, LAYOUT.tie),
          ]),

          // Torso is at the bottom of Body (renders behind arms and tie)
          lyr("Torso", torso, false, LAYOUT.torso),

        ]), // end Body

      ]), // end Jack

      // ── Environment (SEPARATE top-level group — NOT inside Jack) ──────────
      // Must be outside the puppet root so CA does not treat background
      // layers as animated puppet parts.
      grp("Environment", [
        lyr("Chair",             chair,    false, LAYOUT.chair),
        lyr("Office Background", officeBg, false, LAYOUT.officeBg),
      ]),

    ], // end root children
  };

  // 4. Write PSD ────────────────────────────────────────────────────────────
  console.log("   Assembling PSD...");
  const psdDir = resolve(OUTPUT_PSD, "..");
  if (!existsSync(psdDir)) mkdirSync(psdDir, { recursive: true });

  const psdBuffer = writePsd(psd);
  writeFileSync(OUTPUT_PSD, Buffer.from(psdBuffer));

  const psdMB = (statSync(OUTPUT_PSD).size / (1024 * 1024)).toFixed(2);
  console.log(`✓  PSD: assets/puppet/jack_character_animator_v1.psd  (${psdMB} MB)`);

  // 5. Generate flat layout preview PNG ─────────────────────────────────────
  // Composites only the DEFAULT VISIBLE layers onto a dark background canvas
  // so layout positions can be inspected without opening Photopea.
  // Draw order: back → front (environment → body → head → face).
  console.log("   Generating layout preview...");

  const preview = createCanvas(CANVAS_W, CANVAS_H);
  const ctx     = preview.getContext("2d");

  // Dark canvas background makes transparent areas clearly visible
  ctx.fillStyle = "#1a1a2e";
  ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

  // Thin centre guide lines for alignment QC (drawn before layers)
  ctx.strokeStyle = "rgba(255,255,255,0.12)";
  ctx.lineWidth   = 1;
  ctx.beginPath(); ctx.moveTo(960, 0);    ctx.lineTo(960, CANVAS_H); ctx.stroke(); // vertical centre
  ctx.beginPath(); ctx.moveTo(0, 960);    ctx.lineTo(CANVAS_W, 960); ctx.stroke(); // horizontal centre

  // Draw layers back-to-front using only the default-visible layer per group
  const drawLayer = (canvas, pos) => {
    if (canvas && pos) ctx.drawImage(canvas, pos[0], pos[1]);
  };

  drawLayer(officeBg,     LAYOUT.officeBg);    // background fill
  drawLayer(chair,        LAYOUT.chair);        // chair behind body
  drawLayer(torso,        LAYOUT.torso);        // suit body
  drawLayer(tie,          LAYOUT.tie);          // tie over torso
  drawLayer(armLeft,      LAYOUT.armLeft);      // left arm resting
  drawLayer(armRRight,    LAYOUT.armRight);     // right arm resting (not tie-fix)
  drawLayer(headBase,     LAYOUT.headBase);     // head base
  drawLayer(eyeLeftOpen,  LAYOUT.eyeLeft);      // left eye open (default)
  drawLayer(eyeRightOpen, LAYOUT.eyeRight);     // right eye open (default)
  drawLayer(pupilLeft,    LAYOUT.pupilLeft);    // left pupil
  drawLayer(pupilRight,   LAYOUT.pupilRight);   // right pupil
  drawLayer(lbNeutral,    LAYOUT.browLeft);     // left brow neutral (default)
  drawLayer(rbNeutral,    LAYOUT.browRight);    // right brow neutral (default)
  drawLayer(mNeutral,     LAYOUT.mouth);        // mouth neutral (default)

  // Watermark so it's clear this is a layout preview, not production art
  ctx.fillStyle    = "rgba(255,255,255,0.55)";
  ctx.font         = "bold 36px sans-serif";
  ctx.textAlign    = "center";
  ctx.fillText("JACK V1 — LAYOUT PREVIEW (first pass)", 960, 60);
  ctx.font         = "26px sans-serif";
  ctx.fillStyle    = "rgba(255,255,255,0.35)";
  ctx.fillText("All layers at auto-computed positions. Manual rigging still required.", 960, 100);

  const previewBuffer = await preview.encode("png");
  writeFileSync(OUTPUT_PREVIEW, previewBuffer);

  const prevKB = Math.round(statSync(OUTPUT_PREVIEW).size / 1024);
  console.log(`✓  Preview: assets/puppet/jack_character_animator_v1_layout_preview.png  (${prevKB} KB)`);

  // 6. Print layout map summary ─────────────────────────────────────────────
  console.log("\n   Layout map applied:");
  console.log("   Layer                        left    top   (canvas 1920×1920)");
  console.log("   " + "─".repeat(56));
  const rows = [
    ["Office Background",  LAYOUT.officeBg],
    ["Chair",              LAYOUT.chair],
    ["Torso + Tie",        LAYOUT.torso],
    ["Left Arm",           LAYOUT.armLeft],
    ["Right Arm",          LAYOUT.armRight],
    ["Head Base",          LAYOUT.headBase],
    ["Eyes (L/R)",         LAYOUT.eyeLeft],
    ["Pupils (L/R)",       LAYOUT.pupilLeft],
    ["Eyebrows (L/R)",     LAYOUT.browLeft],
    ["Mouth (all)",        LAYOUT.mouth],
  ];
  for (const [label, [l, t]] of rows) {
    console.log(`   ${label.padEnd(30)} ${String(l).padStart(5)}  ${String(t).padStart(5)}`);
  }

  // 7. Summary ──────────────────────────────────────────────────────────────
  console.log("\n" + "─".repeat(58));
  console.log("PSD assembly + layout pass complete.\n");
  console.log("NEXT STEPS:");
  console.log("  1. Open the preview PNG to QC the automated layout:");
  console.log("     assets/puppet/jack_character_animator_v1_layout_preview.png");
  console.log("  2. If positions need correction, edit LAYOUT map in this script");
  console.log("     and re-run to regenerate both PSD and preview.");
  console.log("  3. Open PSD in Photopea (free) for detailed layer inspection:");
  console.log("     https://www.photopea.com  →  File > Open");
  console.log("  4. Fine-tune any positions manually in Photopea, then save.");
  console.log("  5. Import into Adobe Character Animator:");
  console.log("     File > New > Puppet from Photoshop File");
  console.log("     Character > Rigging > Auto-tag puppet");
  console.log("\nFull runbook: docs/animation/psd_assembly_runbook_v1.md");
  console.log("Validate:     node scripts/validate-jack-psd-assembly.mjs");
}

main().catch((err) => {
  console.error("\n✗  BUILD FAILED:", err.message);
  console.error(err.stack);
  process.exit(1);
});
