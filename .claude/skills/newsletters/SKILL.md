---
name: newsletters
description: >
  The newsletter creator skill. Covers writing long-form content that sounds human,
  AEO optimization for AI citation, Substack Notes data extraction, and thumbnail
  generation for articles. Routes to specialized sub-skills for each task.
  Triggers on: "newsletter", "write a newsletter", "newsletter draft", "Substack",
  "article", "edition", "issue", "long-form content", "optimize for AI", "AEO",
  "thumbnail", "cover image", "hero image", "Substack notes", "extract notes",
  "notes data", "newsletter optimization", "AI citation", "sounds human", "less AI".
tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - Edit
  - Grep
  - Glob
  - Agent
---

# Claude Newsletters — Newsletter Creator Skill

> Orchestrator for newsletter writing, optimization, analytics extraction, and
> visual asset generation. Routes to the right sub-skill based on your request.
> Sub-skills and reference files do the work — this file routes, delegates, and quality-checks.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/newsletter write` | `newsletter-human/SKILL.md` | "write a newsletter", "help me write about X", "draft this edition", "make this sound human", "less AI", "newsletter issue", "long-form content", "turn this into a newsletter", "break this into posts" |
| `/newsletter optimize` | `newsletter-optimization/SKILL.md` | "optimize for AI", "AEO optimization", "AI citation", "Perplexity", "ChatGPT cites", "score my article", "restructure for AI engines", "answer capsules" |
| `/newsletter extract` | `newsletter-notes-extractor/SKILL.md` | "extract Substack notes", "get my notes stats", "pull Substack engagement", "export notes from Substack", paste a Substack `/notes` URL |
| `/newsletter thumbnail` | `newsletter-thumbnail/SKILL.md` | "generate thumbnail image", "cover image", "hero image", "social preview", "article cover", "make a thumbnail for this post" |
| `/newsletter thumbnail-prompt` | `thumbnail-prompt/SKILL.md` | "thumbnail prompt", "thumb prompt", "midjourney prompt for this article", "dall-e prompt", "image prompt for thumbnail", "prompt for cover" |
| `/newsletter archive` | `newsletter-archive/SKILL.md` | "archive substack", "import newsletter history", "save my old newsletters", "pull my substack posts into the content archive", "archive all my newsletters" |
| `/newsletter scrape-medium` | `scrape-medium/SKILL.md` | "archive medium", "scrape medium posts", "import medium articles", "pull my medium articles into the content archive", "save medium history" |

If a request spans multiple sub-skills (e.g., "write the newsletter then optimize it for AI"):
run `newsletter-human` first, then pass the approved draft to `newsletter-optimization`.

## Context-Gathering Protocol

Before invoking content sub-skills (`write`, `optimize`, `thumbnail`), collect:

1. **Newsletter name / platform** — e.g., "The Data Dispatch on Substack"
2. **Niche and audience** — Be specific: not "tech readers" — "solo data engineers building their first data stack"
3. **Subscriber tier:**
   - New: < 500 subscribers
   - Growing: 500–5K subscribers
   - Established: 5K–25K subscribers
   - Authority: 25K+ subscribers
4. **Monetization model:** Free / Paid / Freemium (affects `optimize` paywall logic)

For `extract` sub-skill, collect: Substack notes URL, author display name, date range.
For `thumbnail` sub-skill, collect: article text or URL, and verify BRAND BLOCK is configured.

## Sub-Skill Capabilities

### `newsletter-human` — Human Newsletter Writer
Writes newsletters that sound like a person, not a machine. Uses the Single Idea
framework, awareness-level targeting, the 7-step workflow (Plan → Research → Structure →
Opening → Hook → Write → Review → Humanize), and copywriting frameworks (AIDA, PAS,
PASTOR, SUCCES). Loads `references/frameworks.md` and `references/human-craft.md`.

**The core rule:** One idea, one emotion, one action. Everything in the newsletter serves these.

**The authenticity shortcut:** Write for your "past self" — someone 1–2 steps behind you on the journey.

### `newsletter-optimization` — AEO Optimization
3-step process: Score → Restructure → Score Again. Scores articles 0–100 for AI citation
readiness. Adds answer capsules (50–80 words) after each H2, converts headings to question
format, removes links from capsule zones, splits long paragraphs. Does NOT change the
author's voice — capsules are clinical, everything below them is human.

**Key stat:** Answer capsules drive 3× more AI citations. This is the #1 change.

### `newsletter-notes-extractor` — Substack Notes Extractor
Uses Chrome MCP to browse a Substack notes page, scroll to load the target period, extract
structured data (date, text, likes, comments, restacks, link) for a specific author, and
save as a formatted .xlsx spreadsheet. Requires Chrome MCP.

### `newsletter-thumbnail` — Article Thumbnail Generator (Gemini API)
Generates brand-consistent still thumbnails via the Gemini API using a bundled `generate.js`
script. Requires: Gemini API key in `.env`, `generate.js` in cwd, Node.js 18+, and the
BRAND BLOCK in `newsletter-thumbnail/SKILL.md` filled in by the user. Claude Code only.

### `thumbnail-prompt` — Thumbnail Prompt Generator (Midjourney / DALL·E / SD)
Generates a paste-ready image-generation prompt in the brand's locked thumbnail style, read
from `resources/identity/design-guide.md` (falls back to a duotone engraving default
when the guide is blank). No API calls, no image generation. Outputs: primary prompt + one
alternative + thumbnail-survival tradeoff.

## Newsletter → Posts System

The newsletter is the **mother resource**. Write once, extract all week:
- Impact phrases → tweet / LinkedIn hook
- Listicle items → carousel slides
- Framework → educational Reel
- Contrarian take → X thread opener
- Step-by-step → TikTok script

Don't fear repetition — most of the audience didn't see the original post.

## AEO Score Interpretation

| Score | Citation Readiness | Action |
|-------|-------------------|--------|
| 90–100 | HIGH | Publish |
| 70–89 | GOOD | Quick fixes, then publish |
| 50–69 | MEDIUM | Restructuring needed |
| 30–49 | LOW | Major restructuring |
| 0–29 | INVISIBLE | Rewrite with AEO structure |

Answer capsules account for 30/100 points — the single highest-impact category.

## Reference Files

Load on-demand when a sub-skill requires them.

| File | Content |
|------|---------|
| `newsletter-human/references/frameworks.md` | Awareness levels, 5 opening types, 6 headline elements, AIDA/PAS/PASTOR/SUCCES, Cialdini triggers |
| `newsletter-human/references/human-craft.md` | 8 craft techniques, 10 attention-capture patterns, quick anti-AI checklist |
| `newsletter-archive/references/collect_posts.py` | Paginate Substack API → dump `posts.json` |
| `scrape-medium/references/collect_slugs.py` | Paginate Medium API → dump `slugs.json` |

## Quality Gates

Every sub-skill output MUST pass before delivery:

1. **Single idea integrity** — Every newsletter draft must serve exactly one central idea. If the outline covers 3+ separate ideas, flag before writing.
2. **Human voice** — No AI tells: no inflated significance, no rule-of-three without receipts, no vague attributions ("experts say"), no generic conclusions.
3. **AEO correctness** (for `optimize`) — Answer capsules must be 50–80 words, self-contained, no links, no hedging, no preamble.

## Self-Anneal Loop

If a sub-skill output fails a quality gate:
1. Identify which gate failed and why
2. Re-read the relevant reference file
3. Re-generate only the failing sections
4. If still failing after 2 attempts, deliver with explicit caveats

## Output Format

Default to markdown. Newsletter drafts: full formatted text with sections. AEO output: before/after score comparison + full restructured article. Notes extraction: .xlsx file. Thumbnail: PNG file path + scene plan. Always end with "Next Steps" pointing to the logical continuation.
