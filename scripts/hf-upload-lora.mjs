#!/usr/bin/env node
/**
 * hf-upload-lora.mjs
 *
 * Uploads a trained .safetensors LoRA to a private HuggingFace model repo.
 * Repo name auto-increments: jack-saas-lora-v1, -v2, ...
 *
 * Usage:
 *   npm run hf-upload-lora -- --file=./jack-lora.safetensors
 *   npm run hf-upload-lora -- --file=./jack-lora.safetensors --version=3
 *   npm run hf-upload-lora -- --file=./jack-lora.safetensors --public
 *
 * Also callable from the Colab training notebook as the final step.
 */

import { existsSync, statSync } from "node:fs";
import { resolve, basename } from "node:path";
import { loadEnv, requireEnv, ROOT } from "./lib/env.mjs";
import { nextVersion, ensureRepo, uploadOneFile } from "./lib/hf.mjs";

loadEnv();
requireEnv("HF_TOKEN", "HF_USERNAME");

const args = parseArgs(process.argv.slice(2));
if (!args.file) {
  console.error("ERROR: --file=<path-to-.safetensors> is required");
  console.error("Example: npm run hf-upload-lora -- --file=./jack-lora.safetensors");
  process.exit(2);
}

const FILE = resolve(ROOT, args.file);
const PUBLIC = Boolean(args.public);

if (!existsSync(FILE)) {
  console.error(`ERROR: file not found: ${FILE}`);
  process.exit(2);
}
if (!FILE.endsWith(".safetensors")) {
  console.warn(`WARN: file does not end in .safetensors — continuing anyway`);
}

const username = process.env.HF_USERNAME;
const accessToken = process.env.HF_TOKEN;
const prefix = "jack-saas-lora";

const version = args.version
  ? Number(args.version)
  : await nextVersion({ repoType: "model", username, prefix, accessToken });

const name = `${username}/${prefix}-v${version}`;
const fileName = basename(FILE);

console.log(`Target model repo: ${name}  (${PUBLIC ? "public" : "private"})`);
console.log(`LoRA file:         ${FILE}  (${(statSync(FILE).size / 1024 / 1024).toFixed(2)} MB)`);
console.log("");

const { created } = await ensureRepo({
  repoType: "model",
  name,
  accessToken,
  isPrivate: !PUBLIC,
});
console.log(created ? "Repo created." : "Repo already exists — uploading into it.");

console.log("Uploading…");
const t0 = Date.now();
await uploadOneFile({
  repoType: "model",
  name,
  accessToken,
  localPath: FILE,
  pathInRepo: fileName,
});
const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

const repoUrl = `https://huggingface.co/${name}`;
const fileUrl = `https://huggingface.co/${name}/resolve/main/${fileName}`;

console.log("");
console.log(`Done in ${elapsed}s.`);
console.log(`Model repo: ${repoUrl}`);
console.log(`LoRA URL:   ${fileUrl}`);
console.log("");
console.log("Set this in .env:");
console.log(`  LORA_URL=${fileUrl}`);
console.log("");
console.log("Then: npm run generate-stills-lora -- --episode=cut_1a");

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
