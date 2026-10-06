---
name: linkedin-thumbnail
description: Generate a brand-consistent thumbnail for a LinkedIn article, newsletter issue, or link preview. For Claude Code only. Activate when the user asks for a LinkedIn cover image, article header, or link preview image. Reads the article/post, designs a scene that visually represents the content's core idea, then runs generate.js to call Google's Gemini image API.
---

# LinkedIn Thumbnail Skill (Claude Code)

Generate brand-consistent cover images for LinkedIn articles, newsletters, and link previews.

> **This skill is designed for Claude Code only.** It uses Bash to invoke `generate.js`. Claude Desktop cannot drive this skill.

## When to use this skill

Activate when the user:

- Pastes or links a LinkedIn article and asks for a cover image
- Says "make a LinkedIn thumbnail", "article header", "newsletter cover for LinkedIn"
- Wants a link preview image when sharing an external URL on LinkedIn

Don't use for animated content, Stories, or carousel slides.

## Canvas Specifications

| Format | Size | Ratio | Use |
|--------|------|-------|-----|
| Article / newsletter cover | **1200×627 px** | 1.91:1 | Header image on LinkedIn articles and Substack cross-posts |
| Link preview (OG image) | **1200×627 px** | 1.91:1 | Auto-pulled when sharing a URL in a LinkedIn post |
| Safe zone | **1128×600 px** | — | Keep critical elements (face, logo, key text) inside this inner boundary |

**Always generate at 1200×627 px.** The platform crops to 1128×600 px on some displays — no critical element should live in the outer 36 px margin.

## Prerequisites

1. **Gemini API key** with billing enabled — stored in `.env` (`GOOGLE_AI_API_KEY=...`) in the cwd, OR exported in shell rc.
2. **`generate.js` in the cwd** — the zero-dependency Node script that ships with this skill.
3. **Node.js 18+** installed.
4. **BRAND BLOCK filled in below** — every `[FILL IN ...]` marker replaced.

If the BRAND BLOCK still has `[FILL IN]` markers, stop and tell the user to edit this SKILL.md first.

---

## BRAND BLOCK

> Replace each `[FILL IN ...]` placeholder with your own details. This is the source of truth for every LinkedIn thumbnail. Only change it when your brand visual identity changes.

### Characters

**Primary character description:**
[FILL IN — Describe in 1-3 sentences. Include: gender/age range, distinctive physical features, what they're wearing or carrying, and the rendering style (flat illustration, editorial photography style, etc.)]

**Secondary character (optional):**
[FILL IN — Or leave blank.]

**Reference image paths:**
- Primary character ref: `[FILL IN — absolute path]`
- Secondary character ref: `[FILL IN — absolute path or leave blank]`
- Style anchor: `[FILL IN — an image that exemplifies your desired illustration/photo style]`

### Output

**Aspect ratio:** `1.91:1`
**Pixel size:** `1200×627`
**Output directory:** `[FILL IN — absolute path, e.g. /Users/you/Pictures/linkedin-thumbnails/]`

### Composition policies

**Illustration style:**
[FILL IN — Concrete visual style. E.g., "Clean editorial flat illustration, medium line weight, muted professional palette (navy, slate, warm white), no photorealism."]

**Background policy:**
[FILL IN — E.g., "Solid off-white (#F5F5F0) or a subtle gradient that references the article's domain. No busy environments — readability first."]

**Element count:**
[FILL IN — E.g., "3 max — primary figure + 1 domain prop + optional light text label."]

**Environment policy:**
[FILL IN — E.g., "Minimal or abstract. A hint of context is fine; full-scene environments are not."]

**Text in image:**
[FILL IN — LinkedIn readers skim. Text in image is optional but allowed. E.g., "Article title or a key 2-4 word takeaway phrase, set in a clean sans-serif. Never more than 6 words."]

**Prop selection style:**
[FILL IN — E.g., "Domain-native objects that professionals in the field would immediately recognize."]

**Banned visual elements:**
[FILL IN — E.g., "No stock-photo clichés (handshakes, generic lightbulbs, magnifying glasses). No political symbols. No competitor logos."]

**LinkedIn-specific rules (always apply):**
- Image must read clearly at 300 px wide (feed thumbnail preview size)
- Color palette must convey **credibility**: professional blue, slate, warm neutral, or brand palette. Avoid saturated neons.
- If text is included, it must be legible at 300 px wide — minimum apparent font size of ~24 px at full resolution
- Horizontal format is mandatory (1.91:1) — portrait elements should anchor left or center, leaving right-side breathing room
- Safe zone: all key content within 1128×600 px inset (no critical elements touching the outer 36 px border)

---

## Workflow

### Step 1 — Read the article/content

Identify:
- **Core finding**: the one insight or argument. Not the topic — the *conclusion*. ("Async teams ship 40% faster when they write decisions down" is a finding; "remote work" is a topic.)
- **Tone**: authoritative, analytical, provocative, storytelling, how-to, etc.
- **Concrete domain objects**: things that visually belong to this industry/topic. Finance → charts, ledgers. Engineering → diagrams, terminals. Leadership → teams, org charts.

### Step 2 — Design the scene per BRAND BLOCK policies

Output a single scene plan that respects the LinkedIn safe zone and credibility-first composition:

```
SCENE PLAN
- Core finding (1 sentence): ...
- Composition: <horizontal layout, left-right balance, where primary figure/element sits>
- Key prop: <one specific object that enacts the finding — per brand prop style>
- Text overlay (if used): <exact words, max 6, placement, typography notes>
- Action / state: <what the figure or elements ARE DOING that conveys the finding>
- Safe zone check: <confirm no critical element in outer 36 px margin>
- Why this works: <one sentence connecting the visual to the article's core finding>
```

### Step 3 — Confirm with user

Show the SCENE PLAN. Ask if they want to proceed or iterate. If the article has multiple angles, offer 2-3 SCENE PLAN variants for the user to choose before any image is generated — text iteration is free.

### Step 4 — Generate via Bash

```bash
node generate.js \
  --prompt="<full prompt with scene description + LinkedIn constraints>" \
  --refs="<primary ref>,<secondary ref>,<style anchor>" \
  --output="<output_directory>/<article-slug>-YYYY-MM-DD.png"
```

For multiple variants, run sequentially with different `--output` filenames (`-v1.png`, `-v2.png`). Never parallel — avoid rate limits.

On success, the script prints `OK: <output_path>`.

### Step 5 — Review the output

Check against these gates:

- ✓/✗ Canvas is 1200×627 px?
- ✓/✗ Critical elements inside 1128×600 px safe zone?
- ✓/✗ Readable at 300 px wide (feed preview)?
- ✓/✗ Color palette conveys professional credibility?
- ✓/✗ Text (if present) legible at small size — max 6 words?
- ✓/✗ No banned elements?
- ✓/✗ Brand policies honored?

### Step 6 — Iterate via edit

```bash
node generate.js \
  --input="<previous output>" \
  --prompt="<edit instructions: what to change AND what to preserve>" \
  --output="<new output path>"
```

Always state what to PRESERVE. Editing preserves style/composition consistency.

---

## Universal best practices for LinkedIn thumbnails

1. **Horizontal rule.** LinkedIn is a desktop-first feed. 1.91:1 is not optional. Any portrait subject should be placed left-of-center, with negative space to the right for visual breathing room or text.

2. **300 px legibility test.** Before confirming a scene plan, mentally squint — would the key visual element and any text still read at 300 px wide? If the prop requires detail to be understood, it's the wrong prop.

3. **Credibility palette over attention-grabbing neons.** LinkedIn audiences trust muted, professional colors. High-saturation palettes read as ads and get scrolled past. Exception: a single high-contrast accent color to direct the eye is fine.

4. **Props must argue the finding, not illustrate the topic.** A rising arrow argues growth; a wilting plant argues stagnation. Don't pick a prop that merely belongs to the topic — pick one that *shows the conclusion*.

5. **Safe zone is non-negotiable.** LinkedIn crops article headers differently across desktop, mobile, and notification email. The 1128×600 px safe zone is the guaranteed visible area across all contexts.

6. **Text should ADD, not DUPLICATE.** If the title is already in the article header, the image text should be a supporting phrase — not the same words. If no text is needed, omit it.

---

## PROMPT TEMPLATE

```
Generate a single illustrated frame in the EXACT style of the reference images, featuring the EXACT characters from the references.

LinkedIn article cover image — 1200×627 px, 1.91:1 horizontal format.

Scene to render:
<your scene description from Step 2>

Style and constraints (violating any = wrong output):
- Illustration style: <BRAND illustration_style>
- Background: <BRAND background_policy>
- Aspect ratio: 1.91:1 horizontal — this is MANDATORY
- Safe zone: all critical elements within the central 1128×600 px — nothing important in the outer 36 px margin
- Primary character must look identical to the first reference image
- <Secondary character identical to second reference — only if applicable>
- Match the style anchor's line weights, palette, and shading exactly
- Text in image: <BRAND text_in_image policy — exact words if text is used>
- Element count: stay within <BRAND element_count>
- Color palette must convey professional credibility — no neons, no overly saturated colors
- Banned elements: <BRAND banned_elements>
- Must read clearly when displayed at 300 px wide
```

---

## Common pitfalls

1. **Portrait composition sneaking into a horizontal canvas.** Gemini sometimes centers a tall figure and leaves awkward horizontal bands. If the composition feels like a portrait image on a widescreen canvas, edit: "Rebalance the composition to fill the horizontal 1.91:1 frame. Place [subject] left-of-center with [prop or abstract fill] to the right."

2. **Over-saturated palette.** Even with explicit "muted professional" rules, Gemini sometimes produces vivid colors. Edit: "Desaturate the color palette. Shift toward [slate/navy/warm neutral]. Keep the composition unchanged."

3. **Text bleed-through.** Gemini adds text to screens, papers, labels even when not requested. Edit: "Remove all text, letters, and numbers. Replace with abstract texture or blank surface. Keep everything else identical."

4. **Safe zone violation.** Key element ends up in the outer margin. Edit: "Move [element] inward — it must sit within the central 1128×600 px area. Keep all other elements unchanged."

5. **Generic metaphor props.** Lightbulbs, handshakes, gears, magnifying glasses — these are LinkedIn clichés. If Gemini generates one, redirect: "Replace the [cliché prop] with [domain-native object from the article]. Keep everything else identical."

---

## Cost notes

Each `generate.js` call is one Gemini API call. Check current per-image pricing at https://ai.google.dev/gemini-api/docs/pricing before quoting costs — rates change by model and over time.

Text-only scene plan iteration is free. Only image generation and edits cost API credits. Let the user decide how many variants to generate.
