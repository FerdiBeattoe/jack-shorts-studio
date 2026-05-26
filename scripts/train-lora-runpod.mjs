#!/usr/bin/env node
/**
 * train-lora-runpod.mjs
 *
 * Provisions an RTX A5000 on RunPod Secure Cloud, runs the in-pod training
 * script (scripts/runpod/train.sh) end-to-end, waits for the trained LoRA to
 * appear on HuggingFace, then terminates the pod and writes LORA_URL to .env.
 *
 * Default specs:
 *   GPU            NVIDIA RTX A5000 (24 GB)
 *   Image          runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
 *   Container disk 20 GB
 *   Volume disk    50 GB (mounted at /workspace, holds dataset + checkpoints)
 *   Ports          22/tcp (SSH), 8888/http (Jupyter, optional)
 *   Cost           ~$0.30–$0.40 / hr → ~$1 per training run (3 hours typical)
 *
 * Workflow:
 *   1. Pre-compute next LoRA repo version (e.g. user/jack-saas-lora-v3)
 *   2. base64-encode train.sh and pass it as a pod env var
 *   3. POST /v1/pods with a PyTorch image and dockerArgs that decode+run the script
 *   4. Poll HF for jack-lora.safetensors at the pre-computed repo URL
 *   5. Terminate pod
 *   6. Update .env with the new LORA_URL
 *
 * Usage:
 *   npm run train-lora-runpod
 *   npm run train-lora-runpod -- --dataset=you/jack-saas-training-v2
 *   npm run train-lora-runpod -- --gpu-type="NVIDIA RTX A5000" --cloud-type=SECURE
 *   npm run train-lora-runpod -- --max-hours=6 --poll-interval=60
 *   npm run train-lora-runpod -- --dry-run
 *   npm run train-lora-runpod -- --list-gpus
 *
 * Flags:
 *   --dataset=<name>      HF dataset to train on (default: env HF_DATASET or auto-detect latest)
 *   --gpu-type=<id>       RunPod GPU type ID (default: "NVIDIA RTX A5000")
 *   --cloud-type=SECURE|COMMUNITY  (default: SECURE)
 *   --image=<name>        container image (default: PyTorch 2.4.0 / CUDA 12.4)
 *   --container-disk=<gb> (default: 20)
 *   --volume-disk=<gb>    persistent volume in GB (default: 50)
 *   --max-hours=<n>       safety guard — terminate if not done by then (default: 8)
 *   --poll-interval=<sec> HF poll cadence (default: 60)
 *   --no-update-env       skip writing LORA_URL into .env
 *   --keep-pod            don't terminate pod after success (for debugging)
 *   --dry-run             print the pod creation payload and exit (works without npm install)
 *   --list-gpus           list available GPU types on RunPod and exit
 *
 * Env:
 *   RUNPOD_API_KEY        required (skipped for --dry-run)
 *   HF_TOKEN              required (write scope; skipped for --dry-run)
 *   HF_USERNAME           required (skipped for --dry-run)
 *   HF_DATASET            optional; auto-detected from latest jack-saas-training-v* if absent
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { loadEnv, requireEnv, ROOT } from "./lib/env.mjs";
import { nextVersion, latestVersion, fileExists } from "./lib/hf.mjs";
import { createPod, getPod, terminatePod, listGpuTypes } from "./lib/runpod.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));

loadEnv();

const args = parseArgs(process.argv.slice(2));

const DRY_RUN = Boolean(args["dry-run"]);

if (args["list-gpus"]) {
  requireEnv("RUNPOD_API_KEY");
  const types = await listGpuTypes({ apiKey: process.env.RUNPOD_API_KEY });
  console.log(JSON.stringify(types, null, 2));
  process.exit(0);
}

if (!DRY_RUN) {
  requireEnv("RUNPOD_API_KEY", "HF_TOKEN", "HF_USERNAME");
}

const GPU_TYPE = args["gpu-type"] || "NVIDIA RTX A5000";
const CLOUD_TYPE = (args["cloud-type"] || "SECURE").toUpperCase();
const IMAGE = args.image || "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04";
const CONTAINER_DISK_GB = Number(args["container-disk"] || 20);
const VOLUME_DISK_GB = Number(args["volume-disk"] || 50);
const MAX_HOURS = Number(args["max-hours"] || 8);
const POLL_INTERVAL_S = Number(args["poll-interval"] || 60);
const UPDATE_ENV = args["no-update-env"] ? false : true;
const KEEP_POD = Boolean(args["keep-pod"]);

const HF_USERNAME = process.env.HF_USERNAME || (DRY_RUN ? "<HF_USERNAME>" : null);
const HF_TOKEN = process.env.HF_TOKEN || (DRY_RUN ? "<HF_TOKEN>" : null);

// ── Resolve dataset + LoRA version ──────────────────────────────────────────
// In dry-run we use placeholders instead of hitting HF — lets the user inspect
// the pod request payload before installing deps or setting tokens.

let HF_DATASET;
let LORA_REPO_NAME;
let LORA_URL;

if (DRY_RUN && (!process.env.HF_TOKEN || !process.env.HF_USERNAME)) {
  HF_DATASET = args.dataset || process.env.HF_DATASET || `${HF_USERNAME}/jack-saas-training-vN`;
  LORA_REPO_NAME = `${HF_USERNAME}/jack-saas-lora-vN`;
  LORA_URL = `https://huggingface.co/${LORA_REPO_NAME}/resolve/main/jack-lora.safetensors`;
  console.log("(dry-run: using placeholder dataset/LoRA names — set HF_TOKEN+HF_USERNAME to resolve real versions)");
} else {
  HF_DATASET = args.dataset || process.env.HF_DATASET;
  if (!HF_DATASET) {
    const latest = await latestVersion({
      repoType: "dataset",
      username: HF_USERNAME,
      prefix: "jack-saas-training",
      accessToken: HF_TOKEN,
    });
    if (latest === 0) {
      console.error("ERROR: no HF_DATASET set and no `jack-saas-training-v*` dataset found on HF.");
      console.error("Run `npm run prepare-training && npm run hf-upload-dataset` first,");
      console.error("or pass --dataset=<owner>/<name>.");
      process.exit(2);
    }
    HF_DATASET = `${HF_USERNAME}/jack-saas-training-v${latest}`;
    console.log(`Auto-detected dataset: ${HF_DATASET}`);
  }

  const loraVersion = await nextVersion({
    repoType: "model",
    username: HF_USERNAME,
    prefix: "jack-saas-lora",
    accessToken: HF_TOKEN,
  });
  LORA_REPO_NAME = `${HF_USERNAME}/jack-saas-lora-v${loraVersion}`;
  LORA_URL = `https://huggingface.co/${LORA_REPO_NAME}/resolve/main/jack-lora.safetensors`;
}

// ── Build pod request ───────────────────────────────────────────────────────

const TRAIN_SH_PATH = resolve(__dirname, "runpod", "train.sh");
if (!existsSync(TRAIN_SH_PATH)) {
  console.error(`ERROR: missing in-pod script: ${TRAIN_SH_PATH}`);
  process.exit(2);
}
const trainSh = readFileSync(TRAIN_SH_PATH, "utf-8");
const trainShB64 = Buffer.from(trainSh, "utf-8").toString("base64");

// Decode the script from env then run it. Stream logs to stdout so RunPod captures them.
const dockerArgs = `bash -lc 'echo "$STARTUP_SCRIPT_B64" | base64 -d > /tmp/train.sh && chmod +x /tmp/train.sh && bash /tmp/train.sh 2>&1'`;

const podRequest = {
  name: `${LORA_REPO_NAME.split("/")[1]}-${Date.now().toString(36)}`,
  imageName: IMAGE,
  gpuTypeIds: [GPU_TYPE],
  cloudType: CLOUD_TYPE,
  gpuCount: 1,
  containerDiskInGb: CONTAINER_DISK_GB,
  volumeInGb: VOLUME_DISK_GB,
  volumeMountPath: "/workspace",
  ports: "22/tcp,8888/http",
  env: [
    { key: "HF_TOKEN", value: HF_TOKEN },
    { key: "HF_USERNAME", value: HF_USERNAME },
    { key: "HF_DATASET", value: HF_DATASET },
    { key: "LORA_REPO_NAME", value: LORA_REPO_NAME },
    { key: "STARTUP_SCRIPT_B64", value: trainShB64 },
  ],
  dockerArgs,
  supportPublicIp: true, // needed for SSH from your laptop if you want to debug mid-training
};

// ── Plan summary ────────────────────────────────────────────────────────────

console.log("=".repeat(70));
console.log("RunPod LoRA training plan");
console.log("=".repeat(70));
console.log(`Dataset:        ${HF_DATASET}`);
console.log(`Target LoRA:    ${LORA_REPO_NAME}`);
console.log(`Target URL:     ${LORA_URL}`);
console.log(`GPU:            ${GPU_TYPE}  (${CLOUD_TYPE})`);
console.log(`Image:          ${IMAGE}`);
console.log(`Container disk: ${CONTAINER_DISK_GB} GB`);
console.log(`Volume disk:    ${VOLUME_DISK_GB} GB (mounted at /workspace)`);
console.log(`Ports:          22/tcp (SSH), 8888/http (Jupyter)`);
console.log(`Max wall time:  ${MAX_HOURS} hours`);
console.log(`Poll interval:  ${POLL_INTERVAL_S} s`);
console.log("=".repeat(70));

if (DRY_RUN) {
  console.log("\n[DRY RUN] Pod request payload (env values redacted):");
  const redacted = {
    ...podRequest,
    env: podRequest.env.map((e) =>
      ["HF_TOKEN", "STARTUP_SCRIPT_B64"].includes(e.key) ? { key: e.key, value: "<redacted>" } : e
    ),
  };
  console.log(JSON.stringify(redacted, null, 2));
  process.exit(0);
}

// ── Create pod ──────────────────────────────────────────────────────────────

let podId = null;
let signalReceived = false;

async function cleanup(reason) {
  if (!podId || KEEP_POD) return;
  console.log(`Cleaning up pod ${podId} (${reason})…`);
  try {
    await terminatePod({ apiKey: process.env.RUNPOD_API_KEY, id: podId });
    console.log("Pod terminated.");
  } catch (err) {
    console.error(`WARN: failed to terminate pod ${podId}: ${err.message}`);
    console.error("Terminate manually at https://www.runpod.io/console/pods");
  }
}

for (const sig of ["SIGINT", "SIGTERM"]) {
  process.on(sig, async () => {
    if (signalReceived) return;
    signalReceived = true;
    console.log(`\nReceived ${sig}.`);
    await cleanup(sig);
    process.exit(130);
  });
}

console.log("\nProvisioning pod…");
const created = await createPod({ apiKey: process.env.RUNPOD_API_KEY, ...podRequest });
podId = created?.id || created?.pod?.id;
if (!podId) {
  console.error("ERROR: pod creation returned no id. Response:");
  console.error(JSON.stringify(created, null, 2));
  process.exit(1);
}
console.log(`Pod created: ${podId}`);
console.log(`Logs / SSH:  https://www.runpod.io/console/pods/${podId}`);

// ── Wait for RUNNING ────────────────────────────────────────────────────────

try {
  await waitForRunning({ podId, timeoutMs: 10 * 60 * 1000 });

  // ── Poll HF for the trained file ──────────────────────────────────────────

  console.log(`\nTraining started. Polling ${LORA_URL} every ${POLL_INTERVAL_S}s…`);
  const deadlineMs = Date.now() + MAX_HOURS * 3600 * 1000;
  let lastStatusLogMs = 0;

  while (Date.now() < deadlineMs) {
    if (await fileExists({ repoType: "model", name: LORA_REPO_NAME, pathInRepo: "jack-lora.safetensors", accessToken: HF_TOKEN })) {
      console.log("\n✓ LoRA file detected on HuggingFace.");
      break;
    }

    // Every ~5 min log the pod status so we know it's still alive
    if (Date.now() - lastStatusLogMs > 5 * 60 * 1000) {
      lastStatusLogMs = Date.now();
      try {
        const pod = await getPod({ apiKey: process.env.RUNPOD_API_KEY, id: podId });
        const status = pod?.desiredStatus || pod?.runtime?.podType || "UNKNOWN";
        const cost = pod?.costPerHr ? ` ($${pod.costPerHr}/hr)` : "";
        console.log(`  …still training. pod=${status}${cost}  elapsed=${fmtElapsed(Date.now() - (deadlineMs - MAX_HOURS * 3600 * 1000))}`);
      } catch {
        // Non-fatal; keep polling HF
      }
    }

    await sleep(POLL_INTERVAL_S * 1000);
  }

  if (!(await fileExists({ repoType: "model", name: LORA_REPO_NAME, pathInRepo: "jack-lora.safetensors", accessToken: HF_TOKEN }))) {
    throw new Error(`timed out after ${MAX_HOURS}h waiting for ${LORA_URL}`);
  }

  // ── Success — terminate pod, update .env ─────────────────────────────────

  await cleanup("training complete");

  console.log("");
  console.log("=".repeat(70));
  console.log("TRAINING COMPLETE");
  console.log("=".repeat(70));
  console.log(`Repo:     https://huggingface.co/${LORA_REPO_NAME}`);
  console.log(`LoRA URL: ${LORA_URL}`);
  console.log("");

  if (UPDATE_ENV) {
    upsertEnvVar(resolve(ROOT, ".env"), "LORA_URL", LORA_URL);
    console.log(`Updated .env: LORA_URL=${LORA_URL}`);
  } else {
    console.log("Paste into .env:");
    console.log(`  LORA_URL=${LORA_URL}`);
  }
  console.log("");
  console.log("Next: npm run generate-stills-lora -- --episode=cut_1a");
} catch (err) {
  console.error(`\nERROR: ${err.message}`);
  await cleanup("error");
  process.exit(1);
}

// ── Helpers ─────────────────────────────────────────────────────────────────

async function waitForRunning({ podId, timeoutMs }) {
  const start = Date.now();
  let lastStatus = null;
  while (Date.now() - start < timeoutMs) {
    const pod = await getPod({ apiKey: process.env.RUNPOD_API_KEY, id: podId });
    const status = pod?.desiredStatus || pod?.status || "UNKNOWN";
    if (status !== lastStatus) {
      console.log(`  pod status: ${status}`);
      lastStatus = status;
    }
    if (/RUNNING|RUN|STARTED/i.test(status)) return;
    if (/EXITED|FAIL|TERMINATED|ERROR/i.test(status)) {
      throw new Error(`pod entered terminal state before training started: ${status}`);
    }
    await sleep(10_000);
  }
  throw new Error(`pod did not reach RUNNING within ${timeoutMs / 1000}s`);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function fmtElapsed(ms) {
  const s = Math.floor(ms / 1000);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return `${h}h${m.toString().padStart(2, "0")}m`;
}

function upsertEnvVar(path, key, value) {
  let text = existsSync(path) ? readFileSync(path, "utf-8") : "";
  const re = new RegExp(`^${key}=.*$`, "m");
  const line = `${key}=${value}`;
  text = re.test(text) ? text.replace(re, line) : (text.endsWith("\n") || text.length === 0 ? text : text + "\n") + line + "\n";
  writeFileSync(path, text);
}

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
