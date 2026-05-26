import { createCanvas, loadImage } from '@napi-rs/canvas';
import fs from 'node:fs/promises';
import path from 'node:path';

const datasetRoot = process.argv[2] ?? 'assets/lora_training/jack_office_v1';
const mode = process.argv[3] ?? 'all';

const root = path.resolve(datasetRoot);
const outputDir = path.join(root, 'contact_sheets');
await fs.mkdir(outputDir, { recursive: true });

const folders =
  mode === 'sources'
    ? ['source_references']
    : mode === 'accepted'
      ? ['images']
      : ['source_references', 'images'];

const files = [];
for (const folder of folders) {
  const dir = path.join(root, folder);
  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile() && /\.(png|jpg|jpeg|webp)$/i.test(entry.name)) {
        files.push({ folder, name: entry.name, fullPath: path.join(dir, entry.name) });
      }
    }
  } catch {
    // Missing folders should not fail the sheet. This lets us run before generation.
  }
}

files.sort((a, b) => `${a.folder}/${a.name}`.localeCompare(`${b.folder}/${b.name}`));

const cellW = 360;
const cellH = 300;
const labelH = 44;
const padding = 18;
const cols = 3;
const rows = Math.max(1, Math.ceil(files.length / cols));

const canvas = createCanvas(cols * cellW + padding * 2, rows * (cellH + labelH) + padding * 2);
const ctx = canvas.getContext('2d');

ctx.fillStyle = '#202124';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.font = '18px Arial';
ctx.textBaseline = 'top';

if (files.length === 0) {
  ctx.fillStyle = '#f4f1e8';
  ctx.fillText('No images found yet.', padding, padding);
} else {
  for (const [index, file] of files.entries()) {
    const col = index % cols;
    const row = Math.floor(index / cols);
    const x = padding + col * cellW;
    const y = padding + row * (cellH + labelH);

    ctx.fillStyle = '#2d2f33';
    ctx.fillRect(x, y, cellW - 12, cellH + labelH - 12);

    ctx.fillStyle = '#f4f1e8';
    ctx.fillText(`${file.folder}/${file.name}`, x + 12, y + 10, cellW - 36);

    try {
      const image = await loadImage(file.fullPath);
      const maxW = cellW - 28;
      const maxH = cellH - 24;
      const scale = Math.min(maxW / image.width, maxH / image.height);
      const w = image.width * scale;
      const h = image.height * scale;
      const ix = x + (cellW - 12 - w) / 2;
      const iy = y + labelH + (cellH - h) / 2;
      ctx.drawImage(image, ix, iy, w, h);
    } catch (error) {
      ctx.fillStyle = '#ffb4a8';
      ctx.fillText(`Could not load: ${error.message}`, x + 12, y + labelH + 12, cellW - 36);
    }
  }
}

const out = path.join(outputDir, `${mode}_contact_sheet.png`);
await fs.writeFile(out, canvas.toBuffer('image/png'));
console.log(out);
