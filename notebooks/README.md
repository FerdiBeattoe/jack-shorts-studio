# Notebooks

## train-jack-lora.ipynb — SDXL LoRA training on free Colab

Trains a character LoRA for Jack on a free Colab T4 GPU using kohya_ss/sd-scripts. Expected runtime: ~3–5 hours for 1500 steps.

### One-click open in Colab

> Replace `YOUR_GH_USER` with your GitHub user/org and `YOUR_REPO` with the repo name. Once your project is pushed to GitHub the link below will open the notebook directly.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_GH_USER/YOUR_REPO/blob/main/notebooks/train-jack-lora.ipynb)

```
https://colab.research.google.com/github/YOUR_GH_USER/YOUR_REPO/blob/main/notebooks/train-jack-lora.ipynb
```

### Prerequisites (set up locally first)

1. `npm run prepare-training` — bundles `assets/jack-training/` into `dist/jack-training.zip`.
2. `npm run hf-upload-dataset` — uploads the zip to a private HF dataset repo; note the printed name (e.g. `you/jack-saas-training-v1`).

### In Colab

1. `Runtime → Change runtime type → T4 GPU`.
2. Open `🔑 Secrets` (left sidebar) and add three secrets:
   - `HF_TOKEN` — HuggingFace token with **write** scope.
   - `HF_USERNAME` — your HF username.
   - `HF_DATASET` — full name from the upload step, e.g. `you/jack-saas-training-v1`.
3. `Runtime → Run all`.

The final cell prints a `LORA_URL=...` line. Paste it into your local `.env`, then run `npm run generate-stills-lora -- --episode=cut_1a`.

### Things that go wrong

- **"Colab secret HF_TOKEN not set"** — fix the secrets and rerun from the secrets cell.
- **OOM during training** — drop `RESOLUTION` to 768 in cell 4, or `NETWORK_DIM` to 8.
- **`xformers` install fails** — Colab's preinstalled torch may have moved; remove the version pin on the `xformers==…` line and let pip resolve.
- **Disconnected runtime mid-training** — set `MOUNT_DRIVE = True` in cell 2 so checkpoints land in your Drive; on reconnect, skip ahead to cell 6.
