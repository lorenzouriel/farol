---
name: thumbnail-prompt
description: Generate an image-generation prompt for a Substack/Medium article thumbnail in the brand's locked visual style, read from the design guide. Use whenever the user pastes or links an article (or its draft/notes) and asks for a thumbnail, cover, header, or "thumb" prompt — even if they don't name the style, since the style is fixed per brand. Outputs a ready-to-paste prompt plus one alternative and the thumbnail-survival tradeoff. Not for generating the image itself, and not for arbitrary unrelated illustration styles.
---

# Thumbnail Prompt (locked-style series)

Turn an article into a single image-generation prompt that matches the brand's established
header style across Substack and Medium. The output is a *prompt*, not an image — paste-ready
for Midjourney / DALL·E / SD.

The whole job is: read the piece → find the one idea → translate it into one gesture →
dress it in the locked style. Consistency across the series matters more than novelty; the
visual signature is what makes the feed recognizable as the author's.

## STEP 0: Load the brand style block

Read `resources/identity/design-guide.md` before composing anything:

1. If it has a **"Thumbnail style"** (or similar illustration-style) section, use that as the
   STYLE BLOCK and its highlight color as the accent hue.
2. If it defines colors/style but no thumbnail style, derive one: highlight color as the single
   accent, main background as the canvas, general-style adjectives as texture/mood tokens. Then
   offer to save the derived block into the design guide so the series stays locked from now on.
3. If the design guide is blank, use the **fallback style** below and tell the user that's what
   you did — one line, don't block.

The style block, wherever it came from, is *locked*: same tokens every thumbnail, never
per-article restyling. Series recognizability beats per-piece novelty.

### Fallback style (used only when the design guide defines none)

```
duotone, single luminous spot color on black, vintage halftone engraving texture,
etched cross-hatching, no smooth gradients, pure black background, conceptual editorial
header, wide banner crop
```

Why each token earns its place (keep the equivalents when writing a brand's own block):
- **single spot color** — one accent = the *idea / knowledge / creation*. Never two competing accents.
- **no smooth gradients** — does real work: stops DALL·E from flattening texture into clean vector, which breaks series consistency. Keep it even when it feels redundant.
- **halftone engraving, etched cross-hatching** — the texture signature. Midjourney renders this natively; DALL·E needs it stated explicitly or it drifts to flat color.
- **solid single-color background** — non-negotiable. Subject and accent float on it.
- **wide banner crop** — the thumbnail has to read in a feed at small size.

### The contrast rule (applies to any brand palette)

Use the brand's highlight hex as the *base* tone for accent elements. But for the **glowing
idea element** (starburst / emitted light / focal point), push the hue brighter and more
saturated than the base so it punches out of the background. A flat mid-tone on a dark
background has low luminance contrast and goes muddy at thumbnail size; the saturated glow is
what keeps the spot color readable. One accent only — don't let the base tone and the glow
read as two separate colors.

## Process

### 1. Find the one idea
Don't summarize the article. Extract the *single* argument it's making — the thesis the reader
should leave with. If the piece has a central tension or reversal (consume vs. create, input vs.
output, fear vs. action, old self vs. new self), that contrast is usually the strongest thumbnail
because it's inherently visual.

### 2. Pick one gesture
Translate the idea into a *single visual gesture* a viewer grasps in under a second. One subject,
one action. The test: could you describe what's happening in the image in one short sentence? If it
needs two, it's too busy and won't survive shrinking to a feed thumbnail.

Recurring vocabulary that fits editorial-header work (mix, don't checklist):
- a **starburst / light source** in the accent color = an idea, insight, knowledge, the "aha"
- a **figure in profile** (human or animal) in a contemplative pose
- **hands** doing something — shaping, building, reaching, holding
- **books / open pages** as the source
- **growth metaphors** — a sprout through stone, a crack, something emerging
- a **human head/brain** in cross-section for input/output or transformation themes

Lean on *active* gestures (building, shaping, reaching, emerging) over passive ones (just reading,
just sitting) when the article is about doing something with knowledge — it distinguishes the
thumbnail from earlier passive ones in the series and matches a "do something" thesis.

### 3. Compose the prompt
Order the prompt the way image models parse best:

```
[subject + the single action], [secondary detail if any], [STYLE BLOCK], [mood/theme].
```

Keep the subject description concrete and physical. State the action explicitly. Put the glowing
accent on the element that represents the idea, not the background.

### 4. Deliver
Give the user:
1. **Primary prompt** — the strongest single gesture, ready to paste.
2. **One alternative** — a different metaphor for the same thesis.
3. **The tradeoff** — one or two sentences on which to pick and why, *always* judged by whether
   it survives shrinking to feed-thumbnail size. Busy / multi-element / fine-detail-dependent
   concepts lose at small scale; name that when it applies.

Keep the framing tight and engineer-to-engineer. No preamble, no restating the article back.


## Model note (mention only if the user asks how to run it)
- **Midjourney** holds texture + duotone styles natively.
- **DALL·E / SD** drift toward clean flat vector — explicit texture tokens (`no smooth gradients`,
  `etched cross-hatching`, or the brand's equivalents) are what hold the look; don't drop them.
- If the model renders the accent too dark or muddy, state "bright glowing [accent color], high
  luminance" — a base mid-tone hex alone reads too flat against a dark background.
