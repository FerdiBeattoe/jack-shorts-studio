#!/usr/bin/env node
/**
 * check-episode-assets.mjs
 *
 * Checks whether Episode 02 animation clip exports exist on disk.
 * Reports shot completeness, missing clips, and available fallback stills.
 * Warns when any required clip is missing before a render.
 *
 * Usage:
 *   node scripts/check-episode-assets.mjs
 */

import { readFileSync, existsSync, statSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const MANIFEST_PATH = resolve(ROOT, "manifests/jack_episode_02_shot_manifest.json");

// ── Load manifest ──────────────────────────────────────────────────────────

let manifest;
try {
  manifest = JSON.parse(readFileSync(MANIFEST_PATH, "utf-8"));
} catch (err) {
  console.error(`ERROR: Could not read manifest at ${MANIFEST_PATH}`);
  console.error(err.message);
  process.exit(1);
}

const { shots, episode, total_duration_seconds, fps, resolution } = manifest;

// ── Check master audio ─────────────────────────────────────────────────────

const audioPath = resolve(ROOT, manifest.audio_master);
const audioPresent = existsSync(audioPath);
let audioSizeKB = null;
if (audioPresent) {
  audioSizeKB = Math.round(statSync(audioPath).size / 1024);
}

// ── Check each shot ────────────────────────────────────────────────────────

const shotResults = shots.map((shot) => {
  const clipPath = resolve(ROOT, shot.required_clip_path);
  const stillPath = resolve(ROOT, shot.fallback_still);
  const clipPresent = existsSync(clipPath);
  const stillPresent = existsSync(stillPath);

  let clipSizeMB = null;
  if (clipPresent) {
    clipSizeMB = (statSync(clipPath).size / (1024 * 1024)).toFixed(1);
  }

  return {
    ...shot,
    clipPresent,
    stillPresent,
    clipSizeMB,
  };
});

// ── Summary stats ──────────────────────────────────────────────────────────

const clipsPresent = shotResults.filter((s) => s.clipPresent);
const clipsMissing = shotResults.filter((s) => !s.clipPresent);
const stillsPresent = shotResults.filter((s) => s.stillPresent);
const stillsMissing = shotResults.filter((s) => !s.stillPresent);
const readyForAnimatedRender = clipsMissing.length === 0;
const readyForStillsRender = stillsMissing.length === 0;

// ── Print report ───────────────────────────────────────────────────────────

const RESET = "\x1b[0m";
const RED = "\x1b[31m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const CYAN = "\x1b[36m";
const BOLD = "\x1b[1m";
const DIM = "\x1b[2m";

console.log(`\n${BOLD}Episode 02 Asset Check${RESET}`);
console.log(`Episode: ${episode}`);
console.log(`Duration: ${total_duration_seconds}s | FPS: ${fps} | Resolution: ${resolution}`);
console.log(`Manifest: ${MANIFEST_PATH}`);
console.log(`─`.repeat(70));

// Audio
console.log(`\n${BOLD}Master Audio${RESET}`);
if (audioPresent) {
  console.log(`  ${GREEN}✓${RESET} ${manifest.audio_master} (${audioSizeKB} KB)`);
} else {
  console.log(`  ${RED}✗ MISSING:${RESET} ${manifest.audio_master}`);
  console.log(`  ${RED}  Cannot render without audio.${RESET}`);
}

// Shot table
console.log(`\n${BOLD}Shot Status${RESET}`);
console.log(
  `  ${"Shot".padEnd(10)} ${"Duration".padEnd(10)} ${"Clip".padEnd(8)} ${"Still".padEnd(8)} ${"Notes"}`
);
console.log(`  ${"─".repeat(65)}`);

for (const shot of shotResults) {
  const clipStatus = shot.clipPresent
    ? `${GREEN}✓ ready${RESET}`
    : `${RED}✗ miss ${RESET}`;
  const stillStatus = shot.stillPresent
    ? `${GREEN}✓${RESET}`
    : `${RED}✗${RESET}`;
  const sizeInfo = shot.clipPresent ? `(${shot.clipSizeMB} MB)` : "";
  const noteFlag = shot.notes ? `${YELLOW}⚠${RESET}` : " ";

  console.log(
    `  ${shot.shot_id.padEnd(10)} ${`${shot.duration_seconds}s`.padEnd(10)} ${clipStatus} ${stillStatus}        ${noteFlag} ${sizeInfo}`
  );
}

// Completion
console.log(`\n${BOLD}Completeness${RESET}`);
console.log(`  Animation clips: ${clipsPresent.length} / ${shots.length} present`);
console.log(`  Fallback stills: ${stillsPresent.length} / ${shots.length} present`);

// Render readiness
console.log(`\n${BOLD}Render Readiness${RESET}`);
if (readyForAnimatedRender && audioPresent) {
  console.log(`  ${GREEN}${BOLD}READY FOR ANIMATED RENDER.${RESET} All clips and audio present.`);
} else if (readyForStillsRender && audioPresent) {
  console.log(`  ${YELLOW}${BOLD}READY FOR STILLS RENDER.${RESET} Using fallback still images.`);
  console.log(`  ${DIM}Run: pnpm run render${RESET}`);
  if (clipsMissing.length > 0) {
    console.log(`\n  ${YELLOW}Missing animation clips (${clipsMissing.length}):${RESET}`);
    for (const shot of clipsMissing) {
      console.log(`    ${YELLOW}•${RESET} ${shot.shot_id} → ${shot.required_clip_path}`);
      console.log(`      ${DIM}Script: "${shot.script_line}"${RESET}`);
    }
  }
} else {
  console.log(`  ${RED}NOT READY.${RESET} Critical assets missing:`);
  if (!audioPresent) {
    console.log(`    ${RED}✗ Master audio missing${RESET}`);
  }
  for (const shot of stillsMissing) {
    console.log(`    ${RED}✗ Fallback still missing: ${shot.fallback_still}${RESET}`);
  }
}

// Shots with notes
const notedShots = shotResults.filter((s) => s.notes);
if (notedShots.length > 0) {
  console.log(`\n${BOLD}${YELLOW}Warnings${RESET}`);
  for (const shot of notedShots) {
    console.log(`  ${YELLOW}⚠${RESET} ${shot.shot_id}: ${shot.notes}`);
  }
}

// Duration coverage check
const totalCoveredSeconds = shots.reduce(
  (sum, s) => sum + s.duration_seconds,
  0
);
const durationMatch =
  Math.abs(totalCoveredSeconds - total_duration_seconds) < 0.1;
console.log(`\n${BOLD}Timeline Coverage${RESET}`);
if (durationMatch) {
  console.log(
    `  ${GREEN}✓${RESET} Shots cover ${totalCoveredSeconds.toFixed(1)}s / ${total_duration_seconds}s`
  );
} else {
  console.log(
    `  ${YELLOW}⚠${RESET} Shots cover ${totalCoveredSeconds.toFixed(1)}s but manifest total is ${total_duration_seconds}s`
  );
  console.log(`    ${DIM}Check timing.ts for gaps or overlaps.${RESET}`);
}

console.log(`\n${"─".repeat(70)}\n`);

// ── Exit code ──────────────────────────────────────────────────────────────
// Exit 1 only if even the stills render would fail (missing fallbacks or audio)
if (!audioPresent || stillsMissing.length > 0) {
  process.exit(1);
} else {
  process.exit(0);
}
