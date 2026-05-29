#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { spawnSync } from "node:child_process";
import {
  REJECTED_DIR,
  REVIEW_DIR,
  ROOT,
  activeImagePath,
  buildTrainingImagePrompt,
  existingReferenceImages,
  getPromptEntry,
  loadTrainingPrompts,
  normalizeId,
  parseArgs,
  parseIdList,
} from "./lib/jack-training-prompt.mjs";

const args = parseArgs(process.argv.slice(2));
const ids = args.ids ? parseIdList(args.ids) : args.id ? [normalizeId(args.id)] : [];
if (ids.length === 0) {
  console.error("Usage: node scripts/generate-training-image.mjs --id=024");
  console.error("   or: node scripts/generate-training-image.mjs --ids=024-028");
  process.exit(2);
}

const data = loadTrainingPrompts();
mkdirSync(REVIEW_DIR, { recursive: true });
mkdirSync(REJECTED_DIR, { recursive: true });

const codexBin = args["codex-bin"] || process.env.CODEX_BIN || (process.platform === "win32" ? "codex.cmd" : "codex");
const timeoutMs = Number(args.timeout || process.env.TRAINING_IMAGE_TIMEOUT_MS || 420000);
const dryRun = Boolean(args["dry-run"]);
const retryHarderPaws = Boolean(args["harder-paws"]);
const force = Boolean(args.force);
const references = existingReferenceImages();

if (references.length === 0) {
  console.error("ERROR: no reference images found.");
  process.exit(2);
}

for (const id of ids) {
  if (existsSync(activeImagePath(id)) && !force) {
    console.log(`[skip] ${id}: active PNG already exists. Use --force to create a review attempt anyway.`);
    continue;
  }
  const entry = getPromptEntry(data, id);
  const attempt = args.attempt ? Number(args.attempt) : nextAttempt(id);
  const target = resolve(REVIEW_DIR, `${id}_attempt${attempt}.png`);
  const logPath = resolve(REVIEW_DIR, `${id}_attempt${attempt}.log`);
  if (existsSync(target)) {
    console.error(`ERROR: review target already exists: ${target}`);
    process.exit(1);
  }

  const prompt = buildTrainingImagePrompt({ entry, targetPath: target, retryHarderPaws });
  console.log(`[run ] ${id} attempt ${attempt} -> ${target}`);
  console.log(`[refs] ${references.map((r) => r.replace(ROOT + "\\", "")).join(", ")}`);

  if (dryRun) {
    console.log(prompt);
    continue;
  }

  const codexArgs = [
    "exec",
    "--sandbox", "workspace-write",
    "--dangerously-bypass-approvals-and-sandbox",
    "-C", ROOT,
  ];
  for (const ref of references) codexArgs.push("-i", ref);
  codexArgs.push("-");

  const res = spawnSync(codexBin, codexArgs, {
    cwd: ROOT,
    input: prompt,
    encoding: "utf-8",
    maxBuffer: 50 * 1024 * 1024,
    timeout: timeoutMs,
    shell: process.platform === "win32",
  });
  const log = [res.stdout, res.stderr].filter(Boolean).join("\n");
  writeFileSync(logPath, log, "utf-8");
  if (res.error) {
    console.error(`[fail] ${id}: ${res.error.message}`);
    console.error(`Log: ${logPath}`);
    process.exit(1);
  }
  if (res.status !== 0) {
    console.error(`[fail] ${id}: ${codexBin} exited ${res.status}`);
    console.error(tail(log));
    console.error(`Log: ${logPath}`);
    process.exit(res.status || 1);
  }
  if (!existsSync(target)) {
    console.error(`[fail] ${id}: Codex exited cleanly but did not write ${target}`);
    console.error(tail(log));
    console.error(`Log: ${logPath}`);
    process.exit(1);
  }
  console.log(`[log ] ${logPath}`);
  console.log(`[review] ${id}: inspect ${target}, then accept with:`);
  console.log(`node scripts/accept-training-image.mjs --id=${id} --attempt=${attempt} --score=9.5 --notes="..."`);
}

function nextAttempt(id) {
  const names = [
    ...(existsSync(REVIEW_DIR) ? readdirSync(REVIEW_DIR) : []),
    ...(existsSync(REJECTED_DIR) ? readdirSync(REJECTED_DIR) : []),
  ];
  let max = 0;
  const re = new RegExp(`^${id}_(?:attempt|REJECTED_attempt)(\\d+)`, "i");
  for (const name of names) {
    const m = name.match(re);
    if (m) max = Math.max(max, Number(m[1]));
  }
  return max + 1;
}

function tail(text, lines = 40) {
  return String(text || "").split(/\r?\n/).slice(-lines).join("\n");
}
