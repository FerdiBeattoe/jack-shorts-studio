#!/usr/bin/env node

import { copyFileSync, existsSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  REVIEW_DIR,
  ROOT,
  activeCaptionPath,
  activeImagePath,
  getPromptEntry,
  loadTrainingPrompts,
  normalizeId,
  parseArgs,
  sanitizeCaption,
} from "./lib/jack-training-prompt.mjs";

const args = parseArgs(process.argv.slice(2));
if (!args.id) {
  console.error("Usage: node scripts/accept-training-image.mjs --id=023 --attempt=2 --score=9.6 --notes=\"why it passed\"");
  process.exit(2);
}

const id = normalizeId(args.id);
const score = Number(args.score);
const notes = String(args.notes || "").trim();
const reviewer = String(args.reviewer || "codex-four-agent-review").trim();
if (!Number.isFinite(score) || score < 0 || score > 10) {
  console.error("ERROR: --score=<0..10> is required.");
  process.exit(2);
}
if (score < 9.5) {
  console.error(`ERROR: ${id} score ${score.toFixed(1)} is below the active LoRA threshold of 9.5.`);
  process.exit(1);
}
if (!notes) {
  console.error("ERROR: --notes is required for auditability.");
  process.exit(2);
}
const data = loadTrainingPrompts();
const entry = getPromptEntry(data, id);
const attempt = args.attempt ? Number(args.attempt) : null;
const source = args.file
  ? resolve(ROOT, args.file)
  : attempt
    ? resolve(REVIEW_DIR, `${id}_attempt${attempt}.png`)
    : null;

if (!source) {
  console.error("ERROR: pass --attempt=N or --file=path/to/review.png");
  process.exit(2);
}
if (!existsSync(source)) {
  console.error(`ERROR: source image not found: ${source}`);
  process.exit(1);
}
if ((existsSync(activeImagePath(id)) || existsSync(activeCaptionPath(id))) && !args.force) {
  console.error(`ERROR: active ${id} already exists. Use --force only after quarantining/reviewing the existing active files.`);
  process.exit(1);
}

copyFileSync(source, activeImagePath(id));
writeFileSync(activeCaptionPath(id), `${sanitizeCaption(entry.lora_caption)}\n`, "utf-8");

const scorePath = activeCaptionPath(id).replace(/\.txt$/i, ".score.json");
writeFileSync(scorePath, `${JSON.stringify({
  id,
  score,
  reviewer,
  notes,
  source: source.replace(ROOT + "\\", ""),
  accepted_at: new Date().toISOString(),
}, null, 2)}\n`, "utf-8");

console.log(`Accepted ${id}`);
console.log(`PNG: ${activeImagePath(id).replace(ROOT + "\\", "")}`);
console.log(`TXT: ${activeCaptionPath(id).replace(ROOT + "\\", "")}`);
console.log(`Score: ${score.toFixed(1)}/10`);
