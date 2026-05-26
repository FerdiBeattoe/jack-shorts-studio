#!/usr/bin/env node
/**
 * generate-stills.mjs
 *
 * Generates one still per beat from an episode's timing_map.json.
 *
 * Two backends:
 *   - codex-gpt-image-2  (default) — drives the Codex CLI with the Jack reference image
 *   - lora-fal                       — calls fal.ai's SDXL-LoRA endpoint with a trained Jack LoRA
 *
 * Usage:
 *   npm run generate-stills -- --episode=cut_1a
 *   npm run generate-stills -- --episode=cut_1a --backend=lora-fal
 *   npm run generate-stills-lora -- --episode=cut_1a            # same as above
 *   npm run generate-stills -- --episode=cut_1a --from=1 --to=3
 *   npm run generate-stills -- --episode=cut_1a --force
 *   npm run generate-stills -- --episode=cut_1a --dry-run
 *
 * Shared flags:
 *   --episode=<name>     (required) assets/<name>/timing_map.json
 *   --backend=<id>       codex-gpt-image-2 (default) | lora-fal
 *   --from=<id>          run beats with id >= N
 *   --to=<id>            run beats with id <= N
 *   --force              regenerate beats whose PNG already exists
 *   --dry-run            print what would happen without calling out
 *
 * codex-gpt-image-2 flags:
 *   --reference=<path>   override assets/jack-reference.png
 *   --model=<name>       image model name mentioned in the Codex prompt (default gpt-image-2)
 *
 * lora-fal flags:
 *   --lora-url=<url>     override LORA_URL from .env
 *   --lora-scale=<f>     LoRA strength (default 1.0)
 *   --steps=<n>          inference steps (default 35)
 *   --guidance=<f>       CFG (default 7.5)
 *   --trigger=<word>     trigger token prepended to each prompt (default jacksaas)
 *   --fal-endpoint=<id>  fal.ai endpoint (default fal-ai/lora)
 *
 * Env (for lora-fal):
 *   FAL_KEY       fal.ai API key
 *   LORA_URL      HF URL of the trained Jack LoRA .safetensors
 *
 * Env (for codex-gpt-image-2):
 *   CODEX_BIN          override codex executable (default: codex)
 *   STILLS_TIMEOUT_MS  per-beat timeout in ms (default: 300000)
 */

import { spawnSync } from "node:child_process";
import { readFileSync, existsSync, mkdirSync, copyFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { loadEnv } from "./lib/env.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

loadEnv(); // pulls FAL_KEY / LORA_URL from .env if present

// ── Args ─────────────────────────────────────────────────────────────────────

const args = parseArgs(process.argv.slice(2));
if (!args.episode) {
  console.error("ERROR: --episode=<name> is required");
  console.error("Example: npm run generate-stills -- --episode=cut_1a");
  process.exit(2);
}

const EPISODE = args.episode;
const BACKEND = args.backend || "codex-gpt-image-2";
const FORCE = Boolean(args.force);
const DRY_RUN = Boolean(args["dry-run"]);
const FROM = args.from !== undefined ? Number(args.from) : -Infinity;
const TO = args.to !== undefined ? Number(args.to) : Infinity;

if (!["codex-gpt-image-2", "lora-fal"].includes(BACKEND)) {
  console.error(`ERROR: unknown --backend=${BACKEND}. Valid: codex-gpt-image-2, lora-fal`);
  process.exit(2);
}

const TIMING_PATH = resolve(ROOT, "assets", EPISODE, "timing_map.json");
const ASSETS_OUT_DIR = resolve(ROOT, "assets", EPISODE);
const PUBLIC_OUT_DIR = resolve(ROOT, "public", EPISODE);

if (!existsSync(TIMING_PATH)) {
  console.error(`ERROR: missing timing map: ${TIMING_PATH}`);
  process.exit(2);
}
const timing = JSON.parse(readFileSync(TIMING_PATH, "utf-8"));
if (!Array.isArray(timing.beats) || timing.beats.length === 0) {
  console.error(`ERROR: timing map has no beats: ${TIMING_PATH}`);
  process.exit(2);
}

mkdirSync(ASSETS_OUT_DIR, { recursive: true });
mkdirSync(PUBLIC_OUT_DIR, { recursive: true });

// Configure backend-specific state up front so we fail fast on missing config.
const backendCtx = BACKEND === "lora-fal" ? prepareLoraFal(args) : prepareCodex(args);

// ── Run ──────────────────────────────────────────────────────────────────────

const beats = timing.beats.filter((b) => b.id >= FROM && b.id <= TO);
const results = { generated: [], skipped: [], failed: [] };

console.log(`Episode: ${EPISODE} — ${beats.length}/${timing.beats.length} beats in [${rangeLabel(FROM)}..${rangeLabel(TO)}]`);
console.log(`Backend: ${BACKEND}`);
console.log(backendCtx.summary);
console.log(`Output:  ${ASSETS_OUT_DIR}\\beat_<id>.png  (mirrored to public/${EPISODE}/)`);
console.log(DRY_RUN ? "Mode:    [DRY RUN]\n" : "");

for (const beat of beats) {
  const filename = `beat_${beat.id}.png`;
  const assetTarget = resolve(ASSETS_OUT_DIR, filename);
  const publicTarget = resolve(PUBLIC_OUT_DIR, filename);

  if (existsSync(assetTarget) && !FORCE) {
    if (!existsSync(publicTarget)) copyFileSync(assetTarget, publicTarget);
    console.log(`[skip] beat ${beat.id}: already exists (use --force to regenerate)`);
    results.skipped.push(beat.id);
    continue;
  }

  console.log(`[run ] beat ${beat.id} (${beat.start}s–${beat.end}s) → ${filename}`);
  const t0 = Date.now();
  try {
    if (DRY_RUN) {
      backendCtx.dryRun(beat, assetTarget);
    } else {
      await backendCtx.generate(beat, assetTarget);
      if (!existsSync(assetTarget)) throw new Error("no output file written");
      copyFileSync(assetTarget, publicTarget);
    }
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
    console.log(`[ok  ] beat ${beat.id} in ${elapsed}s`);
    results.generated.push(beat.id);
  } catch (err) {
    const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
    console.error(`[FAIL] beat ${beat.id}: ${err.message} (after ${elapsed}s)`);
    results.failed.push(beat.id);
  }
}

console.log("");
console.log(`Done. generated=${results.generated.length}  skipped=${results.skipped.length}  failed=${results.failed.length}`);
if (results.failed.length > 0) {
  console.error("Failed beats: " + results.failed.join(", "));
  process.exit(1);
}

// ── Backend: codex-gpt-image-2 ──────────────────────────────────────────────

function prepareCodex(args) {
  const REFERENCE = resolve(ROOT, args.reference || "assets/jack-reference.png");
  const MODEL = args.model || "gpt-image-2";
  const CODEX_BIN = process.env.CODEX_BIN || "codex";
  const TIMEOUT_MS = Number(process.env.STILLS_TIMEOUT_MS) || 300_000;

  if (!existsSync(REFERENCE)) {
    console.error(`ERROR: missing character reference: ${REFERENCE}`);
    process.exit(2);
  }
  if (!DRY_RUN) {
    const probe = spawnSync(CODEX_BIN, ["--version"], { stdio: "pipe", shell: process.platform === "win32" });
    if (probe.status !== 0) {
      console.error(`ERROR: cannot run \`${CODEX_BIN} --version\`. Is the Codex CLI installed?`);
      process.exit(2);
    }
  }

  return {
    summary: `Reference: ${REFERENCE}\nModel:     ${MODEL} (instructed via Codex prompt)\nCodex:     ${CODEX_BIN}  timeout=${TIMEOUT_MS}ms`,
    dryRun(beat, target) {
      const prompt = buildCodexPrompt({ timing, beat, target, model: MODEL });
      console.log("       " + CODEX_BIN + ` exec -i ${REFERENCE} "<${prompt.length} chars>"`);
    },
    async generate(beat, target) {
      const prompt = buildCodexPrompt({ timing, beat, target, model: MODEL });
      const codexArgs = [
        "exec",
        "--sandbox", "workspace-write",
        "--dangerously-bypass-approvals-and-sandbox",
        "-C", ROOT,
        "-i", REFERENCE,
        prompt,
      ];
      const res = spawnSync(CODEX_BIN, codexArgs, {
        stdio: "inherit",
        timeout: TIMEOUT_MS,
        shell: process.platform === "win32",
      });
      if (res.status !== 0) throw new Error(`codex exited ${res.status}`);
    },
  };
}

function buildCodexPrompt({ timing, beat, target, model }) {
  const character = timing.character || "the character in the attached reference image";
  const world = timing.world || "";
  const styleLock = timing.style_lock || "";
  return [
    `You are generating one still frame for a stop-motion short. Use the ${model} image-generation tool in thinking mode.`,
    ``,
    `Character (locked, must match the attached reference exactly): ${character}`,
    world ? `World: ${world}` : null,
    styleLock ? `Style lock: ${styleLock}` : null,
    ``,
    `Scene description for THIS still:`,
    beat.prompt,
    ``,
    `Output requirements:`,
    `- Aspect ratio: 9:16 (portrait, 1080x1920).`,
    `- Single PNG, no text, no captions, no watermarks, no UI overlays on the character.`,
    `- Character identity must match the attached reference. Do not redesign Jack.`,
    `- Save the generated PNG to this exact absolute path: ${target}`,
    `- Do not modify any other file in the workspace. Do not commit anything.`,
    `- When the file is written, stop. Do not ask follow-up questions.`,
  ].filter(Boolean).join("\n");
}

// ── Backend: lora-fal ───────────────────────────────────────────────────────

function prepareLoraFal(args) {
  const LORA_URL = args["lora-url"] || process.env.LORA_URL;
  const FAL_KEY = process.env.FAL_KEY;
  const LORA_SCALE = args["lora-scale"] !== undefined ? Number(args["lora-scale"]) : 1.0;
  const STEPS = args.steps !== undefined ? Number(args.steps) : 35;
  const GUIDANCE = args.guidance !== undefined ? Number(args.guidance) : 7.5;
  const TRIGGER = args.trigger || "jacksaas";
  const ENDPOINT = args["fal-endpoint"] || "fal-ai/lora";

  if (!FAL_KEY) {
    console.error("ERROR: FAL_KEY not set. Add it to .env or export it in your shell.");
    process.exit(2);
  }
  if (!LORA_URL) {
    console.error("ERROR: LORA_URL not set. Set it in .env (from the Colab training notebook output) or pass --lora-url=<url>.");
    process.exit(2);
  }

  let falClientPromise = null;
  async function getFalClient() {
    if (!falClientPromise) {
      falClientPromise = (async () => {
        let mod;
        try {
          mod = await import("@fal-ai/client");
        } catch (err) {
          console.error("ERROR: `@fal-ai/client` package not installed. Run: npm install");
          throw err;
        }
        const { fal } = mod;
        fal.config({ credentials: FAL_KEY });
        return fal;
      })();
    }
    return falClientPromise;
  }

  return {
    summary: `Endpoint:  ${ENDPOINT}\nLoRA URL:  ${LORA_URL}\nLoRA scale: ${LORA_SCALE}  steps: ${STEPS}  guidance: ${GUIDANCE}  trigger: "${TRIGGER}"`,
    dryRun(beat, target) {
      const prompt = `${TRIGGER}, ${beat.prompt}`;
      console.log(`       fal.subscribe(${ENDPOINT}, prompt="${prompt.slice(0, 80)}…", lora=${LORA_URL}@${LORA_SCALE}) → ${target}`);
    },
    async generate(beat, target) {
      const fal = await getFalClient();
      const prompt = `${TRIGGER}, ${beat.prompt}`;
      const negative_prompt = "text, watermark, logo, signature, ui overlay, low quality, blurry, deformed hands, extra fingers";

      const result = await fal.subscribe(ENDPOINT, {
        input: {
          prompt,
          negative_prompt,
          loras: [{ path: LORA_URL, scale: LORA_SCALE }],
          image_size: "portrait_16_9",
          num_inference_steps: STEPS,
          guidance_scale: GUIDANCE,
          num_images: 1,
          enable_safety_checker: false,
        },
        logs: false,
      });

      const data = result?.data || result;
      const url = data?.images?.[0]?.url;
      if (!url) throw new Error("fal returned no image URL (check endpoint and LORA_URL)");

      const resp = await fetch(url);
      if (!resp.ok) throw new Error(`download failed: HTTP ${resp.status}`);
      const buf = Buffer.from(await resp.arrayBuffer());
      writeFileSync(target, buf);
    },
  };
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

function rangeLabel(n) {
  if (n === -Infinity) return "*";
  if (n === Infinity) return "*";
  return String(n);
}
