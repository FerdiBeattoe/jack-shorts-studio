#!/usr/bin/env node

import { existsSync, writeFileSync } from "node:fs";
import {
  ROOT,
  activeCaptionPath,
  activeImagePath,
  normalizeId,
  parseArgs,
} from "./lib/jack-training-prompt.mjs";

const args = parseArgs(process.argv.slice(2));
if (!args.id || !args.score || !args.notes) {
  console.error("Usage: node scripts/score-active-training-image.mjs --id=009 --score=9.6 --notes=\"why it passes\"");
  process.exit(2);
}

const id = normalizeId(args.id);
const score = Number(args.score);
const notes = String(args.notes).trim();
const reviewer = String(args.reviewer || "codex-four-agent-review").trim();
const verdict = String(args.verdict || "ACCEPT").trim();

if (!existsSync(activeImagePath(id))) {
  console.error(`ERROR: active image missing for ${id}`);
  process.exit(1);
}
if (!existsSync(activeCaptionPath(id))) {
  console.error(`ERROR: active caption missing for ${id}`);
  process.exit(1);
}
if (!Number.isFinite(score) || score < 9.5 || score > 10) {
  console.error("ERROR: --score must be between 9.5 and 10 for an active counted image.");
  process.exit(2);
}

const scorePath = activeCaptionPath(id).replace(/\.txt$/i, ".score.json");
writeFileSync(scorePath, `${JSON.stringify({
  id,
  score,
  verdict,
  reviewer,
  notes,
  source: activeImagePath(id).replace(ROOT + "\\", ""),
  accepted_at: new Date().toISOString(),
}, null, 2)}\n`, "utf-8");

console.log(`Scored ${id}: ${score.toFixed(1)}/10`);
