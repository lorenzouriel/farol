---
name: archive-content
description: "Archives historical content from Medium and LinkedIn into the areas/marketing/content folder structure. Use when the user wants to import past articles, posts, or content history into the content archive. Trigger on: 'archive my medium posts', 'import linkedin history', 'save my old content', 'fill content archive with my posts'."
---

# Archive Content

Imports historical content from Medium and/or LinkedIn into `areas/marketing/content/YYYY/MM/WEEK XX/<platform>/<filename>.md`.

## Invoking the skill

The user will specify a source:
- `archive medium` — fetch all articles from Medium profile
- `archive linkedin` — use Apify scraper
- `archive all` — both sources
- A date range may be specified: `since January 2024`, `from 2024`, etc. Default cutoff: January 1, 2024.

---

## Content archive Structure

```
areas/marketing/content/
  YYYY/
    MM/           ← zero-padded month (01, 02, ... 12)
      WEEK 01/    ← days 1–7
        medium/
          article-slug.md
        linkedin/
          YYYY-MM-DD-post-preview.md
      WEEK 02/    ← days 8–14
      WEEK 03/    ← days 15–21
      WEEK 04/    ← days 22–31
```

**Week folder calculation:**
```python
week = (day - 1) // 7 + 1   # 1–4, clamp to 4 max
week_label = f"WEEK {min(week, 4):02d}"
```

Examples:
- June 3, 2026 → `2026/06/WEEK 01`
- May 21, 2026 → `2026/05/WEEK 03`
- Jan 31, 2024 → `2024/01/WEEK 04`

**File frontmatter:**
```yaml
---
title: "Article Title"
date: YYYY-MM-DD
platform: medium   # or: linkedin
url: https://...
---
```

---

## Medium — Full Workflow

### Step 1: Get user ID

Fetch `https://medium.com/@lorenzouriel?format=json` and extract the `userId` field.
Known value: `79192a9d5fcb` (Lorenzo Uriel).

### Step 2: Paginate all article slugs

API endpoint: `https://medium.com/_/api/users/{userId}/profile/stream?limit=25&source=overview`

Each page returns ~4 posts and a `paging.to` cursor. Continue fetching with `&to={cursor}` until no cursor is returned. The response's `paging` object will have a `to` field if there are more pages.

Collect the `uniqueSlug` from each post object. This is the full URL slug including the hex ID (e.g., `sql-clean-code-guideline-cbfa6aff745e`).

**Note:** The featured post repeats on every page — deduplicate by tracking seen slugs.

### Step 3: Fetch each article

URL: `https://medium.com/@lorenzouriel/{uniqueSlug}`

**WebFetch prompt (use exactly):**
> "Return the raw article text EXACTLY as it appears on the page. Do NOT rewrite, restructure, bullet-point, or summarize anything. Copy the text verbatim, sentence by sentence, paragraph by paragraph, in the exact same order it appears. Include every word the author wrote. If there are code blocks, copy them exactly. If there are headers, copy them exactly. Do not add your own words or structure. Just copy what you see."

Extract:
- Title (from `<h1>` or page title)
- Publication date (shown as e.g. "Jun 3" with year context from the page)
- Full article text verbatim

**Paywalled articles:** Medium truncates member-only articles for anonymous readers. The text will cut off mid-sentence. Save what's available and append `[PAYWALL CUTOFF]`. Report these to the user for manual paste.

**Rate limiting:** Medium enforces a session limit (resets at 3am Sao Paulo time / UTC-3). If the response body is "You've hit your session limit", stop and report to the user.

### Step 4: Derive filename

Take the `uniqueSlug`, remove the trailing hex ID segment (the last `-XXXXXXXXXXXX` part, 12 hex chars):
- `sql-clean-code-guideline-cbfa6aff745e` → `sql-clean-code-guideline.md`
- `airflow-3-0-setup-and-architecture-ef2a81bc3d25` → `airflow-3-0-setup-and-architecture.md`

The regex pattern: remove the last `-[a-f0-9]{12}$` from the slug.

### Step 5: Write the file

Path: `areas/marketing/content/{YYYY}/{MM}/{WEEK_LABEL}/medium/{filename}.md`

Create all subfolders if they don't exist.

**Skip** articles with publish dates before the cutoff (default: Jan 1, 2024).

---

## LinkedIn — Full Workflow

### Source: Apify scraper (CSV export removed by LinkedIn)

LinkedIn removed `Posts.csv` from their data export. Use the Apify Actor instead.

**Refer to the `/apify` skill for full setup and workflow.**

Quick summary:
1. Load Apify MCP tools via ToolSearch
2. Run `harvestapi/linkedin-profile-posts` with `maxPosts: 0` and `postedLimitDate: "YYYY-MM-DD"`
3. Poll with `get-actor-run` until SUCCEEDED
4. Fetch all dataset items (paginate at 200/batch)
5. Filter to `author.publicIdentifier == "lorenzo-uriel"` (excludes reshares)
6. For each item, compute `YYYY/MM/WEEK XX` path and write markdown file

Key output fields from the Actor: `content`, `postedAt.date`, `shareLinkedinUrl`, `article.link`, `author.publicIdentifier`

Reference script: `.claude/skills/research/apify/references/linkedin_to_vault.py`

---

## Reporting

After processing, report:
1. Total files created, by platform and year
2. Date range covered
3. Articles/posts skipped (pre-cutoff)
4. Paywalled articles (Medium only) — list titles so user can paste content

Format:
```
✓ Medium: 92 articles saved (2024–2026)
✓ LinkedIn: 48 posts saved (2024–2026)
⚠ Skipped (pre-2024): 14 articles
⚠ Paywalled (need paste): 5 articles
  - sql-clean-code-guideline (2025-12-10)
  - ...
```

---

## Incremental runs

On subsequent runs, check which folders already contain files for the platform before writing. Skip files that already exist (don't overwrite). Only process new content published since the last run.

To detect new content: compare the most recent date in existing content archive files against the current date and only fetch articles/posts after that date.

---

## Troubleshooting

- **Medium rate limit**: Stop, report to user, retry after 3am Sao Paulo (UTC-3)
- **WebFetch summarizes instead of verbatim**: The prompt above is calibrated to force verbatim output. If it still summarizes, try fetching the article a second time
- **Wrong week folder**: Use `(day - 1) // 7 + 1`, clamped to 4. Day 31 → WEEK 04, not WEEK 05
