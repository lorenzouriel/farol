---
name: newsletter-archive
description: >
  Archives past Substack newsletters into areas/marketing/content/YYYY/MM/WEEK XX/substack/.
  Uses the Substack public API to collect post slugs, then WebFetch to retrieve
  full article text verbatim. Triggered by: 'archive substack', 'import newsletter history',
  'save my old newsletters', 'pull all my substack posts into the content archive'.
---

# Newsletter Archive

Archives all past Substack posts into `areas/marketing/content/YYYY/MM/WEEK XX/substack/`.

## Profile

- **Publication URL:** `https://lorenzouriel.substack.com` (update if different)
- **Handle:** `@lorenzouriel`
- **Platforms:** Substack only — for Medium, use the `/medium` skill

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
        substack/
          post-slug.md
```

**Week formula:** `min((day - 1) // 7 + 1, 4)`

**Filename:** use the `slug` field from the API directly — no hex strip needed.
- `the-data-dispatch-issue-12` → `the-data-dispatch-issue-12.md`

**Frontmatter:**
```yaml
---
title: "Post Title"
date: YYYY-MM-DD
platform: substack
url: https://lorenzouriel.substack.com/p/{slug}
audience: everyone   # or: paid
---
```

---

## Step-by-Step Workflow

### Step 1 — Collect all post slugs

Use `references/collect_posts.py` to paginate the Substack API and dump slugs
with metadata to `posts.json`. No auth required for public posts.

API endpoint:
```
https://{subdomain}.substack.com/api/v1/archive?sort=new&offset=0&limit=12
```

Each response is a JSON array of post objects. Paginate by incrementing `offset`
by 12 until the response is an empty array.

Each post object contains:
- `slug` — URL slug (e.g. `the-data-dispatch-issue-12`)
- `post_date` — ISO 8601 date string
- `title` — post title
- `canonical_url` — full URL to the post
- `audience` — `"everyone"` or `"paid"`
- `type` — `"newsletter"` (skip `"podcast"` or `"thread"` types if present)

### Step 2 — Filter by cutoff date

Default cutoff: **January 1, 2024**. Skip posts where `post_date` is before cutoff.

### Step 3 — Fetch each post via WebFetch

For each slug not already in the content archive, fetch the `canonical_url`.

**WebFetch prompt (use exactly — do not paraphrase):**
> "Return the raw article text EXACTLY as it appears on the page. Do NOT rewrite, restructure, bullet-point, or summarize anything. Copy the text verbatim, sentence by sentence, paragraph by paragraph, in the exact same order it appears. Include every word the author wrote. If there are code blocks, copy them exactly. If there are headers, copy them exactly. Do not add your own words or structure. Just copy what you see."

Extract from the page:
- **Title** — from `<h1>` or use the `title` field from the API (more reliable)
- **Date** — use `post_date` from the API as the source of truth
- **Full text** — verbatim, including code blocks and headers

### Step 4 — Handle edge cases

**Paywalled posts:** Substack truncates paid content for non-subscribers.
The text cuts off with a paywall prompt. Save what's available and append
`[PAYWALL CUTOFF]`. Report to the user for manual paste.

**Rate limiting:** If WebFetch starts returning empty or login-redirect responses,
stop and report to the user.

**Batch size:** Fetch at most 10 posts per session.

### Step 5 — Write the file

Compute path from `post_date`:
```python
year  = date.strftime('%Y')
month = date.strftime('%m')
week  = f"WEEK {min((date.day - 1) // 7 + 1, 4):02d}"
path  = f"areas/marketing/content/{year}/{month}/{week}/substack/{slug}.md"
```

Create all subfolders if they don't exist. Skip if the file already exists.

---

## Incremental Runs

Before fetching, scan existing content archive files:
```python
existing = set()
for f in glob("areas/marketing/content/*/*/WEEK */substack/*.md"):
    existing.add(os.path.basename(f).replace(".md", ""))
```

Skip any slug already in `existing`.

---

## Reporting

After each run, report:
```
✓ Saved: 8 posts (2024-03 → 2024-06)
⚠ Paywalled (paste needed): 2 posts
  - the-data-dispatch-issue-20 (2025-04-10)
  - ...
⚠ Skipped (pre-2024): 5 posts
⚠ Skipped (already in content archive): 31 posts
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/collect_posts.py` | Paginate Substack API → dump `posts.json` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| API returns empty on first call | Check subdomain — update `PUBLICATION_URL` in script |
| WebFetch returns login redirect | Post is paywalled or Substack is throttling — mark `[PAYWALL CUTOFF]` |
| WebFetch returns summary instead of verbatim | Re-fetch the same URL once |
| Date missing from API response | Skip the post and report to user |
| Duplicate slugs after pagination | Deduplicate by `slug` field before writing |
