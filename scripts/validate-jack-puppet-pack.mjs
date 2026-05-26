#!/usr/bin/env node
/**
 * validate-jack-puppet-pack.mjs
 *
 * Checks whether all required puppet layer assets in jack_puppet_manifest_v1.json
 * exist on disk. Reports present/missing counts grouped by category.
 * Exits with code 1 if any V1-mandatory assets are missing.
 *
 * Usage:
 *   node scripts/validate-jack-puppet-pack.mjs
 */

import { readFileSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const MANIFEST_PATH = resolve(ROOT, "manifests/jack_puppet_manifest_v1.json");

// ── Load manifest ──────────────────────────────────────────────────────────

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST_PATH, "utf-8"));
} catch (err) {
  console.error(`ERROR: Could not read manifest at ${MANIFEST_PATH}`);
  console.error(err.message);
  process.exit(1);
}

const { assets } = manifest;

// ── Check each asset ───────────────────────────────────────────────────────

const results = assets.map((asset) => {
  const fullPath = resolve(ROOT, asset.required_file_path);
  const present = existsSync(fullPath);
  return { ...asset, present, fullPath };
});

// ── Build summary ──────────────────────────────────────────────────────────

const present = results.filter((a) => a.present);
const missing = results.filter((a) => !a.present);
const missingV1 = missing.filter((a) => a.required_for_v1);
const missingOptional = missing.filter((a) => !a.required_for_v1);

// Group missing by category
const missingByCategory = {};
for (const asset of missing) {
  if (!missingByCategory[asset.category]) {
    missingByCategory[asset.category] = [];
  }
  missingByCategory[asset.category].push(asset);
}

// ── Print report ───────────────────────────────────────────────────────────

const RESET = "\x1b[0m";
const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const BOLD = "\x1b[1m";
const DIM = "\x1b[2m";

console.log(`\n${BOLD}Jack Puppet Pack Validation${RESET}`);
console.log(`Manifest: ${MANIFEST_PATH}`);
console.log(`Root: ${ROOT}`);
console.log(`─`.repeat(60));

console.log(`\n${BOLD}Summary${RESET}`);
console.log(`  ${GREEN}Present:${RESET}            ${present.length} / ${assets.length}`);
console.log(`  ${RED}Missing (V1):${RESET}       ${missingV1.length}`);
console.log(`  ${YELLOW}Missing (optional):${RESET} ${missingOptional.length}`);

if (present.length > 0) {
  console.log(`\n${BOLD}${GREEN}Present Assets${RESET}`);
  for (const asset of present) {
    console.log(`  ${GREEN}✓${RESET} [${asset.category}] ${asset.asset_id}`);
    console.log(`      ${DIM}${asset.required_file_path}${RESET}`);
  }
}

if (missing.length > 0) {
  console.log(`\n${BOLD}${RED}Missing Assets by Category${RESET}`);
  for (const [category, categoryAssets] of Object.entries(missingByCategory)) {
    const v1Count = categoryAssets.filter((a) => a.required_for_v1).length;
    const optCount = categoryAssets.filter((a) => !a.required_for_v1).length;
    const label = v1Count > 0 ? `${RED}${category}${RESET}` : `${YELLOW}${category}${RESET}`;
    console.log(`\n  ${BOLD}${label}${RESET} (${v1Count} V1-required, ${optCount} optional)`);

    for (const asset of categoryAssets) {
      const tag = asset.required_for_v1 ? `${RED}[V1]${RESET}` : `${YELLOW}[opt]${RESET}`;
      console.log(`    ${tag} ${asset.asset_id}`);
      console.log(`         ${DIM}${asset.required_file_path}${RESET}`);
      if (asset.notes) {
        console.log(`         ${DIM}→ ${asset.notes}${RESET}`);
      }
    }
  }
}

// ── Next steps ─────────────────────────────────────────────────────────────

if (missingV1.length > 0) {
  console.log(`\n${BOLD}${RED}BLOCKED:${RESET} ${missingV1.length} V1-mandatory assets are missing.`);
  console.log(`\nTo generate missing assets:`);
  console.log(`  1. Open prompts/animation/jack_puppet_generation_prompt_book.md`);
  console.log(`  2. Use the relevant prompt for each missing category`);
  console.log(`  3. Save to the required_file_path shown above`);
  console.log(`  4. Run this script again to verify`);
} else if (missingOptional.length > 0) {
  console.log(`\n${BOLD}${GREEN}V1 READY:${RESET} All mandatory assets present.`);
  console.log(`${YELLOW}Note:${RESET} ${missingOptional.length} optional assets still missing.`);
  console.log(`Proceed to PSD assembly — see docs/animation/character_animator_layer_naming_v1.md`);
} else {
  console.log(`\n${BOLD}${GREEN}ALL ASSETS PRESENT.${RESET} Ready for PSD assembly.`);
}

console.log(`\n${"─".repeat(60)}\n`);

// ── Exit code ──────────────────────────────────────────────────────────────

if (missingV1.length > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
