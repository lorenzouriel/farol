---
name: x-thumbnail
description: Generate a brand-consistent thumbnail for an X (Twitter) post — either an in-stream image attached to a tweet or a link card preview image. For Claude Code only. Activate when the user asks for an X thumbnail, tweet image, or link card image. Reads the post/content, designs a scene optimized for the X feed, then runs generate.js to call Google's Gemini image API.
---

# X Thumbnail Skill (Claude Code)

Generate brand-consistent still images for X posts — in-stream attached images and link card previews.

> **This skill is designed for Claude Code only.** It uses Bash to invoke `generate.js`. Claude Desktop cannot drive this skill.

## When to use this skill

Activate when the user:

- Asks for an image to attach to an X post or thread
- Says "make an X thumbnail", "tweet image", "image for my X post", "link card for X"
- Needs a visual to accompany a post that links to an article or external resource

Don't use for video thumbnails, animated GIFs, or X profile/banner images.

## Canvas Specifications

| Format | Size | Ratio | Use |
|--------|------|-------|-----|
| In-stream image (recommended) | **1200×675 px** | 16:9 | Standard attached image; displayed inline in feed |
| Summary card with large image | **1200×628 px** | 1.91:1 | OG/meta image pulled when sharing a URL |
| In-stream square (optional) | **1080×1080 px** | 1:1 | When square framing serves the concept |
| Feed display size | ~**504×284 px** | 16:9 | Actual render size in desktop feed — all legibility must pass at this size |
| Mobile display size | ~**375×211 px** | 16:9 | Mobile feed render — the critical legibility floor |

**Default to 1200×675 px (16:9).** This fills the most feed space on desktop and mobile. Use 1:1 only when the concept specifically demands it.

**X displays images at roughly 40% of full resolution in the feed.** A 1200×675 px image renders at approximately 504×284 px on desktop and 375×211 px on mobile. Every legibility check must be done at ~375 px wide.

**Dark mode.** X supports system dark mode. Images with very light backgrounds that rely on a white frame will appear on a dark UI. Test that the image works against both light and dark feed backgrounds — avoid thin-bordered white-on-white designs.

## Prerequisites

1. **Gemini API key** with billing enabled — stored in `.env` (`GOOGLE_AI_API_KEY=...`) in the cwd, OR exported in shell rc.
2. **`generate.js` in the cwd** — the zero-dependency Node script that ships with this skill.
3. **Node.js 18+** installed.
4. **BRAND BLOCK filled in below** — every `[FILL IN ...]` marker replaced.

If the BRAND BLOCK still has `[FILL IN]` markers, stop and tell the user to edit this SKILL.md first.

---

## BRAND BLOCK

> Replace each `[FILL IN ...]` placeholder. This is the source of truth for every X thumbnail. Only change it when your brand visual identity changes.

### Characters

**Primary character description:**
[FILL IN — Describe in 1-3 sentences. Include: gender/age range, distinctive physical features, what they're wearing, rendering style (flat illustration, editorial, bold graphic, etc.)]

**Secondary character (optional):**
[FILL IN — Or leave blank.]

**Reference image paths:**
- Primary character ref: `[FILL IN — absolute path]`
- Secondary character ref: `[FILL IN — absolute path or leave blank]`
- Style anchor: `[FILL IN — an image that exemplifies your desired visual style]`

### Output

**Default aspect ratio:** `16:9`
**Default pixel size:** `1200×675`
**Square override:** `1080×1080` (use only when concept requires it)
**Output directory:** `[FILL IN — absolute path, e.g. /Users/you/Pictures/x-thumbnails/]`

### Composition policies

**Illustration / visual style:**
[FILL IN — Be specific. E.g., "Bold flat illustration, heavy outlines, punchy two-tone palette (black + one accent color), high contrast. Optimized for clarity at small sizes."]

**Background policy:**
[FILL IN — E.g., "Solid brand color or high-contrast two-tone split. Must work against both light and dark feed backgrounds — avoid designs that disappear on dark mode."]

**Element count:**
[FILL IN — E.g., "2 max — one strong focal element + minimal or no text overlay. X feeds move fast; simplicity wins."]

**Environment policy:**
[FILL IN — E.g., "Abstract or minimal. No detailed scene backgrounds that distract from the focal element."]

**Text in image:**
[FILL IN — X audience reads the post caption; image text should be punchy and additive. E.g., "0-3 words maximum. Bold, high-contrast. Used only when the text punch IS the image (e.g., a bold stat or a single provocative word). Never duplicate the tweet text."]

**Prop selection style:**
[FILL IN — E.g., "Instantly recognizable icons — objects that read in under 0.3 seconds at 375 px wide. Prefer silhouettes and bold shapes over detailed textures."]

**Banned visual elements:**
[FILL IN — E.g., "No competing brand logos. No subtle textures that compress poorly. No text-heavy images."]

**X-specific rules (always apply):**
- All critical elements must be legible at **375 px wide** (mobile feed width)
- Image must work against both **light and dark** X feed backgrounds — avoid designs that rely on a white frame or border
- High contrast is mandatory — X's image compression is aggressive; low-contrast images become muddy at small size
- Text overlay (if used): maximum 3 words, bold, minimum apparent font size of 28px at full resolution
- Avoid fine detail, thin lines, and subtle gradients — they disappear at mobile display size
- No margins or padding that waste screen real estate — the image frame IS the canvas

---

## Workflow

### Step 1 — Read the post / content

Identify:
- **Core message**: what is the tweet saying? What is the ONE idea the image should amplify?
- **Tone**: hot take, data/insight, personal story, humor, provocation, announcement.
- **Domain objects**: concrete visual elements that belong to this topic at a glance.

### Step 2 — Design the scene per BRAND BLOCK policies

X images must have immediate visual impact. The composition should work as a standalone image even without reading the tweet:

```
SCENE PLAN
- Post message (1 sentence): ...
- Format: <16:9 / 1:1 — and why>
- Composition: <one-sentence visual layout; where the focal element sits>
- Key element: <the one bold visual that carries the message>
- Text overlay (if used): <exact 1-3 words, placement, typography>
- Action / state: <what the image IS doing that amplifies the tweet>
- Dark mode check: <will this image read clearly on both light and dark backgrounds?>
- 375 px legibility check: <what must still read at mobile display size?>
```

### Step 3 — Confirm with user

Show the SCENE PLAN. Offer 2-3 variants if the tweet has multiple angles. Text iteration is free.

### Step 4 — Generate via Bash

```bash
node generate.js \
  --prompt="<full prompt with scene + X constraints>" \
  --refs="<primary ref>,<secondary ref>,<style anchor>" \
  --output="<output_directory>/<post-slug>-YYYY-MM-DD.png"
```

For multiple variants, run sequentially with different `--output` filenames.

### Step 5 — Review the output

Check:
- ✓/✗ Correct canvas (1200×675 or 1080×1080)?
- ✓/✗ Reads at 375 px wide (mobile legibility)?
- ✓/✗ Works on both light and dark feed backgrounds?
- ✓/✗ High contrast between elements?
- ✓/✗ Text (if used): max 3 words, bold, legible at small size?
- ✓/✗ Brand style honored?
- ✓/✗ No banned elements?

### Step 6 — Iterate via edit

```bash
node generate.js \
  --input="<previous output>" \
  --prompt="<what to change AND what to preserve>" \
  --output="<new output path>"
```

---

## Universal best practices for X thumbnails

1. **375 px is the floor.** X shows images at roughly 375 px wide on mobile — the dominant platform context for X consumption. Every visual choice must survive that compression. Run a mental squint test on the scene plan: would the focal element and any text still read clearly as a 375 px thumbnail?

2. **Dark mode is not optional.** A significant portion of X users use dark mode. An image with a white or very light background that relies on contrast against that background will look washed out in dark mode. Design with a defined, solid background color — not white — or ensure the subject has sufficient contrast against any background color.

3. **X is a fast-scroll context.** Twitter/X engagement windows are measured in milliseconds. The image must transmit a single clear message instantly. Two elements competing for attention will lose to a single bold element that owns the frame.

4. **Text in image is a power move — use it rarely.** Most high-performing X images with text use 1-3 words that create tension or punch with the tweet. Sentence-length image text is a newsletter behavior, not an X behavior.

5. **Compression kills subtlety.** X compresses images aggressively. Thin borders, subtle shadows, gentle gradients, fine textures — these all degrade. Design bold. Thick lines, solid fills, clear shapes.

6. **The image should ADD, not repeat.** If the tweet already says the thing, the image should show it — visually, emotionally, not textually. An image that just shows the words of the tweet in fancy typography is wasted real estate.

---

## PROMPT TEMPLATE

```
Generate a single illustrated frame in the EXACT style of the reference images, featuring the EXACT characters from the references.

X (Twitter) post image — [1200×675 px / 1080×1080 px] [16:9 / 1:1] format.

Scene to render:
<your scene description from Step 2>

Style and constraints (violating any = wrong output):
- Illustration style: <BRAND illustration_style>
- Background: <BRAND background_policy> — must work on both light AND dark UI backgrounds
- Aspect ratio: [16:9 / 1:1] — this is MANDATORY
- Primary character must look identical to the first reference image
- <Secondary character identical to second reference — only if applicable>
- Match the style anchor's line weights, palette, and shading exactly
- Text in image: <BRAND text_in_image policy — exact words if text is used>
- Element count: stay within <BRAND element_count>
- High contrast between all elements — image will be compressed and displayed at 375 px wide on mobile
- No thin lines, fine textures, or subtle gradients — these disappear at small size
- Banned elements: <BRAND banned_elements>
```

---

## Common pitfalls

1. **Image disappears on dark mode.** If the background is light gray or white, the image blends into the light feed and vanishes entirely in dark mode. Edit: "Change the background to [solid dark/brand color]. Keep all other elements unchanged."

2. **Too much detail at full size — nothing reads at 375 px.** Edit: "Simplify [element]. Remove [fine detail]. Make the focal element bolder and larger relative to the frame. Keep the composition concept unchanged."

3. **Text too long or too small.** Edit: "Replace the text overlay with just '[1-3 words]'. Make it bold, high-contrast. Must be legible when the image is displayed at 375 px wide."

4. **Wrong aspect ratio.** State it twice in the prompt if Gemini ignores it.

5. **Busy composition with two competing focal points.** X images need one clear visual winner. Edit: "Remove [secondary element]. The focal point is [primary element]. Background should be [solid fill]. Keep everything else identical."

---

## Cost notes

Each `generate.js` call is one Gemini API call. Check current per-image pricing at https://ai.google.dev/gemini-api/docs/pricing — rates vary by model.

Text scene plan iteration is free. Image generation and edits cost API credits. The user decides how many variants to generate.
