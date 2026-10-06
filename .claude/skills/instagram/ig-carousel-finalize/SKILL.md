---
name: ig-carousel-finalize
description: >
  Finalizes an approved Instagram carousel: builds a PDF from the rendered slide images,
  then strips the folder down to images only (deletes the HTML, render scripts, node_modules,
  and text files). Use after a carousel is approved, or when the user says "finalize carousel",
  "carousel to PDF", "clean the carousel folder", "carousel approved", or "export carousel PDF".
---

# Carousel Finalize

Post-processing companion to the `ig-carousel` skill. Once a carousel is approved, this turns
the working folder into a clean deliverable: **a `carousel.pdf` plus the slide images, nothing else.**

> Destructive. It deletes files. Always confirm the target folder and show the deletion list
> before removing anything. Build the PDF FIRST (cleanup removes the tooling it needs).

---

## What it keeps vs. deletes

| Keep | Delete |
|---|---|
| All image files (`.png .jpg .jpeg .webp .gif`) anywhere in the folder | `carousel.html`, `render.js`, any `.js` |
| The generated `carousel.pdf` | `node_modules/`, `package*.json`, `.env` |
| | `copy.md`, `caption*.md`, any `.md` |
| | any other non-image file |

Net result: slide images (e.g. `instagram/slide-01.png …`) + `carousel.pdf`.

---

## Inputs

- **Target folder** — the carousel output folder produced by `ig-carousel`
  (e.g. `areas/marketing/content/<type>-<theme>-<date>/`). If the user doesn't name one, list the
  carousel folders and ask, or offer the most recent.
- **PDF source** — the `instagram/` slide PNGs in filename order. If there's no `instagram/`
  subfolder, fall back to slide PNGs at the folder root.

---

## Workflow

### 1. Locate + confirm
Identify the target folder. Show its contents and state exactly what will be kept and deleted.
**Get explicit confirmation before any deletion.**

### 2. Build the PDF (before cleanup)
Write a disposable `_carousel-pdf.js` into the folder and run it. It reads the slide images in
order, auto-detects the slide size from the first PNG, and writes `carousel.pdf` at the folder root.

```javascript
// _carousel-pdf.js — slide PNGs -> single PDF (one slide per page)
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const SRC = process.argv[2] || 'instagram';   // folder holding slide images
const OUT = process.argv[3] || 'carousel.pdf';

function pngSize(buf) {
  if (buf.length > 24 && buf[0] === 0x89 && buf[1] === 0x50) {
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  }
  return null;
}

(async () => {
  const dir = fs.existsSync(SRC) ? SRC : '.';
  const files = fs.readdirSync(dir)
    .filter(f => /\.(png|jpe?g)$/i.test(f))
    .sort();
  if (!files.length) { console.error('No slide images found in ' + dir); process.exit(1); }

  const first = fs.readFileSync(path.join(dir, files[0]));
  const size = pngSize(first) || { w: 1080, h: 1350 };

  const imgs = files.map(f => {
    const b64 = fs.readFileSync(path.join(dir, f)).toString('base64');
    const mime = f.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
    return `<img src="data:${mime};base64,${b64}">`;
  }).join('\n');

  const html = `<!doctype html><html><head><style>
    @page { size: ${size.w}px ${size.h}px; margin: 0; }
    * { margin: 0; padding: 0; }
    img { display: block; width: ${size.w}px; height: ${size.h}px; page-break-after: always; }
    img:last-child { page-break-after: auto; }
  </style></head><body>${imgs}</body></html>`;

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.pdf({ path: OUT, width: `${size.w}px`, height: `${size.h}px`, printBackground: true });
  await browser.close();
  console.log(`PDF created: ${OUT} (${files.length} pages, ${size.w}x${size.h})`);
})();
```

Run it, reusing Playwright from wherever the carousel's `node_modules` lives (same pattern as
`render.js`):

```bash
# from inside the carousel folder
NODE_PATH="<folder-with-node_modules>/node_modules" node _carousel-pdf.js instagram carousel.pdf
```

**Fallbacks if Playwright isn't reachable:**
```bash
# ImageMagick
magick instagram/slide-*.png carousel.pdf
# Python + Pillow
python -c "from PIL import Image,glob; im=[Image.open(f).convert('RGB') for f in sorted(glob.glob('instagram/slide-*.png'))]; im[0].save('carousel.pdf',save_all=True,append_images=im[1:])"
```

Verify `carousel.pdf` exists and has the right page count before moving on.

### 3. Clean the folder
Delete everything except image files and the PDF.

**PowerShell** (run from inside the carousel folder):
```powershell
Remove-Item -Recurse -Force .\node_modules -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File | Where-Object { $_.Extension -notmatch '(?i)\.(png|jpg|jpeg|webp|gif|pdf)$' } | Remove-Item -Force
Get-ChildItem -Recurse -Directory | Where-Object { @(Get-ChildItem $_.FullName -Recurse -File).Count -eq 0 } | Remove-Item -Recurse -Force
```

**Bash:**
```bash
rm -rf node_modules
find . -type f ! -iregex '.*\.\(png\|jpg\|jpeg\|webp\|gif\|pdf\)' -delete
find . -type d -empty -delete
```

### 4. Report
Show the final folder tree (images + `carousel.pdf`) and the PDF path.

---

## Rules

- Never delete before the PDF is confirmed created.
- Never delete before showing the keep/delete list and getting confirmation.
- Operate only on the single target folder — never recurse into sibling carousel folders.
- Keep every image file regardless of subfolder (`instagram/`, `tiktok/`, source photos all survive).
- The disposable `_carousel-pdf.js` is itself deleted by step 3 — that's intended.
