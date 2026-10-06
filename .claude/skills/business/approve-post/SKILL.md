---
name: approve-post
description: >
  Publishes an approved content package: flips blog draft to published, copies carousel
  PNGs to the site's public folder, commits and pushes, waits for deploy, and posts the
  carousel to Instagram + Facebook via Meta Graph API. Use after /publish-topic or when
  the user says "approve post", "publish post X", or "go live".
---

# /approve-post - Publish Approved Content

Bridges approved content (blog + carousel + captions, created by `/business publish-topic`) to real publishing — site, Instagram, and Facebook.

## When NOT to use

- Content hasn't been created yet → use `/business publish-topic` first
- User is still reviewing → do not run until they say "approved" / "go live"
- Site not deployed / Meta API not configured → complete setup below first

## Prerequisites (one-time setup)

`.env` at the workspace root with:

```
META_PAGE_ACCESS_TOKEN=   # long-lived Page token from Facebook
META_PAGE_ID=             # Facebook Page ID
META_IG_USER_ID=          # Instagram Business account ID
SITE_URL=                 # e.g. https://example.com
```

Also requires:
- Site with automatic deploy from the `main` branch (Netlify, Vercel, etc.)
- Instagram Business account connected to the Facebook Page
- Facebook Page with correct permissions on the Meta App
- `resources/scripts/post-instagram.js` and `resources/scripts/post-facebook.js` configured

If anything is missing: stop and point to setup. Create `resources/documents/meta-api-setup.md` if it does not exist.

## Argument

`/approve-post <slug>` — where `<slug>` is the blog file name **without `.md`**.

Example: `/approve-post how-to-retain-clients`

If the user did not pass a slug, list all blogs with `draft: true` and ask which one.

---

## Step 1 — Locate and validate files

- Blog: `site/.../blog/<slug>.md` (path depends on stack — Astro, Hugo, WordPress, etc.)
- Carousel: find `areas/marketing/content/<slug>-*` (folder has a date suffix)
- Validate that PNGs exist at `<carousel-folder>/instagram/slide-XX.png` (2 to 10 slides)
- Validate that `caption.md` and `caption-linkedin.md` exist

If anything is missing: stop and report exactly what is missing before proceeding.

## Step 2 — Show summary and ask for final confirmation

Show the user:
- Blog title
- Number of carousel slides
- First 200 characters of caption
- Final URL that will be published

Ask: **"Confirm publishing? (yes/no)"**. Only continue if they say yes.

## Step 3 — Flip draft to false

Edit the blog frontmatter: `draft: true` → `draft: false`.

## Step 4 — Copy PNGs to the site's public folder

- Source: `areas/marketing/content/<slug>-<date>/instagram/slide-*.png`
- Destination: `site/.../public/img/posts/<slug>/slide-*.png`
- Create destination folder if it does not exist
- Overwrite if already exists (handles re-publishing)

## Step 5 — Commit and push

```bash
git add site/<path>/blog/<slug>.md site/<path>/public/img/posts/<slug>/
git commit -m "publish: <blog title>"
git push origin main
```

Wait for push to complete successfully. If push fails: **rollback** `draft: false` → `draft: true`, report the error, and stop. Do not proceed.

## Step 6 — Wait for deploy

Automatic deploy (Netlify/Vercel) takes ~1-2 minutes. Validate the post is live:

```bash
curl -sf -o /dev/null -w "%{http_code}" "$SITE_URL/blog/$slug/"
```

Also check that at least `slide-01.png` is publicly accessible:

```bash
curl -sf -o /dev/null -w "%{http_code}" "$SITE_URL/img/posts/$slug/slide-01.png"
```

Wait for HTTP 200 on both (timeout: 5 minutes). **Do not call the Meta API until both return 200** — the API fetches images by public URL and will fail silently if the image is not accessible yet.

If deploy does not come up in 5 minutes: report, ask the user whether to continue anyway or abort.

## Step 7 — Post to Instagram

```bash
node --env-file=.env resources/scripts/post-instagram.js areas/marketing/content/<slug>-<date>
```

Capture the returned post ID. If this fails: **stop. Do not proceed to Facebook.** Report the error. The site is already live — only the feed post failed.

## Step 8 — Post to Facebook

```bash
node --env-file=.env resources/scripts/post-facebook.js areas/marketing/content/<slug>-<date>
```

Capture the returned post ID. If Facebook fails but Instagram succeeded: report the failure and suggest retrying only Facebook afterward.

## Step 9 — LinkedIn

LinkedIn is manual (company API requires lengthy approval). Show the user:

```
LinkedIn: paste this manually at https://linkedin.com/company/<your-page>:
<contents of caption-linkedin.md>
```

## Step 10 — Final summary

```
✓ Published: <blog title>

Site:       <SITE_URL>/blog/<slug>/
Instagram:  <post link>
Facebook:   <post link>
LinkedIn:   pending — text ready in caption-linkedin.md (post manually)
```

---

## Error handling

| What failed | What to do |
|---|---|
| Push failed | Rollback `draft: true`, report, stop |
| Deploy not up in 5 min | Report, ask user: continue or abort |
| Instagram API failed | Stop. Site is live. Report IG failure only |
| Facebook failed, Instagram OK | Report FB failure. Suggest retry `/approve-post facebook-only <slug>` |
| Missing files at Step 1 | Stop immediately, list exactly what is missing |

## Principles

1. **Human confirmation before anything irreversible.** Never skip Step 2.
2. **Idempotent where possible.** Re-running with the same slug should detect prior publishing (blog not draft, PNGs already in public/) and ask whether to re-post or just update.
3. **Fail early, fail loudly.** Any missing prerequisite = abort and explain exactly what is missing.
4. **Per-platform isolation.** Instagram and Facebook failures are independent. One failing does not require rolling back the other.
5. **Log everything.** Each step prints what it is doing and the result.
