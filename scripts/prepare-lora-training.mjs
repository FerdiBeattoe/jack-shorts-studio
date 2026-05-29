#!/usr/bin/env node
/**
 * prepare-lora-training.mjs
 *
 * Validates and packages the Jack LoRA training set.
 *
 * Reads images from `assets/jack-training/`, ensures each one has a paired
 * `.txt` caption file containing the trigger word `jacksaas`, requires a
 * `.score.json` audit file with score >= 9.5, and writes a
 * kohya_ss-compatible zip to `dist/jack-training.zip`.
 *
 * Usage:
 *   npm run prepare-training
 *   npm run prepare-training -- --src=assets/jack-training --out=dist/jack-training.zip
 *   npm run prepare-training -- --trigger=jacksaas --strict
 *
 * Flags:
 *   --src=<dir>      training data directory (default: assets/jack-training)
 *   --out=<path>     output zip path (default: dist/jack-training.zip)
 *   --trigger=<word> required trigger word in every caption (default: jacksaas)
 *   --strict         exit non-zero if any warnings (default: only errors fail)
 */

import { readFileSync, readdirSync, statSync, existsSync, mkdirSync, createWriteStream } from "node:fs";
import { resolve, dirname, basename, extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

const args = parseArgs(process.argv.slice(2));
const SRC = resolve(ROOT, args.src || "assets/jack-training");
const OUT = resolve(ROOT, args.out || "dist/jack-training.zip");
const TRIGGER = (args.trigger || "jacksaas").toLowerCase();
const STRICT = Boolean(args.strict);

const IMAGE_EXTS = new Set([".png", ".jpg", ".jpeg", ".webp"]);
const MAX_LONG_EDGE = 2048; // SDXL trains at 1024; >2048 wastes upload bandwidth

if (!existsSync(SRC)) {
  console.error(`ERROR: training source dir does not exist: ${SRC}`);
  console.error("Create it and drop ~20–50 Jack images plus matching .txt caption files.");
  process.exit(2);
}

// ── Discover image/caption pairs ────────────────────────────────────────────

const entries = readdirSync(SRC, { withFileTypes: true })
  .filter((e) => e.isFile())
  .map((e) => e.name);

const images = entries
  .filter((name) => IMAGE_EXTS.has(extname(name).toLowerCase()))
  .sort();

if (images.length === 0) {
  console.error(`ERROR: no images found in ${SRC} (looked for .png/.jpg/.jpeg/.webp)`);
  process.exit(2);
}

const errors = [];
const warnings = [];
const captionLengths = [];
const pairs = []; // { imagePath, captionPath, scorePath, captionText }

for (const imageName of images) {
  const imagePath = join(SRC, imageName);
  const base = basename(imageName, extname(imageName));
  const captionPath = join(SRC, `${base}.txt`);
  const scorePath = join(SRC, `${base}.score.json`);

  if (!existsSync(captionPath)) {
    errors.push(`${imageName}: missing caption file (${base}.txt)`);
    continue;
  }
  if (!existsSync(scorePath)) {
    errors.push(`${imageName}: missing score audit file (${base}.score.json)`);
    continue;
  }

  const captionText = readFileSync(captionPath, "utf-8").trim();
  if (captionText.length === 0) {
    errors.push(`${imageName}: caption file is empty`);
    continue;
  }
  if (!captionText.toLowerCase().includes(TRIGGER)) {
    errors.push(`${imageName}: caption missing trigger word "${TRIGGER}"`);
    continue;
  }
  const score = readScore(scorePath);
  if (!score.ok) {
    errors.push(`${imageName}: invalid score audit file (${score.reason})`);
    continue;
  }
  captionLengths.push(captionText.length);

  // Dimension checks (PNG only — JPG/WebP we just warn about size)
  const stat = statSync(imagePath);
  if (stat.size > 8 * 1024 * 1024) {
    warnings.push(`${imageName}: file is ${(stat.size / 1024 / 1024).toFixed(1)} MB (large)`);
  }
  if (extname(imageName).toLowerCase() === ".png") {
    const dims = readPngDimensions(imagePath);
    if (dims) {
      const long = Math.max(dims.width, dims.height);
      if (long > MAX_LONG_EDGE) {
        warnings.push(
          `${imageName}: ${dims.width}x${dims.height} — long edge ${long}px > ${MAX_LONG_EDGE}px (will be downscaled during training; consider resizing first)`
        );
      }
      if (long < 768) {
        warnings.push(`${imageName}: ${dims.width}x${dims.height} — under 768px, may train poorly at SDXL 1024`);
      }
    }
  } else {
    warnings.push(`${imageName}: ${extname(imageName)} (PNG is preferred for training)`);
  }

  pairs.push({ imagePath, captionPath, scorePath, imageName, captionName: `${base}.txt`, scoreName: `${base}.score.json` });
}

// ── Report ──────────────────────────────────────────────────────────────────

const avgCaptionChars = captionLengths.length
  ? Math.round(captionLengths.reduce((a, b) => a + b, 0) / captionLengths.length)
  : 0;

console.log(`Training source: ${SRC}`);
console.log(`Trigger word:    "${TRIGGER}"`);
console.log("");
console.log(`Images discovered: ${images.length}`);
console.log(`Valid pairs:       ${pairs.length}`);
console.log(`Avg caption chars: ${avgCaptionChars}`);
console.log("");

if (errors.length > 0) {
  console.error(`ERRORS (${errors.length}):`);
  for (const e of errors) console.error(`  - ${e}`);
  console.error("");
}
if (warnings.length > 0) {
  console.warn(`WARNINGS (${warnings.length}):`);
  for (const w of warnings) console.warn(`  - ${w}`);
  console.warn("");
}

if (errors.length > 0) {
  console.error("Aborting zip build — fix errors above and re-run.");
  process.exit(1);
}
if (pairs.length < 10) {
  console.warn(`Note: only ${pairs.length} valid pairs. SDXL LoRA typically needs 20–50 for character lock.`);
}

// ── Build zip ───────────────────────────────────────────────────────────────

mkdirSync(dirname(OUT), { recursive: true });

const archiver = await loadArchiver();
const output = createWriteStream(OUT);
const archive = archiver("zip", { zlib: { level: 9 } });

const zipDone = new Promise((res, rej) => {
  output.on("close", res);
  output.on("error", rej);
  archive.on("error", rej);
  archive.on("warning", (err) => {
    if (err.code === "ENOENT") console.warn(`archiver warning: ${err.message}`);
    else rej(err);
  });
});

archive.pipe(output);
for (const p of pairs) {
  archive.file(p.imagePath, { name: p.imageName });
  archive.file(p.captionPath, { name: p.captionName });
  archive.file(p.scorePath, { name: p.scoreName });
}
await archive.finalize();
await zipDone;

const zipSize = statSync(OUT).size;
console.log(`Wrote: ${OUT} (${(zipSize / 1024 / 1024).toFixed(2)} MB)`);
console.log(`Next: npm run hf-upload-dataset`);

if (STRICT && warnings.length > 0) {
  console.error(`\n--strict: exiting non-zero due to ${warnings.length} warning(s).`);
  process.exit(1);
}

// ── Helpers ─────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const out = {};
  for (const arg of argv) {
    if (!arg.startsWith("--")) continue;
    const eq = arg.indexOf("=");
    if (eq === -1) out[arg.slice(2)] = true;
    else out[arg.slice(2, eq)] = arg.slice(eq + 1);
  }
  return out;
}

function readPngDimensions(path) {
  try {
    const fd = readFileSync(path);
    // PNG signature is 8 bytes, then IHDR chunk: 4-byte length, 4-byte "IHDR",
    // then 4-byte width and 4-byte height at offsets 16 and 20.
    if (fd.length < 24) return null;
    if (fd.toString("ascii", 12, 16) !== "IHDR") return null;
    return { width: fd.readUInt32BE(16), height: fd.readUInt32BE(20) };
  } catch {
    return null;
  }
}

function readScore(path) {
  let data;
  try {
    data = JSON.parse(readFileSync(path, "utf-8"));
  } catch (err) {
    return { ok: false, reason: `JSON parse failed: ${err.message}` };
  }
  if (typeof data !== "object" || data === null) {
    return { ok: false, reason: "score audit is not an object" };
  }
  if (Number(data.score) < 9.5) {
    return { ok: false, reason: `score ${data.score} below 9.5` };
  }
  if (typeof data.notes !== "string" || data.notes.trim().length === 0) {
    return { ok: false, reason: "notes missing" };
  }
  if (data.reject_gate === true || data.verdict === "REJECT") {
    return { ok: false, reason: "reject gate/verdict present" };
  }
  return { ok: true };
}

async function loadArchiver() {
  try {
    const mod = await import("archiver");
    return mod.default || mod;
  } catch (err) {
    console.error("ERROR: `archiver` package not installed.");
    console.error("Run: npm install");
    process.exit(2);
  }
}
