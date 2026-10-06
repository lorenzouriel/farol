---
name: ig-thumbnail
description: Generate a brand-consistent still thumbnail (cover image) for an Instagram feed post, carousel cover, or Reel thumbnail. For Claude Code only. Activate when the user asks for an Instagram cover, feed image, carousel first slide, or Reel thumbnail. Reads the content brief, designs a scene optimized for the Instagram scroll, then runs generate.js to call Google's Gemini image API.
---

# Instagram Thumbnail Skill (Claude Code)

Generate brand-consistent still thumbnails and cover images for Instagram — feed posts, carousel covers, and Reel thumbnails.

> **This skill is designed for Claude Code only.** It uses Bash to invoke `generate.js`. Claude Desktop cannot drive this skill.

## When to use this skill

Activate when the user:

- Asks for a feed image, carousel cover, or Reel thumbnail
- Says "make an Instagram thumbnail", "cover image for Instagram", "first slide of the carousel"
- Needs a static visual to anchor a post or Reel

Don't use for full carousel sequences (each slide), animated content, or Stories (ephemeral content that shouldn't use limited API quota on thumbnails).

## Canvas Specifications

| Format | Size | Ratio | Use |
|--------|------|-------|-----|
| Feed portrait **(recommended)** | **1080×1350 px** | 4:5 | Most screen real estate in the feed; highest engagement format |
| Feed square | **1080×1080 px** | 1:1 | Grid-first designs; when square framing serves the concept |
| Reel thumbnail | **1080×1920 px** | 9:16 | Reel cover frame shown before playback |
| Grid safe zone (portrait posts) | **1080×1080 px center** | 1:1 | Profile grid crops portrait posts to square — critical elements must sit in the center 1080×1080 px |

**Default to 1080×1350 px (4:5).** It takes more vertical feed space and typically drives higher reach. Only use 1:1 when the concept specifically requires square framing.

**Grid safe zone is mandatory for 4:5 posts.** Instagram's profile grid shows a 1:1 crop of every post. Anything outside the central 1080×1080 px will be cropped on the grid. No critical elements (face, key prop, logo, text) should live outside that zone.

## Prerequisites

1. **Gemini API key** with billing enabled — stored in `.env` (`GOOGLE_AI_API_KEY=...`) in the cwd, OR exported in shell rc.
2. **`generate.js` in the cwd** — the zero-dependency Node script that ships with this skill.
3. **Node.js 18+** installed.
4. **BRAND BLOCK filled in below** — every `[FILL IN ...]` marker replaced.

If the BRAND BLOCK still has `[FILL IN]` markers, stop and tell the user to edit this SKILL.md first.

---

## BRAND BLOCK

> Replace each `[FILL IN ...]` placeholder. This is the source of truth for every Instagram thumbnail. Only change it when your brand visual identity changes.

### Characters

**Primary character description:**
[FILL IN — Describe in 1-3 sentences. Include: gender/age range, distinctive physical features, what they're wearing, rendering style (flat illustration, bold graphic, photo-realistic, etc.)]

**Secondary character (optional):**
[FILL IN — Or leave blank.]

**Reference image paths:**
- Primary character ref: `[FILL IN — absolute path]`
- Secondary character ref: `[FILL IN — absolute path or leave blank]`
- Style anchor: `[FILL IN — an image that exemplifies your desired visual style and mood]`

### Output

**Default aspect ratio:** `4:5`
**Default pixel size:** `1080×1350`
**Square override:** `1080×1080` (use only when concept requires it)
**Reel thumbnail override:** `1080×1920`
**Output directory:** `[FILL IN — absolute path, e.g. /Users/you/Pictures/instagram-thumbnails/]`

### Composition policies

**Illustration / visual style:**
[FILL IN — Be specific. E.g., "Bold, high-contrast flat illustration with thick outlines, vibrant palette (coral, teal, off-white), zero photorealism. Energy matches a fashion editorial."]

**Background policy:**
[FILL IN — E.g., "Solid brand color or a simple two-tone split. No busy environments — the figure must pop instantly in the feed scroll."]

**Element count:**
[FILL IN — E.g., "2-3 max — primary figure + 1 bold prop + optional minimal text."]

**Environment policy:**
[FILL IN — E.g., "Minimal abstract or solid. Avoid detailed scene-setting backgrounds that compete with the figure."]

**Text in image:**
[FILL IN — Instagram audiences scan fast. E.g., "One bold 1-3 word hook overlaid in the upper or lower third. Font must match brand typeface. Avoid full sentences."]

**Prop selection style:**
[FILL IN — E.g., "Bold iconic objects — instantly recognizable at a glance, no detail needed. Prefer shapes over textures."]

**Banned visual elements:**
[FILL IN — E.g., "No stock photography aesthetics. No competitor logos. No busy patterns that reduce legibility."]

**Instagram-specific rules (always apply):**
- For 4:5 posts: all critical elements (face, key prop, any text, logo) must sit within the **central 1080×1080 px square** — the profile grid crops everything outside this
- Image must stop the scroll — the first visual impression within 0.3 seconds must communicate the brand and the content hook
- Color contrast ratio between subject and background must be high enough to read as a thumbnail at 293×293 px (profile grid display size)
- Text (if used): maximum 3 words, bold weight, must be legible at 293×293 px
- Avoid flat, low-contrast images — Instagram's feed compression reduces subtle gradients

---

## Workflow

### Step 1 — Read the content brief

Identify:
- **Hook / core message**: what is this post trying to say in the first 0.3 seconds? What emotion or curiosity should it trigger?
- **Target emotion**: stop-scroll energy type — curiosity, inspiration, shock, aspiration, humor, relatability.
- **Domain objects**: visual elements that belong to this niche. Fitness → weights, movement lines. Business → charts, milestones. Food → ingredients, plating.

### Step 2 — Design the scene per BRAND BLOCK policies

Output a single scene plan. For 4:5 posts, explicitly verify the grid safe zone:

```
SCENE PLAN
- Content hook (1 sentence): ...
- Format: <4:5 / 1:1 / 9:16 — and why>
- Composition: <where the primary subject sits, what fills the frame, how the eye moves>
- Key prop: <one bold object that communicates the hook in 0.3 seconds>
- Text overlay (if used): <exact 1-3 words, position (upper/lower third), typography notes>
- Action / state: <what is happening in this frozen moment>
- Grid safe zone check: <confirm all critical elements within central 1080×1080 px for 4:5 posts>
- Stop-scroll assessment: <what makes this image arrest the thumb in the first 0.3 seconds>
```

### Step 3 — Confirm with user

Show the SCENE PLAN. Offer 2-3 variants if the content has multiple angles. Text iteration is free — only image generation costs API credits.

### Step 4 — Generate via Bash

```bash
node generate.js \
  --prompt="<full prompt with scene + Instagram constraints>" \
  --refs="<primary ref>,<secondary ref>,<style anchor>" \
  --output="<output_directory>/<post-slug>-YYYY-MM-DD.png"
```

For multiple variants, run sequentially with different `--output` filenames.

### Step 5 — Review the output

Check:
- ✓/✗ Correct canvas size (1080×1350, 1080×1080, or 1080×1920)?
- ✓/✗ For 4:5: all critical elements inside central 1080×1080 px safe zone?
- ✓/✗ Passes the scroll-stop test? (Strong contrast, immediate visual clarity)
- ✓/✗ Legible at 293×293 px profile grid size?
- ✓/✗ Text (if used): max 3 words, legible at small size?
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

## Universal best practices for Instagram thumbnails

1. **The 0.3-second rule.** Instagram feed moves fast. The image must communicate brand + hook within 0.3 seconds. A viewer who has to look twice to understand what they're seeing will scroll. One strong focal point, one bold color, one immediate idea.

2. **Grid safe zone is not optional.** Profile grids matter for first impressions when someone visits the account. Any 4:5 or Reel post that has critical content outside the center square will look broken on the grid. Design the center square first, extend outward.

3. **High contrast saves compressed images.** Instagram compresses images heavily. Low-contrast compositions lose depth. Design with at least 3:1 contrast between subject and background. Avoid subtle gradients as a primary design element — they become muddy in feed.

4. **Portrait beats square for reach.** 4:5 takes more feed space = more exposure per scroll. Only use 1:1 when the composition genuinely benefits from square framing.

5. **The prop must arrest, not explain.** Instagram is visual-first. The prop should trigger a gut reaction — curiosity, surprise, aspiration — before the viewer reads any text. A prop that requires context to understand is the wrong prop for a thumbnail.

6. **Minimal text, maximum weight.** If text appears in the image, it must be readable at 293 px wide. That means 3 words maximum, bold weight, high contrast. Use text to amplify an emotion, not to explain the post.

---

## PROMPT TEMPLATE

```
Generate a single illustrated frame in the EXACT style of the reference images, featuring the EXACT characters from the references.

Instagram thumbnail — [1080×1350 px / 1080×1080 px / 1080×1920 px] [4:5 / 1:1 / 9:16] format.

Scene to render:
<your scene description from Step 2>

Style and constraints (violating any = wrong output):
- Illustration style: <BRAND illustration_style>
- Background: <BRAND background_policy>
- Aspect ratio: [4:5 / 1:1 / 9:16] — this is MANDATORY
- Grid safe zone (4:5 posts only): all critical elements within the central 1080×1080 px square
- Primary character must look identical to the first reference image
- <Secondary character identical to second reference — only if applicable>
- Match the style anchor's line weights, palette, and shading exactly
- Text in image: <BRAND text_in_image policy — exact words if text is used>
- Element count: stay within <BRAND element_count>
- High contrast between subject and background — must read clearly at 293 px wide
- Banned elements: <BRAND banned_elements>
```

---

## Common pitfalls

1. **Critical element outside grid safe zone.** For 4:5 posts, Gemini sometimes places the face or key text near the top or bottom of the 1350 px height, where the grid crops it. Edit: "Move [element] into the central 1080×1080 px area. Keep all other composition unchanged."

2. **Low contrast background.** Pastel or gradient backgrounds that look good at full size become muddy in feed at 293 px. Edit: "Increase contrast between [subject] and background. Shift background to [solid color]. Keep everything else identical."

3. **Text too small or too long.** Gemini sometimes renders sentence-length text. Edit: "Replace the text with just the words '[max 3 words]'. Make it bold and legible at 293 px wide. Keep everything else identical."

4. **Wrong aspect ratio.** State the ratio twice in the prompt if Gemini ignores it.

5. **Busy background competing with subject.** Environment details that seemed subtle at full resolution become visual noise at thumbnail size. Edit: "Simplify the background to [solid color / abstract wash]. Keep the subject and prop unchanged."

---

## Cost notes

Each `generate.js` call is one Gemini API call. Check current per-image pricing at https://ai.google.dev/gemini-api/docs/pricing — rates vary by model.

Text scene plan iteration is free. Image generation and edits cost API credits. The user decides how many variants to generate.
