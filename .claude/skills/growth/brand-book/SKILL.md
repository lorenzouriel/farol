---
name: brand-book
description: Assembles everything the user has created inside resources/identity/ (design guide, logos, photos, assets) into a professional, shareable brand guidelines PDF — the kind designers hand off to clients, freelancers, and agencies. Trigger on "brand book", "brand guidelines PDF", "brand PDF", "share my brand", "export brand identity", "brand kit for designers".
version: 1.0.0
category: marketing-growth
---

# Brand Book — Shareable Brand Guidelines PDF

You are a brand designer producing a hand-off document. The user has brand material scattered in their workspace — maybe a filled design guide, maybe just a folder of photos and a logo. Your job: collect it, organize it, and lay it out as a polished multi-page PDF that an outside designer, freelancer, or partner can work from without asking questions.

This skill does NOT invent a brand. If the identity doesn't exist yet, route to `growth/brand-identity` first. This skill packages what exists.

---

## STEP 1: Inventory the identity folder

Scan `resources/identity/` recursively and classify everything:

| Type | Detect by | Used for |
|------|-----------|----------|
| Design guide | `design-guide.md` | Colors, typography, style rules, logo paths, do-nots |
| Logos | filename contains `logo`, or SVG files | Logo section (primary, dark-background, icon variants) |
| Photos / imagery | `.jpg`, `.jpeg`, `.png`, `.webp` not classified as logo | Imagery-style section |
| Fonts | `.ttf`, `.otf`, `.woff2` | Typography specimens (load via `@font-face`) |
| Other docs | `.md`, `.pdf`, `.txt` | Extra guidelines to fold in |

Also gather context (silently, per CompanyOS rules):
- `memory/company.md` → mission, what the business does (brand story page)
- `memory/preferences.md` → tone of voice, writing style (voice & tone page)
- `resources/marketing-growth/` → prior `brand-identity` report, if any
- `areas/marketing/` → 2–4 recent visuals (carousels, thumbnails) as real application examples

Print a short inventory to the user before building: what was found, what's missing.

## STEP 2: Fill gaps — extract, don't interrogate

- **Colors missing** (design guide blank): extract the dominant palette from the logo and photos with Python (Pillow: quantize to 5–6 colors, drop near-white/near-black, present hex values). Confirm with the user in ONE message: "I extracted these colors from your assets: … Use them?"
- **Typography missing**: if font files exist, use them. Otherwise ask for the font names once; if unknown, state in the PDF "Typography: to be defined" rather than inventing.
- **Voice missing**: derive 3–4 tone adjectives from `memory/preferences.md`. If empty, skip the page.
- **Logo missing**: skip logo pages, list it under "Gaps" on the final page.

Never block on a gap. Build with what exists; every gap becomes one line on the final "What's still missing" page so the brand book itself doubles as a to-do list.

## STEP 3: Build the book as paged HTML

Create `resources/documents/brand/brand-book.html`. One file, one `<section class="page">` per PDF page:

```css
@page { size: A4 landscape; margin: 0; }
.page {
  width: 297mm; height: 210mm;
  page-break-after: always;
  box-sizing: border-box; padding: 18mm;
  position: relative; overflow: hidden;
}
```

**The book must be styled with the brand it documents** — its colors, its fonts (embed local font files via `@font-face` with absolute `file:///` paths, Google-font fallback only if named in the design guide). A brand book in default Helvetica with blue links is a failed deliverable.

Page order (include only pages with real material):

1. **Cover** — logo centered, "Brand Guidelines", company name, month/year, brand background color
2. **Contents** — numbered sections
3. **Brand story** — mission / what the company does / values (from memory)
4. **Logo** — primary on light and dark swatches; variants side by side; clear-space diagram (padding = logo-mark height); minimum size
5. **Logo don'ts** — 4–6 crossed-out miniatures: stretched, recolored, shadowed, busy background
6. **Colors** — large swatches with name, HEX, RGB, and role (background / highlight / text / forbidden). Forbidden colors get their own clearly marked row
7. **Typography** — specimen per font: full alphabet, weights, and a type scale (H1/H2/body/caption) with sizes
8. **Imagery** — grid of the user's actual photos (3–6, `object-fit: cover`), one line describing the common style (lighting, subject, mood)
9. **Voice & tone** — tone spectrum, 3 do/don't copy pairs written in the brand's actual voice
10. **Applications** — real examples pulled from `areas/marketing/` (screenshots/exports of posts, carousels)
11. **What's still missing** — the gap list from Step 2 (omit if none)
12. **Back cover** — logo small, contact line, "vX.Y — {date}"

Layout rules: generous whitespace, one idea per page, footer on every inner page (`{Company} Brand Guidelines — p. N`), no emoji, no decorative clip-art. Reference all images with absolute `file:///` paths so headless rendering resolves them.

## STEP 4: Render to PDF

Render with headless Chrome/Edge (Edge always present on Windows):

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu ^
  --print-to-pdf="{workspace}\output\documents\brand\brand-book.pdf" ^
  --no-pdf-header-footer "file:///{workspace}/resources/documents/brand/brand-book.html"
```

(macOS/Linux: use `google-chrome`/`chromium` with the same flags.) If no Chromium browser is available, fall back to Python `weasyprint`; only if that also fails, build directly with `reportlab` per `formats/pdf`.

**Verify before declaring done**: open the PDF (or convert page 1–2 to images) and check — page count matches sections, images actually rendered (not broken), fonts applied, nothing overflows its page. Fix and re-render if not.

## STEP 5: Deliver

Report to the user:
- Path: `resources/documents/brand/brand-book.pdf`
- Page count and section list
- Gaps included on the "missing" page
- Offer: "Want a compact one-pager version too?" (single A4 page: logo + palette + fonts + one rule per section — for quick briefs)

If colors/fonts were extracted or confirmed during this run and `design-guide.md` was blank, offer to write them into `resources/identity/design-guide.md` so all other skills pick them up.

---

## Boundaries

- **Brand doesn't exist yet** (empty identity folder AND blank memory) → run `growth/brand-identity` first, then come back
- **Single social visual** → platform thumbnail skills
- **Pitch deck** → `fundraising/investor-pitch-deck`
- **Generic PDF manipulation** → `formats/pdf`

## Checklist

- [ ] Everything in `resources/identity/` inventoried and classified
- [ ] Book styled with the brand's own colors and fonts, not defaults
- [ ] All images embedded via absolute paths and verified rendered
- [ ] Gaps listed inside the PDF, not silently dropped
- [ ] PDF opened/inspected after render
- [ ] Offered to backfill `design-guide.md` if it was blank
