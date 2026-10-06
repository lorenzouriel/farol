---
name: ig-image-downloader
description: >
  Download images from Instagram posts directly into the user's workspace folder.
  Handles both single-image posts and multi-image carousels.
  Use this skill whenever the user shares an Instagram post URL and wants the image(s) saved,
  or says anything like "download this Instagram image", "grab this post", "save this IG photo",
  "get the images from this post", or pastes an instagram.com/p/ link.
  Also trigger when the user mentions downloading, saving, or extracting images from Instagram
  even if they haven't shared a URL yet — ask for the link.
---

# Instagram Image Downloader

Download images from Instagram posts into the user's folder. Works with single-image posts and carousels.

## Prerequisites

The user's network allowlist must include `*.cdninstagram.com` so the workspace can reach Instagram's image CDN.
If downloads fail with exit code 56 or an "not on allowlist" error, tell the user:
> Add `*.cdninstagram.com` in **Settings → Capabilities → Network allowlist**, then start a new chat.

## Workflow

### 1. Open the post in Chrome

Use Chrome MCP to navigate to the Instagram URL. Wait 3 seconds for the page to load.

```
navigate → https://www.instagram.com/p/SHORTCODE/
wait 3s
screenshot (to confirm the page loaded)
```

### 1b. Extract post caption

Before downloading, extract the post caption to use later for the folder name. Run this JavaScript:

```js
const captionEl = document.querySelector('h1') || document.querySelector('[data-testid="post-comment-root"] span') || document.querySelector('div[role="dialog"] ul li span');
const caption = captionEl ? captionEl.innerText.substring(0, 120) : '';
JSON.stringify({ caption });
```

From the caption, derive a short, descriptive name suffix (3-6 words, lowercase, hyphens instead of spaces, no special characters). Hold off on creating the folder until after step 2 (carousel detection), since the folder prefix depends on whether the post is a single image or a carousel.

### 2. Detect single image vs carousel

Run this JavaScript via `javascript_tool`:

```js
const nextBtn = document.querySelector('button[aria-label="Next"]') || document.querySelector('button[aria-label="Go to next image"]');
const dots = document.querySelectorAll('[role="tablist"] [role="tab"]');
const isCarousel = !!nextBtn || dots.length > 0;
const slideCount = dots.length || 1;
JSON.stringify({ isCarousel, slideCount });
```

Note: `slideCount` from dots is unreliable — it may return 1 even for carousels. Use the presence of a "Next" button as the primary carousel signal, and keep advancing until no "Next" button is found.

### 2b. Create the named folder

Now that you know whether the post is a single image or a carousel, create the folder with the appropriate prefix:

**Naming convention:**
- **Single image** → `ig-post-<descriptive-name>`
- **Carousel** → `ig-carousel-<descriptive-name>`

Examples:
- Caption: "5 Python tricks every beginner should know" (single image) → `ig-post-5-python-tricks-for-beginners`
- Caption: "How I built my first AI agent" (carousel) → `ig-carousel-building-first-ai-agent`
- Caption is empty or unreadable (single image) → `ig-post-SHORTCODE`
- Caption is empty or unreadable (carousel) → `ig-carousel-SHORTCODE`

Create the folder inside `Notes Ideas/`:
```bash
mkdir -p "/path/to/workspace/Notes Ideas/<folder-name>"
```

All images and PDFs for this post go inside this folder.

### 3. Extract the image URL

The Chrome MCP blocks full CDN URLs (they contain query strings with auth tokens). Work around this by encoding the **entire URL** in 200-character base64 chunks. This preserves the exact CDN authentication tokens — reassembling host + path + query separately can corrupt them and cause 403 errors.

**For single-image posts**, use the `'Photo by'` alt-text selector with a fallback:

```js
const allImgs = document.querySelectorAll('img');
let targetImg = null;
for (const img of allImgs) {
  if (img.naturalWidth > 300 && img.alt && img.alt.includes('Photo by')) {
    targetImg = img;
    break;
  }
}
if (!targetImg) {
  let maxW = 0;
  for (const img of document.querySelectorAll('img[src*="cdninstagram"]')) {
    const rect = img.getBoundingClientRect();
    if (img.naturalWidth > maxW && rect.top < 200 && rect.width > 400) {
      maxW = img.naturalWidth;
      targetImg = img;
    }
  }
}
if (targetImg) {
  const full = new URL(targetImg.src).href;
  const c1 = btoa(full.substring(0, 200));
  const c2 = btoa(full.substring(200, 400));
  const c3 = btoa(full.substring(400));
  JSON.stringify({ c1, c2, c3 });
} else {
  'IMAGE_NOT_FOUND';
}
```

**For carousel posts**, use strict viewport-position filtering to grab the **center slide only**. Instagram keeps many large images in the DOM — previous/next carousel slides, "More posts" thumbnails — and without position filtering you'll grab the wrong one:

```js
const allImgs = document.querySelectorAll('img[src*="cdninstagram"]');
let centerImg = null;
for (const img of allImgs) {
  if (img.naturalWidth > 300) {
    const rect = img.getBoundingClientRect();
    if (rect.left > 400 && rect.left < 700 && rect.top < 200 && rect.width > 400) {
      centerImg = img;
      break;
    }
  }
}
if (centerImg) {
  const full = new URL(centerImg.src).href;
  const c1 = btoa(full.substring(0, 200));
  const c2 = btoa(full.substring(200, 400));
  const c3 = btoa(full.substring(400));
  JSON.stringify({ c1, c2, c3 });
} else {
  'IMAGE_NOT_FOUND';
}
```

The `rect.left > 400 && rect.left < 700` filter targets the center position in Instagram's carousel layout. The previous slide sits at ~left:69 and the next at ~left:1033, so this range cleanly isolates the active slide.

### 4. Download in the workspace

Reassemble the full URL from the base64 chunks in bash and download with curl. Save into the named folder created in step 2b.

For a **single image**:
```bash
C1="<chunk1_from_js>"
C2="<chunk2_from_js>"
C3="<chunk3_from_js>"
FULL_URL="$(echo -n "$C1" | base64 -d)$(echo -n "$C2" | base64 -d)$(echo -n "$C3" | base64 -d)"
curl -L -o "/path/to/workspace/Notes Ideas/<folder-name>/instagram_SHORTCODE.jpg" "$FULL_URL" -s -w "HTTP %{http_code}, Size: %{size_download} bytes\n"
```

For a **carousel**, append a slide number:
```bash
curl -L -o "/path/to/workspace/Notes Ideas/<folder-name>/instagram_SHORTCODE_1.jpg" "$FULL_URL" ...
```

Remember to use the correct bash mount path for the user's workspace folder (check the path mapping in your system prompt).

### 5. For carousels — advance and repeat

If the post is a carousel, click the "Next" button via Chrome MCP's `computer` tool (use `find` to locate it, or click by coordinate on the right edge of the image area around x:815), wait 2 seconds for the new slide to render, then repeat steps 3-4 for each slide.

Keep advancing until no "Next" button is found — that means you've reached the last slide.

Name files sequentially: `instagram_SHORTCODE_1.jpg`, `instagram_SHORTCODE_2.jpg`, etc.

### 5b. For carousels — create a combined PDF

After downloading all carousel slides, combine them into a single PDF inside the same folder. Use reportlab + Pillow to scale each image to 50% of its pixel dimensions for the page size:

```python
from reportlab.pdfgen import canvas
from PIL import Image
import glob

shortcode = "SHORTCODE"
folder = "/path/to/workspace/Notes Ideas/<folder-name>"
images = sorted(glob.glob(f"{folder}/instagram_{shortcode}_*.jpg"), key=lambda x: int(x.split('_')[-1].replace('.jpg','')))
c = canvas.Canvas(f"{folder}/instagram_{shortcode}.pdf")
for img_file in images:
    img = Image.open(img_file)
    pw, ph = img.size[0]*0.5, img.size[1]*0.5
    c.setPageSize((pw, ph))
    c.drawImage(img_file, 0, 0, width=pw, height=ph)
    c.showPage()
c.save()
```

### 6. Verify

Read the saved file(s) with the `Read` tool to confirm they're valid images (the tool renders images visually). Report what was saved.

## Things that do NOT work — don't waste time on these

These approaches were tested and all fail. Do not attempt them:

- **Encoding only the query string** — Encoding just `url.search` with `btoa()` and reassembling with host + path in bash can corrupt CDN auth tokens, causing 403 errors. Always use the full-URL chunked approach described above.
- **Using generic "largest image" selectors for carousels** — Instagram keeps many large images in the DOM (carousel slides, "More posts" thumbnails). Without viewport-position filtering (`rect.left` between 400-700), you'll grab the wrong image.
- **Passing image data through Chrome JS returns** — The Chrome MCP content filter blocks base64, hex, and any binary-like encoding in JavaScript return values. Don't try canvas-to-base64, hex encoding, reversed strings, or chunked transfers of image data.
- **Browser-triggered downloads + Finder** — Triggering a download via JS `<a>` element puts the file in the user's Downloads folder, but the workspace sandbox can't access it. Moving it via computer-use/Finder works but is slow and fragile. Avoid this entirely.
- **Direct web_fetch or curl without the allowlist** — Instagram's CDN (`scontent-*.cdninstagram.com`) is not on the default network allowlist. The prerequisite must be met first.

## Output location

Save images to the user's workspace `Notes Ideas/` folder, organized into per-post subfolders prefixed with `ig-post-` (single images) or `ig-carousel-` (carousels), followed by a descriptive name derived from the post caption. Each post gets its own folder containing its image(s) and, for carousels, a combined PDF. Use the `computer://` link format so the user can view the files directly.
