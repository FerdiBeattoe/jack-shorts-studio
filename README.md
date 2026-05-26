# Jack Shorts Studio

Local, deterministic short-video production pipeline for **Jack**, a 2D adult-animation humanoid golden retriever character used for TikTok content. Stills are generated either via Codex/GPT-Image or via a trained Jack character LoRA on fal.ai; Remotion composites them into 9:16 MP4s.

## Stack

- **Renderer:** Remotion 4.x + React + TypeScript
- **Still generation (reference flow):** OpenAI Codex CLI + GPT Image 2 with a locked character reference
- **Still generation (production flow):** SDXL LoRA trained on RunPod (~$1/run), inferenced via fal.ai
- **Package manager:** pnpm or npm

## Setup

```
npm install                          # or pnpm install
cp .env.example .env                 # then fill in FAL_KEY / HF_TOKEN / HF_USERNAME / RUNPOD_API_KEY
```

## Quick start (reference flow)

If you have the Codex CLI logged in and a Jack reference image at `assets/jack-reference.png`:

```
npm run generate-stills -- --episode=cut_1a --from=1 --to=3   # smoke test
npm run generate-stills -- --episode=cut_1a                   # full episode
npm run dev                                                   # preview in Remotion Studio
npm run render                                                # render MP4
```

## LoRA Training: RunPod (recommended)

Trains a Jack LoRA on an RTX A5000 (24 GB) Secure Cloud pod. End-to-end orchestration from your laptop: provisions the pod, runs training, uploads the LoRA to HuggingFace, tears down the pod, writes `LORA_URL` back into your `.env`. Typical run: ~3 hours, ~$1.

### One-time setup

1. **Sign up at [runpod.io](https://runpod.io)** and add a small balance ($5 is plenty).
2. **Create an API key** at [runpod.io/console/user/settings](https://www.runpod.io/console/user/settings) → API Keys.
3. **Set `RUNPOD_API_KEY` in your `.env`** (and also `HF_TOKEN`, `HF_USERNAME` if not already).
4. *(Optional)* **Register the RunPod MCP server with Claude Code** so you can drive provisioning conversationally from any future session:
   ```
   claude mcp add runpod --scope user -e RUNPOD_API_KEY=<your-key> -- npx -y @runpod/mcp-server@latest
   ```
   Verify with `claude mcp list`. The `npm run train-lora-runpod` script does not require the MCP — it talks to RunPod's REST API directly — but the MCP is handy for one-off pod inspection inside Claude Code.

### Per-training-run workflow

1. **Collect training images** — generate ~20–50 Jack stills via ChatGPT Plus (or any source). Varied poses, expressions, framings; all clearly the same Jack.
2. **Caption them** — for each image at `assets/jack-training/jack_NNN.png`, add a sibling `assets/jack-training/jack_NNN.txt` whose content includes the trigger token **`jacksaas`**.
   ```
   jacksaas, golden retriever in navy suit at desk, calm expression
   ```
3. **Validate and bundle** — `npm run prepare-training` (writes `dist/jack-training.zip`).
4. **Upload to HuggingFace** — `npm run hf-upload-dataset` (creates private repo `you/jack-saas-training-vN`).
5. **Kick off training** — `npm run train-lora-runpod`.
   - Auto-detects the latest dataset repo if `HF_DATASET` isn't pinned.
   - Pre-computes the next LoRA repo name `you/jack-saas-lora-vN`.
   - Provisions the pod, streams pod status, polls HF for the trained `.safetensors`.
   - On completion, terminates the pod and writes `LORA_URL=…` into your `.env`.
6. **Generate stills via the LoRA** — `npm run generate-stills-lora -- --episode=cut_1a`. Outputs land at `assets/<ep>/beat_N.png` and `public/<ep>/beat_N.png`, exactly like the Codex backend.
7. **Render** — `npm run render`.

### Useful flags

```
npm run train-lora-runpod -- --dry-run              # show pod request payload, exit
npm run train-lora-runpod -- --list-gpus            # list GPU types available on your account
npm run train-lora-runpod -- --dataset=user/foo     # override auto-detected dataset
npm run train-lora-runpod -- --gpu-type="NVIDIA RTX A4000"   # cheaper GPU
npm run train-lora-runpod -- --max-hours=4          # tighter timeout
npm run train-lora-runpod -- --keep-pod             # don't terminate on success (debugging)
```

### If something goes wrong

- **Pod stuck in CREATED / not RUNNING** — RunPod sometimes can't immediately allocate an A5000 in Secure Cloud. Wait, or pass `--cloud-type=COMMUNITY`, or pick a different `--gpu-type`.
- **HF poll never sees the file** — open `https://www.runpod.io/console/pods/<podId>` (printed at the start of the run) and check container logs. If training failed mid-way, the orchestrator will hit `--max-hours` and clean up.
- **Orchestrator crashes / Ctrl+C** — the script catches SIGINT and terminates the pod before exit. If anything escapes that, terminate manually at the console URL above.

## LoRA Training: Colab (free fallback)

If you'd rather not pay for compute, the original Colab T4 notebook still works. It takes longer (~3–5 hours on free T4 vs ~3 hours on A5000) and you have to babysit it (Colab disconnects idle sessions), but it costs $0.

Steps 1–4 are identical to the RunPod path above. Then:

5. Open `notebooks/train-jack-lora.ipynb` in Google Colab — see `notebooks/README.md` for the one-click URL and secret setup. Set runtime to T4 GPU.
6. Set Colab secrets (left sidebar): `HF_TOKEN`, `HF_USERNAME`, `HF_DATASET`.
7. `Runtime → Run all`. The notebook trains, uploads the LoRA to HuggingFace, prints `LORA_URL=…`. Paste it into your local `.env`.
8. Continue from step 6 of the RunPod workflow.

## Why this architecture

The Remotion side never knows or cares how stills were generated. `JackScene` and the compositions read from `public/<episode>/beat_N.png`, so swapping the backend is a config change, not a code change. Training off the project (Colab or RunPod) keeps weights out of git; storing them on HF keeps inference reproducible from any machine.

## Scripts

| Command | What it does |
|---|---|
| `npm run dev` | Remotion Studio (preview compositions live) |
| `npm run render` | Render the current DougEp02 composition to `renders/draft/` |
| `npm run generate-stills -- --episode=<name>` | Generate stills via Codex + GPT Image 2 (default backend) |
| `npm run generate-stills-lora -- --episode=<name>` | Generate stills via fal.ai + trained LoRA |
| `npm run prepare-training` | Validate `assets/jack-training/` and zip it for HF |
| `npm run hf-upload-dataset` | Upload `dist/jack-training.zip` to a private HF dataset repo |
| `npm run hf-upload-lora -- --file=<path>` | Upload a `.safetensors` LoRA to a private HF model repo |
| `npm run train-lora-runpod` | Provision RunPod pod, train SDXL LoRA, upload to HF, tear down |

## Environment variables

See `.env.example`. Required for the LoRA workflow:

- `RUNPOD_API_KEY` — RunPod API key (for `train-lora-runpod`)
- `HF_TOKEN` — HuggingFace token with write scope (uploads + training)
- `HF_USERNAME` — your HF username (for repo naming)
- `FAL_KEY` — fal.ai API key (for `generate-stills-lora`)
- `LORA_URL` — set automatically by `train-lora-runpod` on success, or manually from the Colab fallback

`.env` is gitignored. `.safetensors` files are gitignored.

## Directory layout

```
assets/
  jack-reference.png                   # locked character ref (Codex backend)
  jack-training/                       # ~20–50 PNG + .txt caption pairs (LoRA training)
  <episode>/
    timing_map.json                    # beat list with prompts, captions, audio path
    beat_N.png                         # generated stills (canonical copy)
public/
  <episode>/beat_N.png                 # mirror Remotion reads via staticFile()
notebooks/
  train-jack-lora.ipynb                # Colab T4 fallback training notebook
  README.md
scripts/
  generate-stills.mjs                  # dual-backend still generator
  prepare-lora-training.mjs            # validate + zip training data
  hf-upload-dataset.mjs                # private HF dataset upload
  hf-upload-lora.mjs                   # private HF model upload
  train-lora-runpod.mjs                # RunPod orchestrator (provision → train → tear down)
  runpod/train.sh                      # in-pod training bash script
  lib/env.mjs                          # .env loader
  lib/hf.mjs                           # HF API helpers (auto-versioning, file existence)
  lib/runpod.mjs                       # RunPod REST client
src/                                   # Remotion compositions and components
```
