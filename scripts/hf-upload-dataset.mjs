#!/usr/bin/env node
/**
 * hf-upload-dataset.mjs
 *
 * Uploads dist/jack-training.zip to a private HuggingFace dataset repo.
 * Repo name auto-increments: jack-saas-training-v1, -v2, ...
 *
 * Usage:
 *   npm run hf-upload-dataset
 *   npm run hf-upload-dataset -- --zip=dist/jack-training.zip
 *   npm run hf-upload-dataset -- --version=3      # force version, skip auto-detect
 *   npm run hf-upload-dataset -- --public         # default is private
 */

import { existsSync, statSync } from "node:fs";
import { resolve } from "node:path";
import { loadEnv, requireEnv, ROOT } from "./lib/env.mjs";
import { nextVersion, ensureRepo, uploadOneFile } from "./lib/hf.mjs";

loadEnv();
requireEnv("HF_TOKEN", "HF_USERNAME");

const args = parseArgs(process.argv.slice(2));
const ZIP = resolve(ROOT, args.zip || "dist/jack-training.zip");
const PUBLIC = Boolean(args.public);

if (!existsSync(ZIP)) {
  console.error(`ERROR: ${ZIP} not found. Run \`npm run prepare-training\` first.`);
  process.exit(2);
}

const username = process.env.HF_USERNAME;
const accessToken = process.env.HF_TOKEN;
const prefix = "jack-saas-training";

const version = args.version
  ? Number(args.version)
  : await nextVersion({ repoType: "dataset", username, prefix, accessToken });

const name = `${username}/${prefix}-v${version}`;
console.log(`Target dataset repo: ${name}  (${PUBLIC ? "public" : "private"})`);
console.log(`Zip:                 ${ZIP}  (${(statSync(ZIP).size / 1024 / 1024).toFixed(2)} MB)`);
console.log("");

const { created } = await ensureRepo({
  repoType: "dataset",
  name,
  accessToken,
  isPrivate: !PUBLIC,
});
console.log(created ? "Repo created." : "Repo already exists — uploading into it.");

console.log("Uploading…");
const t0 = Date.now();
await uploadOneFile({
  repoType: "dataset",
  name,
  accessToken,
  localPath: ZIP,
  pathInRepo: "jack-training.zip",
});
const elapsed = ((Date.now() - t0) / 1000).toFixed(1);

const url = `https://huggingface.co/datasets/${name}`;
const fileUrl = `https://huggingface.co/datasets/${name}/resolve/main/jack-training.zip`;

console.log("");
console.log(`Done in ${elapsed}s.`);
console.log(`Dataset:  ${url}`);
console.log(`Zip URL:  ${fileUrl}`);
console.log("");
console.log("Next: paste this dataset URL into the Colab notebook's HF_DATASET cell,");
console.log("      or set HF_DATASET secret in Colab to:");
console.log(`      ${name}`);

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
