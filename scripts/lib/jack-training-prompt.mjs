import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
export const ROOT = resolve(__dirname, "..", "..");
export const PROMPTS_PATH = resolve(ROOT, "jack-training-prompts.json");
export const TRAINING_DIR = resolve(ROOT, "assets", "jack-training");
export const REVIEW_DIR = resolve(TRAINING_DIR, "_generated_review");
export const REJECTED_DIR = resolve(TRAINING_DIR, "_rejected");

export const DEFAULT_REFERENCE_IMAGES = [
  "assets/jack-reference.png",
  "assets/jack-training/jack_019.png",
  "assets/jack-training/jack_021.png",
  "assets/jack-training/jack_022.png",
];

export const CANONICAL_OFFICE = `Warm wood executive SaaS office, late afternoon. Dark walnut desk in the foreground. Tall window with golden-hour blinds on camera-left. Warm wooden bookshelf behind Jack on camera-right with books, a small plant, and soft amber lamp glow. Off-white ceramic coffee mug and yellow legal pad may appear on the desk when useful. When a laptop is visible, it must stay in the accepted baseline position: open silver laptop at the lower-right foreground desk edge, angled toward Jack, never moved to camera-left or centered. Keep the desk tone, window/blinds position, bookshelf proportions, amber lighting, laptop placement, and warm office mood consistent with the accepted active LoRA images.`;

export const OFFICE_AVOID = `Avoid teal/open-plan office, flat teal wall, cold grey modern office, wall clock as the main background, globe/fancy library variant, changed bookshelf style, changed window position, blue lighting, sterile corporate room, or generic office drift.`;

export const PAW_LOCK = `Jack has golden retriever paws, not human hands. Visible top/outside paw surfaces must be golden fur only. Brown or darker pad markings belong only on underside/palm pad surfaces when clearly visible. No brown marks on the outside of digits, no dark nail tips, no nail polish appearance. Paws: golden fur on all visible surfaces, brown pad markings only on underside when visible, zero nail-like markings.`;

export const HARDER_PAW_LOCK = `PAWS MUST LOOK LIKE DOG PAWS: smooth golden fur on all visible surfaces. Absolutely zero brown, dark, or nail-like markings on the outside or top of any digit. Paw pads are hidden on the underside unless the underside is clearly visible.`;

export function loadTrainingPrompts() {
  const data = JSON.parse(readFileSync(PROMPTS_PATH, "utf-8"));
  if (!Array.isArray(data.prompts) || data.prompts.length !== 50) {
    throw new Error(`Expected 50 prompts in ${PROMPTS_PATH}`);
  }
  return data;
}

export function normalizeId(raw) {
  const s = String(raw || "").trim();
  const m = s.match(/^(?:jack_)?(\d{1,3})$/i);
  if (!m) throw new Error(`Invalid training id: ${raw}`);
  const n = Number(m[1]);
  if (!Number.isInteger(n) || n < 1 || n > 50) {
    throw new Error(`Training id out of range 1..50: ${raw}`);
  }
  return `jack_${String(n).padStart(3, "0")}`;
}

export function parseIdList(raw) {
  const ids = [];
  for (const part of String(raw || "").split(",")) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    const range = trimmed.match(/^(?:jack_)?(\d{1,3})-(?:jack_)?(\d{1,3})$/i);
    if (range) {
      const start = Number(range[1]);
      const end = Number(range[2]);
      const step = start <= end ? 1 : -1;
      for (let n = start; step > 0 ? n <= end : n >= end; n += step) {
        ids.push(normalizeId(n));
      }
    } else {
      ids.push(normalizeId(trimmed));
    }
  }
  return [...new Set(ids)];
}

export function getPromptEntry(data, id) {
  const normalized = normalizeId(id);
  const entry = data.prompts.find((p) => p.id === normalized);
  if (!entry) throw new Error(`Missing prompt entry for ${normalized}`);
  return entry;
}

export function activeImagePath(id) {
  return resolve(TRAINING_DIR, `${normalizeId(id)}.png`);
}

export function activeCaptionPath(id) {
  return resolve(TRAINING_DIR, `${normalizeId(id)}.txt`);
}

export function sanitizeCaption(caption) {
  return String(caption || "")
    .replace(/\bfingers resting on keys\b/gi, "paws resting on keys")
    .replace(/\bemphatic finger jab forward\b/gi, "emphatic paw point forward")
    .replace(/\bsingle finger pointing\b/gi, "single paw pointing")
    .replace(/\bfinger jabbing\b/gi, "paw pointing")
    .replace(/\bfinger curled\b/gi, "paw curled")
    .replace(/\bfinger\b/gi, "paw digit")
    .replace(/\bfingers\b/gi, "paw digits")
    .replace(/\bhands\b/gi, "paws")
    .replace(/\s+/g, " ")
    .trim();
}

export function section(text, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(`\\[${escaped}[^\\]]*\\]\\s*([\\s\\S]*?)(?=\\n\\s*\\[[^\\]]+\\]|$)`, "i");
  return text.match(re)?.[1]?.trim() || "";
}

export function pawSafeText(text) {
  return String(text || "")
    .replace(/\bfingers resting on keys\b/gi, "paws resting on keys")
    .replace(/\bemphatic finger jab forward\b/gi, "emphatic paw point forward")
    .replace(/\bsingle finger pointing\b/gi, "single paw pointing")
    .replace(/\bfinger jabbing\b/gi, "paw pointing")
    .replace(/\bfinger tense\b/gi, "paw held firm")
    .replace(/\bfinger curled\b/gi, "paw curled")
    .replace(/\bfinger\b/gi, "paw digit")
    .replace(/\bfingers relaxed\b/gi, "paw digits relaxed")
    .replace(/\bfingers spread\b/gi, "paw digits spread")
    .replace(/\bfingers\b/gi, "paw digits")
    .replace(/\bhuman hands\b/gi, "human hands");
}

export function buildTrainingImagePrompt({ entry, targetPath, referenceImages = DEFAULT_REFERENCE_IMAGES, retryHarderPaws = false }) {
  const original = entry.generation_prompt;
  const character = section(original, "CHARACTER") || "";
  const pose = pawSafeText(section(original, "POSE & ACTION FOR THIS STILL") || "");
  const style = section(original, "STYLE") || "";
  const framing = section(original, "FRAMING") || "";
  const pawClause = retryHarderPaws ? `${PAW_LOCK}\n${HARDER_PAW_LOCK}` : PAW_LOCK;
  const direction = directionLock(entry.pose);

  const refs = referenceImages.map((img, index) => {
    if (index === 0) return `Image ${index + 1}: ${img} is the character identity reference. Match Jack exactly.`;
    return `Image ${index + 1}: ${img} is an accepted active LoRA image. Use it as office/lighting/style continuity anchor, not as the pose.`;
  });

  return [
    `Generate one LoRA training image: ${entry.id}. Use the built-in Codex image generation tool with gpt-image-2 behavior.`,
    `Do not use scripts/image_gen.py, do not use the OpenAI SDK directly, and do not require OPENAI_API_KEY.`,
    ``,
    `Input image roles:`,
    ...refs,
    ``,
    `[CANONICAL OFFICE - LOCKED]`,
    CANONICAL_OFFICE,
    OFFICE_AVOID,
    ``,
    `[CHARACTER - LOCKED]`,
    character,
    ``,
    `[POSE & ACTION FOR THIS STILL - ${entry.id}]`,
    direction,
    targetOverride(entry.id),
    pose,
    ``,
    `[PAW ANATOMY - LOCKED]`,
    pawClause,
    ``,
    `[STYLE - LOCKED]`,
    style,
    ``,
    `[FRAMING - LOCKED]`,
    framing,
    ``,
    `[VALIDATION BEFORE SAVE]`,
    `Pass all of these before writing the final file:`,
    `- Golden retriever species, Jack identity, honey fur, floppy ears, amber eyes.`,
    `- Black suit, white shirt, black skinny tie.`,
    `- Warm wood office continuity: left golden blinds/window, right wooden bookshelf, dark desk, amber light.`,
    `- No teal/open-plan office drift and no wrong bookshelf variant.`,
    `- 2D adult-animation cel-shaded illustration with paper-grain texture.`,
    `- 9:16 vertical portrait framing.`,
    `- Correct pose/expression/mouth/paw action for ${entry.id}.`,
    `- Paw check: no brown/dark nail-like markings on outside or top of digits.`,
    ``,
    `[OUTPUT]`,
    `Save the generated PNG to this exact absolute path: ${targetPath}`,
    `Do not write to assets/jack-training/${entry.id}.png directly.`,
    `Do not modify jack-training-prompts.json.`,
    `Do not modify any other file.`,
    `No text, captions, watermarks, logos, or UI overlays in the image.`,
  ].join("\n");
}

function targetOverride(id) {
  switch (id) {
    case "jack_004":
      return "Slot-specific expression lock: this is engaged mid-sentence talking, not tired, sleepy, deadpan, bored, or exasperated. Eyes must look alive and present, eyebrows neutral, mouth half open mid-word, with open explanatory paw gestures.";
    case "jack_005":
      return "Slot-specific expression lock: this is confident lecture mode, not tired, sleepy, deadpan, bored, or smug. Eyes must be direct and alert, eyelids open enough to read as engaged, brow slightly raised, mouth only slightly open as if calmly explaining.";
    default:
      return "";
  }
}

function directionLock(pose) {
  switch (pose) {
    case "profile_left":
      return "Orientation lock: Jack is in full left profile. His nose and muzzle point toward the camera-left edge of the image. We see the left side of his face. Do not face camera-right.";
    case "profile_right":
      return "Orientation lock: Jack is in full right profile. His nose and muzzle point toward the camera-right edge of the image. We see the right side of his face. Do not face camera-left.";
    case "three_quarter_left":
      return "Orientation lock: Jack is turned three-quarters toward camera-left. Do not mirror him into camera-right.";
    case "three_quarter_right":
      return "Orientation lock: Jack is turned three-quarters toward camera-right. Do not mirror him into camera-left.";
    default:
      return "";
  }
}

export function existingReferenceImages(images = DEFAULT_REFERENCE_IMAGES) {
  return images.map((p) => resolve(ROOT, p)).filter((p) => existsSync(p));
}

export function parseArgs(argv) {
  const out = {};
  for (const arg of argv) {
    if (!arg.startsWith("--")) continue;
    const eq = arg.indexOf("=");
    if (eq === -1) out[arg.slice(2)] = true;
    else out[arg.slice(2, eq)] = arg.slice(eq + 1);
  }
  return out;
}
