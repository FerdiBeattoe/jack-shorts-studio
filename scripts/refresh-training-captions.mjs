#!/usr/bin/env node

import { existsSync, writeFileSync } from "node:fs";
import {
  activeCaptionPath,
  activeImagePath,
  loadTrainingPrompts,
  sanitizeCaption,
} from "./lib/jack-training-prompt.mjs";

const data = loadTrainingPrompts();
let written = 0;

for (const entry of data.prompts) {
  if (!existsSync(activeImagePath(entry.id))) continue;
  writeFileSync(activeCaptionPath(entry.id), `${sanitizeCaption(entry.lora_caption)}\n`, "utf-8");
  console.log(`caption refreshed: ${entry.id}.txt`);
  written++;
}

console.log(`Done. Refreshed ${written} active captions.`);
