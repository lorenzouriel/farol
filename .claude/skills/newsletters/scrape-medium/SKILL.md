---
name: scrape-medium
description: >
  Scrapes and archives Lorenzo Uriel's Medium articles into areas/marketing/content.
  Uses the Medium public API to collect slugs, then WebFetch to retrieve full
  article text verbatim. Saves to YYYY/MM/WEEK XX/medium/filename.md.
  Trigger on: 'archive medium', 'scrape medium posts', 'import medium articles'.
---

# Medium Scraper

Archives Medium articles into `areas/marketing/content/YYYY/MM/WEEK XX/medium/`.

## Profile

- **Handle:** `@lorenzouriel`
- **User ID:** `79192a9d5fcb` (stable — used in API calls)
- **Profile URL:** `https://medium.com/@lorenzouriel`

---

## Content archive Path Convention

```
areas/marketing/content/
  YYYY/
    MM/        ← zero-padded (01–12)
      WEEK 01/ ← days 1–7
      WEEK 02/ ← days 8–14
      WEEK 03/ ← days 15–21
      WEEK 04/ ← days 22–31
        medium/
          article-slug.md
```

**Week formula:** `min((day - 1) // 7 + 1, 4)`

**Filename:** take the `uniqueSlug`, strip the trailing 12-char hex ID.
- `sql-clean-code-guideline-cbfa6aff745e` → `sql-clean-code-guideline.md`
- Regex: remove last `-[a-f0-9]{12}$`

**Frontmatter:**
```yaml
---
title: "Article Title"
date: YYYY-MM-DD
platform: medium
url: https://medium.com/@lorenzouriel/{uniqueSlug}
---
```

---

## Step-by-Step Workflow

### Step 1 — Collect all article slugs

Use the helper script `references/collect_slugs.py` to paginate the Medium API and
dump all slugs with their dates to `slugs.json`. No auth required.

API endpoint:
```
https://medium.com/_/api/users/79192a9d5fcb/profile/stream?limit=25&source=overview
```

Pagination: each response has a `paging.to` cursor. Fetch with `&to={cursor}` until
no cursor is returned. The featured post repeats on every page — deduplicate by slug.

Each post object contains:
- `uniqueSlug` — full slug with hex ID (e.g. `sql-clean-code-guideline-cbfa6aff745e`)
- `firstPublishedAt` — Unix timestamp in milliseconds

### Step 2 — Filter by cutoff date

Default cutoff: **January 1, 2024**. Skip slugs where `firstPublishedAt` is before cutoff.

### Step 3 — Fetch each article via WebFetch

For each slug not already in the content archive, fetch:
```
https://medium.com/@lorenzouriel/{uniqueSlug}
```

**WebFetch prompt (use exactly — do not paraphrase):**
> "Return the raw article text EXACTLY as it appears on the page. Do NOT rewrite, restructure, bullet-point, or summarize anything. Copy the text verbatim, sentence by sentence, paragraph by paragraph, in the exact same order it appears. Include every word the author wrote. If there are code blocks, copy them exactly. If there are headers, copy them exactly. Do not add your own words or structure. Just copy what you see."

Extract from the page:
- **Title** — from `<h1>` or the page `<title>`
- **Date** — shown as "Jun 3, 2026" or "Jan 16, 2024"; use `firstPublishedAt` from the API as the source of truth for the date
- **Full text** — verbatim, including code blocks and headers

### Step 4 — Handle edge cases

**Paywalled articles:** Medium truncates member-only content for anonymous readers.
The text cuts off mid-sentence. Save what's available and append `[PAYWALL CUTOFF]`
at the end. Report these to the user so they can paste the full content manually.

**Rate limiting:** Medium enforces a session limit (resets at 3 AM São Paulo time / UTC-3).
If the response body is "You've hit your session limit", stop immediately and report to the user.

**Batch size:** Fetch at most 10 articles per session to avoid triggering the session limit.

### Step 5 — Write the file

Compute path from the publish date:
```python
year  = date.strftime('%Y')
month = date.strftime('%m')
week  = f"WEEK {min((date.day - 1) // 7 + 1, 4):02d}"
path  = f"areas/marketing/content/{year}/{month}/{week}/medium/{filename}.md"
```

Create all subfolders if they don't exist. Skip if the file already exists (incremental runs).

---

## Incremental Runs

Before fetching, scan existing content archive files:
```python
existing = set()
for f in glob("areas/marketing/content/*/*/WEEK */medium/*.md"):
    existing.add(os.path.basename(f))
```

Skip any slug whose derived filename is already in `existing`.

---

## Reporting

After each run, report:
```
✓ Saved: 12 articles (2024-03 → 2024-06)
⚠ Paywalled (paste needed): 3 articles
  - sql-clean-code-guideline (2025-12-10)
  - airflow-3-1-setup (2025-11-30)
  - ...
⚠ Skipped (pre-2024): 8 articles
⚠ Skipped (already in content archive): 45 articles
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/collect_slugs.py` | Paginate Medium API → dump `slugs.json` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Session limit hit | Stop. Retry after 3 AM São Paulo (UTC-3) |
| WebFetch returns summary instead of verbatim | Re-fetch the same URL once — caching layer sometimes differs |
| Date not visible on page | Use `firstPublishedAt` timestamp from `slugs.json` |
| Slug already has no hex ID | Skip the regex strip — use the slug as-is |
| Duplicate filenames after strip | Append `-2`, `-3` etc. |
