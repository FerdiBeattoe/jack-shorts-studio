#!/usr/bin/env node

import { existsSync, mkdirSync, renameSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  REJECTED_DIR,
  ROOT,
  activeCaptionPath,
  activeImagePath,
  normalizeId,
  parseArgs,
} from "./lib/jack-training-prompt.mjs";

const args = parseArgs(process.argv.slice(2));
if (!args.id || !args.reason) {
  console.error("Usage: node scripts/quarantine-training-image.mjs --id=020 --reason=\"nail defect\"");
  process.exit(2);
}

const id = normalizeId(args.id);
const reason = String(args.reason).trim();
const suffix = slug(reason);

mkdirSync(REJECTED_DIR, { recursive: true });

const moved = [];
moveIfExists(activeImagePath(id), resolve(REJECTED_DIR, `${id}_REJECTED_${suffix}.png`));
moveIfExists(activeCaptionPath(id), resolve(REJECTED_DIR, `${id}_REJECTED_${suffix}.txt`));
moveIfExists(activeCaptionPath(id).replace(/\.txt$/i, ".score.json"), resolve(REJECTED_DIR, `${id}_REJECTED_${suffix}.score.json`));

const notePath = resolve(REJECTED_DIR, `${id}_REJECTED_${suffix}.review.json`);
writeFileSync(notePath, `${JSON.stringify({
  id,
  reason,
  moved,
  quarantined_at: new Date().toISOString(),
}, null, 2)}\n`, "utf-8");

for (const item of moved) {
  console.log(`moved: ${item.from.replace(ROOT + "\\", "")} -> ${item.to.replace(ROOT + "\\", "")}`);
}
console.log(`review: ${notePath.replace(ROOT + "\\", "")}`);

function moveIfExists(from, to) {
  if (!existsSync(from)) return;
  if (existsSync(to)) {
    const ext = to.match(/\.[^.]+$/)?.[0] || "";
    const base = ext ? to.slice(0, -ext.length) : to;
    let i = 2;
    while (existsSync(`${base}_${i}${ext}`)) i++;
    to = `${base}_${i}${ext}`;
  }
  renameSync(from, to);
  moved.push({ from, to });
}

function slug(value) {
  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "review-failed";
}
