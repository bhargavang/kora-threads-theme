// Turns the SVGs from build_images.py into JPEGs using your installed Chrome.
//
//   cd tools && npm install
//   python3 build_images.py && node render_images.mjs
//
// Set CHROME_PATH if Chrome isn't in the default macOS location.

import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer-core';

const here = dirname(fileURLToPath(import.meta.url));
const repo = join(here, '..');
const svgDir = join(here, '.build', 'svg');
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// Render at 1.2x so product images come out 1200 x 1500.
const SCALE = 1.2;

const manifest = JSON.parse(await readFile(join(svgDir, 'manifest.json'), 'utf8'));
const browser = await puppeteer.launch({ executablePath: chrome, headless: true });
const page = await browser.newPage();

for (const item of manifest) {
  await page.setViewport({ width: item.width, height: item.height, deviceScaleFactor: SCALE });
  await page.goto(pathToFileURL(join(svgDir, item.svg)).href, { waitUntil: 'load' });
  await page.screenshot({
    path: join(repo, item.jpg),
    type: 'jpeg',
    quality: 82,
    clip: { x: 0, y: 0, width: item.width, height: item.height },
  });
  console.log('wrote', item.jpg);
}

await browser.close();
