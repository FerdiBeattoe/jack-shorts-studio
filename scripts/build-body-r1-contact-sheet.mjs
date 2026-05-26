#!/usr/bin/env node
import { existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createCanvas, loadImage } from "@napi-rs/canvas";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const STAGING_DIR = resolve(ROOT, "assets/puppet/layers_staging/body_r1");
const OUTPUT_PATH = resolve(STAGING_DIR, "body_r1_contact_sheet.png");

const ASSETS = [
  "jack_torso_front.png",
  "jack_torso_three_quarter.png",
  "jack_arm_left_resting.png",
  "jack_arm_right_resting.png",
  "jack_arm_right_tie_fix.png",
  "jack_tie_straight.png",
];

const REFERENCE_PATH = resolve(
  ROOT,
  "assets/puppet/refs/jack_body_pose_reference_sheet.png",
);

const CELL_W = 360;
const CELL_H = 400;
const HEADER_H = 78;
const LABEL_H = 58;
const COLS = 3;
const ROWS = 2;
const WIDTH = COLS * CELL_W;
const HEIGHT = HEADER_H + ROWS * (CELL_H + LABEL_H);

mkdirSync(STAGING_DIR, { recursive: true });

const canvas = createCanvas(WIDTH, HEIGHT);
const ctx = canvas.getContext("2d");

function drawBackground() {
  ctx.fillStyle = "#f2f2f2";
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  ctx.fillStyle = "#111111";
  ctx.font = "bold 26px sans-serif";
  ctx.fillText("Jack Body R1 Staging Contact Sheet", 24, 34);
  ctx.font = "15px sans-serif";
  ctx.fillStyle = "#333333";
  ctx.fillText("Missing files are shown as placeholders. Review against jack_body_pose_reference_sheet.png.", 24, 58);
}

function drawCheckerboard(x, y, w, h, size = 22) {
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(x, y, w, h);
  for (let row = 0; row < Math.ceil(h / size); row += 1) {
    for (let col = 0; col < Math.ceil(w / size); col += 1) {
      ctx.fillStyle = (row + col) % 2 === 0 ? "#d7d7d7" : "#ffffff";
      ctx.fillRect(x + col * size, y + row * size, size, size);
    }
  }
}

function drawMissingPlaceholder(x, y, w, h, name) {
  ctx.fillStyle = "#efefef";
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "#9a9a9a";
  ctx.setLineDash([12, 10]);
  ctx.lineWidth = 3;
  ctx.strokeRect(x + 14, y + 14, w - 28, h - 28);
  ctx.setLineDash([]);
  ctx.fillStyle = "#555555";
  ctx.font = "bold 24px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("MISSING", x + w / 2, y + h / 2 - 10);
  ctx.font = "14px sans-serif";
  ctx.fillText(name, x + w / 2, y + h / 2 + 18);
  ctx.textAlign = "left";
}

function fitRect(srcW, srcH, maxW, maxH) {
  const scale = Math.min(maxW / srcW, maxH / srcH);
  return {
    w: Math.round(srcW * scale),
    h: Math.round(srcH * scale),
  };
}

async function drawAsset(name, index) {
  const col = index % COLS;
  const row = Math.floor(index / COLS);
  const x = col * CELL_W;
  const y = HEADER_H + row * (CELL_H + LABEL_H);
  const pad = 18;
  const imageX = x + pad;
  const imageY = y + pad;
  const imageW = CELL_W - pad * 2;
  const imageH = CELL_H - pad * 2;
  const assetPath = resolve(STAGING_DIR, name);

  ctx.fillStyle = "#e5e5e5";
  ctx.fillRect(x, y, CELL_W, CELL_H + LABEL_H);
  ctx.strokeStyle = "#c5c5c5";
  ctx.lineWidth = 1;
  ctx.strokeRect(x + 0.5, y + 0.5, CELL_W - 1, CELL_H + LABEL_H - 1);

  if (existsSync(assetPath)) {
    drawCheckerboard(imageX, imageY, imageW, imageH);
    const img = await loadImage(assetPath);
    const fitted = fitRect(img.width, img.height, imageW, imageH);
    const dx = imageX + Math.round((imageW - fitted.w) / 2);
    const dy = imageY + Math.round((imageH - fitted.h) / 2);
    ctx.drawImage(img, dx, dy, fitted.w, fitted.h);
    ctx.fillStyle = "#1f1f1f";
    ctx.font = "14px sans-serif";
    ctx.fillText(`${img.width}x${img.height}`, x + 14, y + CELL_H + 42);
  } else {
    drawMissingPlaceholder(imageX, imageY, imageW, imageH, name);
  }

  ctx.fillStyle = "#111111";
  ctx.font = "bold 15px sans-serif";
  ctx.fillText(name, x + 14, y + CELL_H + 22);
}

drawBackground();
await Promise.all(ASSETS.map(drawAsset));

ctx.fillStyle = "#333333";
ctx.font = "13px sans-serif";
ctx.fillText(`Reference: ${REFERENCE_PATH.replace(ROOT + "\\", "")}`, 24, HEIGHT - 12);

const png = canvas.toBuffer("image/png");
await import("node:fs/promises").then(({ writeFile }) => writeFile(OUTPUT_PATH, png));

console.log(`Wrote ${OUTPUT_PATH}`);
