#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import {
  CANONICAL_OFFICE,
  DEFAULT_REFERENCE_IMAGES,
  OFFICE_AVOID,
  PAW_LOCK,
  ROOT,
  TRAINING_DIR,
  activeCaptionPath,
  activeImagePath,
  buildTrainingImagePrompt,
  loadTrainingPrompts,
  sanitizeCaption,
} from "./lib/jack-training-prompt.mjs";

const data = loadTrainingPrompts();
mkdirSync(TRAINING_DIR, { recursive: true });

const rejectedNames = existsSync(resolve(TRAINING_DIR, "_rejected"))
  ? readdirSync(resolve(TRAINING_DIR, "_rejected"))
  : [];
const reviewNames = existsSync(resolve(TRAINING_DIR, "_generated_review"))
  ? readdirSync(resolve(TRAINING_DIR, "_generated_review"))
  : [];

const lines = [];
lines.push("# Jack LoRA Working Prompts");
lines.push("");
lines.push("Generated from `jack-training-prompts.json` without modifying it.");
lines.push("");
lines.push("## Canonical Locks");
lines.push("");
lines.push("Use these references for generation:");
for (const ref of DEFAULT_REFERENCE_IMAGES) lines.push(`- \`${ref}\``);
lines.push("");
lines.push("Office lock:");
lines.push("");
lines.push(CANONICAL_OFFICE);
lines.push("");
lines.push("Office avoid:");
lines.push("");
lines.push(OFFICE_AVOID);
lines.push("");
lines.push("Paw lock:");
lines.push("");
lines.push(PAW_LOCK);
lines.push("");
lines.push("## Status");
lines.push("");
lines.push("| ID | Active PNG | Active TXT | Review files | Rejected files | Caption |");
lines.push("|---|---:|---:|---:|---:|---|");
for (const entry of data.prompts) {
  const reviewCount = reviewNames.filter((n) => n.startsWith(`${entry.id}_`)).length;
  const rejectedCount = rejectedNames.filter((n) => n.startsWith(`${entry.id}_`)).length;
  lines.push(`| ${entry.id} | ${existsSync(activeImagePath(entry.id)) ? "yes" : "no"} | ${existsSync(activeCaptionPath(entry.id)) ? "yes" : "no"} | ${reviewCount} | ${rejectedCount} | ${sanitizeCaption(entry.lora_caption)} |`);
}
lines.push("");
lines.push("## Work Backwards: 050 to 001");
lines.push("");
for (const entry of [...data.prompts].reverse()) {
  const active = existsSync(activeImagePath(entry.id)) && existsSync(activeCaptionPath(entry.id));
  const target = resolve(TRAINING_DIR, "_generated_review", `${entry.id}_attempt1.png`);
  lines.push(`### ${entry.id}${active ? " - active" : " - needs image"}`);
  lines.push("");
  lines.push(`Caption: \`${sanitizeCaption(entry.lora_caption)}\``);
  lines.push("");
  lines.push("Prompt:");
  lines.push("");
  lines.push("```text");
  lines.push(buildTrainingImagePrompt({ entry, targetPath: target }));
  lines.push("```");
  lines.push("");
}

const out = resolve(TRAINING_DIR, "WORKING_PROMPTS.md");
writeFileSync(out, `${lines.join("\n")}\n`, "utf-8");
console.log(`Wrote ${out.replace(ROOT + "\\", "")}`);
