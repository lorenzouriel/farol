---
name: publish-topic
description: >
  Orchestrates a complete SEO + social content package from a topic. Writes a blog post,
  creates a carousel summary, and generates captions for Instagram, Facebook, and LinkedIn —
  all connected, with the carousel pointing to the blog. Use when the user asks to publish
  a topic or turn a topic into content.
---

# /publish-topic - SEO + Social Content Pipeline

Orchestrator skill. Takes a topic → delivers a blog post + carousel + 3 captions (Instagram, Facebook, LinkedIn), all connected.

## Dependencies

- **Content strategy:** `areas/marketing/seo/05-content-strategy.md` (master list of topics, created by `/content seo`)
- **SEO research:** `areas/marketing/seo/01-demand-research.md`, `02-competition-analysis.md`, `08-ai-geo-optimization.md`
- **Carousel skill:** `.claude/skills/instagram/ig-carousel/SKILL.md` — use for the carousel phase
- **Site (blog):** `site/` — destination for articles. Common structure: Astro at `site/src/content/blog/`, or WordPress, or other. If no site exists yet, ask before proceeding.
- **Tone of voice:** `memory/preferences.md`
- **Context:** `memory/company.md`, `resources/identity/design-guide.md`

---

## Step 0 — Choose the topic

If the user passed an explicit topic → use it.

If nothing was passed → read `areas/marketing/seo/05-content-strategy.md`, list the satellite articles + pillar page, and ask:

> "Which topic from the strategy? (list of options)"

Mentally note which topics already have a blog post (check the blog folder) to avoid duplicates.

## Step 1 — Research before writing

Before writing a single word, read what the SEO research says about this topic:

- **Keywords and variations** from `01-demand-research.md`
- **How competitors treat it** from `02-competition-analysis.md` — to avoid the obvious. Search the top 5 results on Google and YouTube for this topic. Note: what already exists, which angle is weakest, what no one answered well. Write to fill that gap.
- **GEO angle** from `08-ai-geo-optimization.md` (if applicable) — questions that AI engines answer about this topic. Including a direct-answer section increases the chance of being cited in ChatGPT/Gemini/Perplexity results.

If these files do not exist, do a WebSearch of the top 5 Google results for the main keyword and use those as input.

## Step 2 — Write the blog post

**Destination:** depends on the site stack. Common patterns:
- Astro: `site/src/content/blog/<slug>.md`
- WordPress: generate markdown for the user to paste in the editor
- Other: confirm with the user

**Slug:** short kebab-case, no stopwords. "How to retain clients as a freelancer" → `retain-clients-freelancer`

**Frontmatter:**

```yaml
---
title: "Attractive title, close to the keyword"
description: "Meta description 150-160 characters, with keyword and benefit for the reader"
publishedAt: YYYY-MM-DD
author: "<name from memory/company.md>"
keywords:
  - primary keyword
  - variation 1
  - variation 2
draft: true
---
```

**Always start with `draft: true`.** The user reviews and flips to `false` when approving — or uses `/business approve-post`.

**Article structure (800-1500 words):**

1. **Lead (1-2 paragraphs):** concrete problem the audience faces. No preamble.
2. **H2 — What and why:** explain the problem and its root cause
3. **H2 — How to / what to look for:** practical steps or criteria
4. **H2 — Detail or comparison** (optional): technical depth or alternative approaches
5. **H2 — Where the business fits:** natural connection to the product/service — not an ad, a logical conclusion
6. **CTA:** WhatsApp link / form / contact configured in `memory/company.md`

**Writing rules** (follow `memory/preferences.md` strictly):
- Short sentences, 2-4 line paragraphs
- Concrete: numbers, certifications, dates, values when known
- No marketing jargon if the audience does not use it
- Clean markdown: `##` for H2, `###` for H3, lists with `-`, links in `[text](url)`

## Step 3 — Carousel summary

**Without asking, go straight to carousel creation** using the Instagram visual skill (ig-carousel) — text-only carousel type.

**Folder:** `areas/marketing/content/<blog-slug>-<YYYY-MM-DD>/`

Slide structure:
- **Slide 1 — Cover:** same title as the blog (or a shorter variation)
- **Slides 2-6:** the key points of the blog (1 idea per slide, natural phrasing — not dry bullets)
- **Last slide — CTA to the blog:** "Full article at our blog" + URL `<domain>/blog/<slug>`

**Cover style:** follow feed alternation sequence (light → dark/photo → accent color → repeat) — check the most recent folder in `areas/marketing/content/` to maintain consistency.

## Step 4 — Captions (3 versions)

Save all in `areas/marketing/content/<carousel-folder>/`:

**`caption.md`** (Instagram + Facebook — same text):
- Hook on the first line (question, bold statement, or number)
- 2-3 paragraphs of context (natural phrasing, no corporate tone)
- CTA to carousel ("Swipe through") + CTA to blog ("Full article at the link in bio" or direct URL)
- Business offer block (differentiators, contact)
- 10-15 hashtags (audience + niche + local)

**`caption-linkedin.md`** (LinkedIn — different approach):
- Hook (can be provocative, professional)
- 3-5 analytical paragraphs — LinkedIn accepts long text and rewards depth
- No "swipe through" (different audience, different behavior)
- CTA: direct link to the blog post
- No aggressive offer block — close with 1 line on who the company is
- Max 3 hashtags at the end, from the professional niche

**`caption-short.md`** (for X/Twitter or Stories):
- 1-2 lines max
- One strong idea + link

## Step 5 — Delivery summary

At the end, show the user a clear list:

```
✓ Blog post: <path>/<slug>.md (draft)
✓ Carousel: areas/marketing/content/<folder>/
    carrossel.html + render.js
    PNGs in instagram/
✓ Captions:
    caption.md (Instagram + Facebook)
    caption-linkedin.md
    caption-short.md

To publish:
1. Review the blog → flip draft: false when ready
2. Rebuild the site (if Astro/Hugo/etc) or paste into CMS
3. Render carousel PNGs: cd areas/marketing/content/<folder> && node render.js
4. Post carousel on Instagram + Facebook with caption.md (or use /business approve)
5. Post text + link on LinkedIn with caption-linkedin.md
```

---

## When NOT to use

- Standalone carousel (no blog) → use `/instagram visual` directly
- Updating an existing article → edit the `.md` directly
- Single-idea post or quote → use `/instagram carousel` directly

## Principles

1. **Blog is the parent piece.** Carousel and captions derive from it, not the other way around.
2. **Everything connected.** Each piece references the others — carousel links to blog, blog has a CTA to contact.
3. **Always draft first.** Never auto-publish — user reviews, then uses `/business approve-post`.
4. **Avoid the obvious.** Research competitors before writing. Write to fill the gap they left, not to repeat what already exists.
5. **The audience's language.** No corporate speak. Always.
