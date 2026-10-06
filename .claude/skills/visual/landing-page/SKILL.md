---
name: landing-page
description: "Generates a premium, conversion-focused single-page HTML landing page in the company's own brand identity, with a modular section library (nav, hero, social proof, features, how-it-works, stats, testimonials, pricing, FAQ, footer), GSAP scroll animation, 3D mouse-parallax, fluid responsive typography, and a full SEO/accessibility baseline. Use whenever the user says 'create a landing page', 'build a landing page', 'make a landing page for X', 'I need a web page for Y', or provides product/service details and wants a polished website. Also triggers on 'promotional page', 'product page', 'one-pager', 'web presence', 'sales page', 'product launch page', or any standalone visual HTML page. Always use this skill rather than generating HTML ad hoc — it applies the brand system, conversion structure, and animation stack that make the result genuinely professional."
---

# Landing Page Generator

Produces a polished, **conversion-focused**, self-contained HTML landing page **in the
company's own brand**. One brief in, one production-quality `.html` file out.

Three layers make it professional, not just pretty:
1. **Brand-adaptive design system** — colors, fonts, and shape language come from the brand.
2. **Conversion structure** — a modular section library assembled for the offer, with one job: move the visitor to a single primary action.
3. **Technical baseline** — SEO/OG meta, accessibility, responsive fluid type, reduced-motion support.

---

## Step 0 — Load the brand (do this first)

Read `resources/identity/design-guide.md` and map it to design tokens. This is what makes every page
look like *the client*, not a template.

| Token | From design-guide | Fallback (premium dark) |
|---|---|---|
| `--bg` | Main background | `#0A1628` |
| `--bg-alt` | Alternative background / cards | `#0D1F38` |
| `--surface` | Card background | `rgba(255,255,255,0.04)` |
| `--border` | Borders | `rgba(255,255,255,0.12)` |
| `--text` | Main text | `#F7F7F2` |
| `--text-muted` | — (derive at ~68% opacity) | `rgba(247,247,242,0.68)` |
| `--accent` | Highlight / CTA color | `#00D4AA` |
| `--accent-2` | Secondary accent (optional) | `#F5A623` |
| `--radius` | Card border radius | `12px` |
| `--font-display` | Titles font | `Inter`, 700–800 |
| `--font-body` | Body font | `Inter`, 400–500 |

Rules:
- If the design-guide is blank or missing, use the fallback palette (don't stop to run `/install`).
- **Honor the "forbidden color" / "what to NEVER do"** entries — never emit them.
- If the brand is **monochromatic / no accent color**, drop the accent glows and use tonal
  contrast (a lighter/darker shade of the text color) for CTAs and dividers instead.
- Load the brand fonts from Google Fonts with `preconnect` + `display=swap`. If a font isn't
  on Google Fonts, fall back to the nearest system stack and note it.
- Use the brand **logo** (from the design-guide) in the nav and footer when a path exists.

Define every token as a CSS custom property on `:root` and reference tokens everywhere — no
hardcoded hex in components.

---

## Step 1 — Extract content + plan the conversion

Pull these from the prompt/brief (invent compelling, on-brand values when missing):

| Field | What to extract |
|---|---|
| Product / offer name | The thing being promoted |
| One-line value prop | What it does + for whom, ≤12 words |
| Hero headline | Outcome-led, ≤8 words |
| Hero subtext | 1–2 sentences, the promise |
| Primary CTA | One action, repeated (e.g. "Start free", "Book a call") |
| Features / benefits | 3–6, each title + one benefit-led sentence |
| Proof | Logos, testimonials, metrics, or credentials |
| Steps | How it works, 3–4 steps (if relevant) |
| Pricing | Tiers (if relevant) |
| FAQ | 3–6 real objections + answers |

**Conversion rules (apply throughout):**
- **One primary CTA**, same label everywhere. Secondary actions are visually quieter.
- Lead with the **outcome/benefit**, not features. Specifics beat adjectives.
- Message hierarchy: a visitor must grasp *what / for whom / why now* in the first screen.
- Place proof immediately after the hero to cover the credibility gap before asking.
- Follow `memory/preferences.md` for voice. No hype, no corporate filler, no invented stats.

---

## Step 2 — Assemble sections

Pick from the library based on the brief. **Hero, one proof element, and a closing CTA are
mandatory.** Add the rest when the content supports them — never pad with empty sections.

Recommended order:
`Nav → Hero → Social proof (logos) → Features → How-it-works → Stats → Testimonials → Pricing → FAQ → Closing CTA → Footer`

### Section library

**1. Sticky nav** — fixed top bar, transparent over hero, gains `--bg` + subtle bottom
border after scrolling ~80px. Left: logo. Right: 2–4 anchor links + the primary CTA button.
Collapses to a simple menu under 720px.

**2. Hero** — full viewport (`min-height: 100svh`), centered. Eyebrow (accent, caps) →
H1 → subtext → primary CTA (+ optional quiet secondary) → scroll indicator. Behind it, two
parallax shape layers for depth (see Animation). For monochromatic brands, use a soft
radial vignette instead of colored shapes.

**3. Social proof / logo strip** — "Trusted by" caps label + a row of muted logos (or
client/credential names as styled text if no logos). Keep it understated.

**4. Features** — section headline + optional subtext + a grid of cards (3-col default,
2-col for exactly 4 items, 1-col mobile). Card = inline geometric SVG icon (accent stroke) +
title + benefit sentence. Hover: lift + border brighten.

**5. How-it-works** — 3–4 numbered steps, horizontal on desktop / stacked on mobile, with a
connecting line. Each step: number, title, one sentence.

**6. Stats band** — full-width strip, 3–4 big numbers that count up on scroll, each with a
short label.

**7. Testimonials** — 1–3 quote cards: quote, name, role/company, optional avatar circle.
Only use real quotes from the brief; never fabricate attributed quotes.

**8. Pricing** — 2–3 tier cards; highlight the recommended tier (accent border + badge).
Each: name, price, short line, feature list, CTA. Monthly only unless told otherwise.

**9. FAQ** — accordion of 3–6 items; first can be open. Smooth height transition,
accessible (`<button aria-expanded>`).

**10. Closing CTA** — full-width, restated headline + subtext + the primary CTA, with an
ambient accent glow behind the button (skip the glow for monochromatic brands).

**11. Footer** — logo, short tagline, link columns, copyright. Muted, smaller type.

---

## Design system

### Fluid type scale (use `clamp()` — never fixed px for headings)
```css
:root {
  --step-eyebrow: 0.8rem;
  --step-body:    clamp(1rem, 0.95rem + 0.3vw, 1.125rem);
  --step-h3:      clamp(1.25rem, 1.1rem + 0.6vw, 1.5rem);
  --step-h2:      clamp(2rem, 1.5rem + 2vw, 3.25rem);
  --step-h1:      clamp(2.75rem, 1.8rem + 4.5vw, 5rem);
  /* spacing */
  --space-section: clamp(72px, 8vw, 130px);
  --maxw: 1140px;
}
```

### Components
- **Button (primary):** `--accent` bg, contrast text, `--radius`, `padding: 16px 42px`,
  weight 700, transition on bg + `translateY(-2px)` hover, visible `:focus-visible` outline.
- **Button (secondary):** transparent, `1px solid --border`, `--text`.
- **Card:** `--surface` bg, `1px solid --border`, `--radius`, generous padding, hover lift.
- Section wrapper: `padding: var(--space-section) 24px;` inner `max-width: var(--maxw); margin: 0 auto;`.

---

## Animation stack

Include GSAP only (no other libs):
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
```

**Wrap all motion in a reduced-motion guard:**
```javascript
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduce) {
  gsap.registerPlugin(ScrollTrigger);
  // ... all animations below
}
```
When reduced motion is on, everything must be visible at rest (no opacity:0 left behind).

- **Hero entrance:** `gsap.set()` initial hidden state, then a staggered timeline
  (eyebrow → title → subtext → CTA → indicator), `power3.out`.
- **Mouse parallax:** two hero shape layers drift at different speeds from the cursor, plus a
  subtle same-direction drift on `.hero-content` (camera-pan feel).
- **Scroll reveals:** feature/testimonial/pricing cards rise with a slight `rotateX` tilt,
  `stagger`, `toggleActions: "play none none reverse"`.
- **Stat count-up:** animate numbers on scroll into view.
- **Nav:** toggle solid background class past 80px scroll.
- **Ambient float:** decorative shapes use CSS keyframes (cheaper/smoother than JS).

(The detailed hero-timeline, parallax, and card-reveal snippets from the classic premium
template still apply — reuse them, just driven by the brand tokens.)

---

## Technical baseline (always include)

`<head>`:
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[Product] — [value prop]</title>
<meta name="description" content="[≤155 chars]">
<meta property="og:title" content="[Product]">
<meta property="og:description" content="[value prop]">
<meta property="og:type" content="website">
<meta name="theme-color" content="[--bg]">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```
- Semantic HTML: `<nav> <header> <main> <section> <footer>`, one `<h1>`, logical heading order.
- Every decorative shape `aria-hidden="true"`; every image has `alt`.
- Visible `:focus-visible` styles on all interactive elements; anchor links scroll smoothly.
- `<html lang>` set to the workspace language.
- `overflow-x: hidden` on body; never cause horizontal scroll on mobile.

---

## Output

1. Write the complete HTML in a single pass — all CSS in `<style>`, all JS in `<script>`.
   Only external calls: Google Fonts + cdnjs GSAP.
2. Save to: `resources/documents/landing-pages/<product-name-kebab>-landing.html`
   (create the folder if needed). **File naming:** kebab-case from the product name —
   "Quill AI" → `quill-ai-landing.html`.
3. Open it / give the user the path to preview.

### Pre-delivery quality gate (verify before handing off)
- [ ] Brand: colors + fonts come from `resources/identity/design-guide.md`; no forbidden color used.
- [ ] One primary CTA, identical label, repeated (hero + nav + closing).
- [ ] Hero communicates what / for whom / why in the first screen.
- [ ] At least one proof element directly after the hero.
- [ ] Responsive at 1440 / 768 / 375 — no overflow, readable type, grids collapse.
- [ ] `prefers-reduced-motion` respected; nothing stuck invisible.
- [ ] `<head>` has title, description, OG tags; one `<h1>`; images have alt.
- [ ] Self-contained (only Fonts + GSAP external); saved to the correct path.
