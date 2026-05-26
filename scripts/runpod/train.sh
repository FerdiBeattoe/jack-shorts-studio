#!/usr/bin/env bash
# In-pod training script. Runs inside a RunPod PyTorch container provisioned
# by scripts/runpod-train-lora.mjs.
#
# The orchestrator base64-encodes this file into the pod's STARTUP_SCRIPT_B64
# env var, and the pod's container CMD decodes and runs it.
#
# Required env (set by the orchestrator):
#   HF_TOKEN           HuggingFace write token
#   HF_USERNAME        HF user (for logging only — repo name is pre-computed)
#   HF_DATASET         dataset repo, e.g. "user/jack-saas-training-v1"
#   LORA_REPO_NAME     target model repo, e.g. "user/jack-saas-lora-v3"
#
# Optional env (defaults applied if unset):
#   TRIGGER            default: jacksaas
#   REPEATS            default: 10        (kohya_ss "{N}_{class}" repeats)
#   BASE_MODEL         default: stabilityai/stable-diffusion-xl-base-1.0
#   RESOLUTION         default: 1024
#   BATCH_SIZE         default: 1
#   GRAD_ACCUM         default: 2
#   NETWORK_DIM        default: 16
#   NETWORK_ALPHA      default: 16
#   LEARNING_RATE      default: 1e-4
#   MAX_TRAIN_STEPS    default: 1500
#   SAVE_EVERY_STEPS   default: 250
#   MIXED_PRECISION    default: fp16
#   OPTIMIZER          default: AdamW8bit

set -euo pipefail
set -o errtrace

step() { echo ""; echo "===== $* ====="; date -u +"      utc=%Y-%m-%dT%H:%M:%SZ"; }
fail() { echo "FATAL: $*" >&2; exit 1; }

# Apply defaults
: "${TRIGGER:=jacksaas}"
: "${REPEATS:=10}"
: "${BASE_MODEL:=stabilityai/stable-diffusion-xl-base-1.0}"
: "${RESOLUTION:=1024}"
: "${BATCH_SIZE:=1}"
: "${GRAD_ACCUM:=2}"
: "${NETWORK_DIM:=16}"
: "${NETWORK_ALPHA:=16}"
: "${LEARNING_RATE:=1e-4}"
: "${MAX_TRAIN_STEPS:=1500}"
: "${SAVE_EVERY_STEPS:=250}"
: "${MIXED_PRECISION:=fp16}"
: "${OPTIMIZER:=AdamW8bit}"

[ -n "${HF_TOKEN:-}" ]       || fail "HF_TOKEN not set"
[ -n "${HF_DATASET:-}" ]     || fail "HF_DATASET not set"
[ -n "${LORA_REPO_NAME:-}" ] || fail "LORA_REPO_NAME not set"

WORK=/workspace
TRAIN_ROOT=$WORK/training_data
CLASS_DIR=$TRAIN_ROOT/${REPEATS}_${TRIGGER}
OUTPUT_DIR=$WORK/output
OUTPUT_NAME=jack-lora
KOHYA_DIR=$WORK/sd-scripts

mkdir -p "$WORK" "$TRAIN_ROOT" "$OUTPUT_DIR"
cd "$WORK"

step "1/7 Environment summary"
echo "HF_DATASET     = $HF_DATASET"
echo "LORA_REPO_NAME = $LORA_REPO_NAME"
echo "Trigger        = $TRIGGER  (repeats=$REPEATS)"
echo "Hyperparams    = res=$RESOLUTION rank=$NETWORK_DIM steps=$MAX_TRAIN_STEPS lr=$LEARNING_RATE bs=$BATCH_SIZE grad_accum=$GRAD_ACCUM"
nvidia-smi || fail "no GPU visible"

step "2/7 Clone kohya_ss/sd-scripts"
if [ ! -d "$KOHYA_DIR/.git" ]; then
  git clone --depth 1 https://github.com/kohya-ss/sd-scripts.git "$KOHYA_DIR"
fi
cd "$KOHYA_DIR"

step "3/7 Install Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt
pip install \
  xformers==0.0.27 \
  bitsandbytes==0.43.1 \
  accelerate==0.30.1 \
  diffusers==0.27.2 \
  peft==0.10.0 \
  huggingface_hub==0.23.0

step "4/7 Download training dataset from HuggingFace"
python - <<PY
import os, zipfile, shutil, sys
from huggingface_hub import hf_hub_download, login

login(token=os.environ["HF_TOKEN"], add_to_git_credential=False)

class_dir = os.environ["CLASS_DIR"]
if os.path.isdir(class_dir):
    shutil.rmtree(class_dir)
os.makedirs(class_dir, exist_ok=True)

zip_path = hf_hub_download(
    repo_id=os.environ["HF_DATASET"],
    repo_type="dataset",
    filename="jack-training.zip",
    token=os.environ["HF_TOKEN"],
)
with zipfile.ZipFile(zip_path) as zf:
    zf.extractall(class_dir)

imgs = [f for f in os.listdir(class_dir) if f.lower().endswith((".png",".jpg",".jpeg",".webp"))]
txts = [f for f in os.listdir(class_dir) if f.lower().endswith(".txt")]
print(f"Extracted: {len(imgs)} images, {len(txts)} captions")
if len(imgs) < 5:
    print("ERROR: fewer than 5 images — re-check prepare-training step.", file=sys.stderr)
    sys.exit(2)
PY
export CLASS_DIR

step "5/7 Launch training"
accelerate launch --num_cpu_threads_per_process 1 sdxl_train_network.py \
  --pretrained_model_name_or_path="$BASE_MODEL" \
  --train_data_dir="$TRAIN_ROOT" \
  --resolution="${RESOLUTION},${RESOLUTION}" \
  --output_dir="$OUTPUT_DIR" \
  --output_name="$OUTPUT_NAME" \
  --save_model_as=safetensors \
  --network_module=networks.lora \
  --network_dim="$NETWORK_DIM" \
  --network_alpha="$NETWORK_ALPHA" \
  --train_batch_size="$BATCH_SIZE" \
  --gradient_accumulation_steps="$GRAD_ACCUM" \
  --learning_rate="$LEARNING_RATE" \
  --optimizer_type="$OPTIMIZER" \
  --lr_scheduler=cosine_with_restarts \
  --lr_warmup_steps=100 \
  --max_train_steps="$MAX_TRAIN_STEPS" \
  --save_every_n_steps="$SAVE_EVERY_STEPS" \
  --mixed_precision="$MIXED_PRECISION" \
  --save_precision="$MIXED_PRECISION" \
  --xformers \
  --cache_latents \
  --gradient_checkpointing \
  --max_data_loader_n_workers=2 \
  --seed=42

step "6/7 Locate best checkpoint"
FINAL_PATH=$WORK/jack-lora.safetensors
python - <<PY
import glob, re, shutil, os, sys
cands = sorted(glob.glob(os.path.join(os.environ["OUTPUT_DIR"], os.environ["OUTPUT_NAME"] + "*.safetensors")))
if not cands:
    print("ERROR: no .safetensors produced; training likely failed.", file=sys.stderr)
    sys.exit(2)
def step_of(p):
    m = re.search(r"(?:step|-)(\d+)\.safetensors$", p)
    return int(m.group(1)) if m else 10**9
cands.sort(key=step_of)
best = cands[-1]
shutil.copy(best, os.environ["FINAL_PATH"])
for c in cands:
    print(" ", c, f"({os.path.getsize(c)/1e6:.1f} MB)")
print("Selected:", best)
print("Final:   ", os.environ["FINAL_PATH"])
PY
export OUTPUT_DIR OUTPUT_NAME FINAL_PATH

step "7/7 Upload LoRA to HuggingFace"
python - <<PY
import os, sys
from huggingface_hub import create_repo, upload_file

repo_id = os.environ["LORA_REPO_NAME"]
token   = os.environ["HF_TOKEN"]
src     = os.environ["FINAL_PATH"]

create_repo(repo_id=repo_id, repo_type="model", private=True, exist_ok=True, token=token)
upload_file(
    path_or_fileobj=src,
    path_in_repo="jack-lora.safetensors",
    repo_id=repo_id,
    repo_type="model",
    token=token,
)
print("Uploaded:", f"https://huggingface.co/{repo_id}/resolve/main/jack-lora.safetensors")
PY

echo ""
echo "===== TRAINING COMPLETE ====="
echo "LORA_URL=https://huggingface.co/${LORA_REPO_NAME}/resolve/main/jack-lora.safetensors"
echo ""
echo "The orchestrator polls HuggingFace for this file and will terminate the pod."
echo "Pod will idle here until terminated. Do not delete logs."

# Stay alive briefly so the orchestrator sees the upload before the container exits.
# RunPod will preserve logs when terminated externally.
sleep 120
