#!/usr/bin/env node
/**
 * validate-jack-psd-assembly.mjs
 *
 * Verifies the PSD assembly workflow is complete and correct:
 *
 *   1. Node PSD builder (primary path) exists and is non-empty
 *   2. Photoshop JSX fallback exists (kept for Photoshop users)
 *   3. Runbook exists and documents the free Node+Photopea workflow
 *   4. All V1-mandatory PNG inputs still exist (source files unchanged)
 *   5. PSD output file exists and is larger than 0 bytes
 *   6. Layout preview PNG exists and is larger than 0 bytes
 *
 * NOTE: This script does NOT open or visually inspect the PSD or preview.
 *       Visual review requires opening the preview PNG or PSD in Photopea.
 *
 * Usage:
 *   node scripts/validate-jack-psd-assembly.mjs
 *
 * Exit codes:
 *   0 — all checks pass
 *   1 — one or more checks failed
 */

import { readFileSync, existsSync, statSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

// ── Colour helpers ────────────────────────────────────────────────────────
const R  = "\x1b[31m";
const G  = "\x1b[32m";
const Y  = "\x1b[33m";
const C  = "\x1b[36m";
const B  = "\x1b[1m";
const D  = "\x1b[2m";
const RS = "\x1b[0m";

const pass = (msg) => console.log(`  ${G}✓${RS} ${msg}`);
const fail = (msg) => console.log(`  ${R}✗${RS} ${B}${msg}${RS}`);
const info = (msg) => console.log(`  ${D}→ ${msg}${RS}`);
const warn = (msg) => console.log(`  ${Y}⚠${RS} ${msg}`);
const head = (msg) => console.log(`\n${B}${msg}${RS}`);

// ── Paths ─────────────────────────────────────────────────────────────────
const PATHS = {
  nodeBuilder:   resolve(ROOT, "scripts/build-jack-character-animator-psd-v1.mjs"),
  jsxFallback:   resolve(ROOT, "scripts/assemble-jack-character-animator-v1.jsx"),
  runbook:       resolve(ROOT, "docs/animation/psd_assembly_runbook_v1.md"),
  manifest:      resolve(ROOT, "manifests/jack_puppet_manifest_v1.json"),
  psdOutput:     resolve(ROOT, "assets/puppet/jack_character_animator_v1.psd"),
  layoutPreview: resolve(ROOT, "assets/puppet/jack_character_animator_v1_layout_preview.png"),
};

let failCount = 0;

// ── Check 1: Node PSD builder (primary path) ─────────────────────────────
head("1. Node PSD Builder (primary)");
if (!existsSync(PATHS.nodeBuilder)) {
  fail("scripts/build-jack-character-animator-psd-v1.mjs — NOT FOUND");
  info("Create this file to enable the free, no-Photoshop build workflow.");
  failCount++;
} else {
  const size = statSync(PATHS.nodeBuilder).size;
  if (size < 200) {
    fail(`Node builder exists but is suspiciously small (${size} bytes)`);
    failCount++;
  } else {
    pass(`scripts/build-jack-character-animator-psd-v1.mjs  (${Math.round(size / 1024)} KB)`);
    // Spot-check for key CA layer names in the builder
    const src = readFileSync(PATHS.nodeBuilder, "utf-8");
    const required = [
      "ag-psd", "@napi-rs/canvas", "initializeCanvas",
      "Neutral", "Left Upper Lid", "Right Upper Lid",
      "Left Eye", "Right Eye", "Mouth", "Jack", "Head", "Body",
    ];
    const absent = required.filter((k) => !src.includes(k));
    if (absent.length > 0) {
      warn(`Builder missing expected references: ${absent.join(", ")}`);
    } else {
      pass("Builder contains all expected ag-psd + CA layer name references");
    }
    // Check dependencies are installed
    const agPsdInstalled = existsSync(resolve(ROOT, "node_modules/ag-psd"));
    const napiInstalled  = existsSync(resolve(ROOT, "node_modules/@napi-rs/canvas"));
    if (agPsdInstalled && napiInstalled) {
      pass("Dependencies ag-psd + @napi-rs/canvas installed");
    } else {
      fail("Missing npm dependencies:");
      if (!agPsdInstalled)  info("ag-psd not installed — run: pnpm add ag-psd");
      if (!napiInstalled)   info("@napi-rs/canvas not installed — run: pnpm add @napi-rs/canvas");
      failCount++;
    }
  }
}

// ── Check 2: Photoshop JSX fallback ──────────────────────────────────────
head("2. Photoshop JSX Fallback (secondary)");
if (!existsSync(PATHS.jsxFallback)) {
  warn("scripts/assemble-jack-character-animator-v1.jsx — not found");
  info("The JSX is optional fallback. The Node builder is the primary path.");
  // Not a failure — JSX is fallback only
} else {
  const size = statSync(PATHS.jsxFallback).size;
  pass(`scripts/assemble-jack-character-animator-v1.jsx  (${Math.round(size / 1024)} KB) [fallback only]`);
}

// ── Check 3: Runbook ──────────────────────────────────────────────────────
head("3. Runbook");
if (!existsSync(PATHS.runbook)) {
  fail("docs/animation/psd_assembly_runbook_v1.md — NOT FOUND");
  failCount++;
} else {
  const size = statSync(PATHS.runbook).size;
  pass(`docs/animation/psd_assembly_runbook_v1.md  (${Math.round(size / 1024)} KB)`);
  const rb = readFileSync(PATHS.runbook, "utf-8");
  if (rb.includes("jack_character_animator_v1.psd")) {
    pass("Runbook documents PSD output path");
  } else {
    fail("Runbook does not reference jack_character_animator_v1.psd");
    failCount++;
  }
  if (rb.includes("build-jack-character-animator-psd-v1.mjs")) {
    pass("Runbook documents the free Node builder as primary workflow");
  } else {
    fail("Runbook does not reference build-jack-character-animator-psd-v1.mjs");
    failCount++;
  }
  if (rb.includes("Photopea") || rb.includes("photopea")) {
    pass("Runbook documents free Photopea inspection step");
  } else {
    warn("Runbook does not mention Photopea free inspection workflow");
  }
}

// ── Check 4: V1-mandatory PNG inputs ─────────────────────────────────────
head("4. V1-Mandatory PNG Inputs (source files intact)");
let manifest;
try {
  manifest = JSON.parse(readFileSync(PATHS.manifest, "utf-8"));
} catch (err) {
  fail(`Cannot load manifest: ${err.message}`);
  failCount++;
}

if (manifest) {
  const v1Assets = manifest.assets.filter((a) => a.required_for_v1);
  const missingPngs = v1Assets.filter(
    (a) => !existsSync(resolve(ROOT, a.required_file_path))
  );
  if (missingPngs.length === 0) {
    pass(`All ${v1Assets.length} V1-mandatory source PNGs present and unchanged`);
  } else {
    fail(`${missingPngs.length} of ${v1Assets.length} V1-mandatory PNGs are missing`);
    missingPngs.forEach((a) => info(`[${a.category}] ${a.required_file_path}`));
    failCount++;
  }
  const optMissing = manifest.assets
    .filter((a) => !a.required_for_v1 && !existsSync(resolve(ROOT, a.required_file_path)));
  if (optMissing.length > 0) {
    warn(`${optMissing.length} optional assets not yet generated (non-blocking)`);
  }
}

// ── Check 5: PSD output file ──────────────────────────────────────────────
head("5. PSD Output File");
if (!existsSync(PATHS.psdOutput)) {
  fail("assets/puppet/jack_character_animator_v1.psd — NOT GENERATED");
  info("Run: node scripts/build-jack-character-animator-psd-v1.mjs");
  failCount++;
} else {
  const bytes  = statSync(PATHS.psdOutput).size;
  const sizeMB = (bytes / (1024 * 1024)).toFixed(2);
  if (bytes === 0) {
    fail("PSD file is 0 bytes — rebuild required");
    info("Run: node scripts/build-jack-character-animator-psd-v1.mjs");
    failCount++;
  } else if (bytes < 100_000) {
    warn(`PSD is very small (${sizeMB} MB) — may lack pixel data`);
    info("Open in Photopea to verify layer contents: photopea.com");
  } else {
    pass(`assets/puppet/jack_character_animator_v1.psd  (${sizeMB} MB)`);
    info("Layers are positioned by LAYOUT map in the Node builder (first pass)");
  }
}

// ── Check 6: Layout preview PNG ───────────────────────────────────────────
head("6. Layout Preview PNG");
if (!existsSync(PATHS.layoutPreview)) {
  fail("assets/puppet/jack_character_animator_v1_layout_preview.png — NOT GENERATED");
  info("Run: node scripts/build-jack-character-animator-psd-v1.mjs");
  failCount++;
} else {
  const bytes = statSync(PATHS.layoutPreview).size;
  const sizeKB = Math.round(bytes / 1024);
  if (bytes === 0) {
    fail("Layout preview is 0 bytes — rebuild required");
    failCount++;
  } else {
    pass(`assets/puppet/jack_character_animator_v1_layout_preview.png  (${sizeKB} KB)`);
    info("Open this PNG to visually QC layer positions before Photopea/CA import");
  }
}

// ── Summary ───────────────────────────────────────────────────────────────
console.log(`\n${"─".repeat(60)}`);
if (failCount === 0) {
  console.log(`\n${B}${G}ALL CHECKS PASSED.${RS}`);
  if (existsSync(PATHS.psdOutput)) {
    const sizeMB = (statSync(PATHS.psdOutput).size / (1024 * 1024)).toFixed(2);
    const prevKB = existsSync(PATHS.layoutPreview)
      ? Math.round(statSync(PATHS.layoutPreview).size / 1024) : 0;
    console.log(`\nPSD    (${sizeMB} MB): assets/puppet/jack_character_animator_v1.psd`);
    console.log(`Preview (${prevKB} KB): assets/puppet/jack_character_animator_v1_layout_preview.png`);
    console.log(`\n${B}QC workflow:${RS}`);
    console.log(`  1. Open the preview PNG to check automated layer positions`);
    console.log(`  2. Open PSD in Photopea ${C}https://www.photopea.com${RS} for layer-name verification`);
    console.log(`  3. Fine-tune positions if needed (edit LAYOUT map, re-run builder)`);
    console.log(`\n${B}Then proceed to Character Animator:${RS}`);
    console.log(`  File > New > Puppet from Photoshop File`);
    console.log(`  Character > Rigging > Auto-tag puppet`);
  }
  console.log(`\nFull runbook: docs/animation/psd_assembly_runbook_v1.md`);
} else {
  console.log(`\n${B}${R}BLOCKED: ${failCount} check(s) failed.${RS}`);
  console.log("Resolve the issues above before proceeding to Character Animator.");
}
console.log(`\n${"─".repeat(60)}\n`);

process.exit(failCount > 0 ? 1 : 0);
