---
name: newsletter-notes-extractor
description: >
  Extract Substack Notes data (date, text, likes, comments, restacks, link) from a publication's
  notes page for a specific author and time period, then compile everything into a formatted .xlsx
  spreadsheet. Use this skill whenever the user wants to scrape, extract, or collect Substack notes
  or posts data — even if they say "get my notes stats", "pull my Substack engagement data",
  "export notes from Substack", or "grab post metrics from my publication". Also trigger when the
  user mentions a Substack notes URL (anything ending in /notes) and wants data pulled from it.
---

# Substack Notes Extractor

Extract notes from a Substack publication's notes page for a given author and time period, then
save the results as a professionally formatted Excel spreadsheet.

## Required Inputs

Before starting, collect these three inputs from the user. If any are missing, ask:

1. **Start URL** — The Substack notes page URL (e.g. `https://mypublication.com/notes`)
2. **Author name** — The display name shown on notes (e.g. "Frank Andrade")
3. **Period** — The month or date range to extract (e.g. "February 2026", "March 1–15, 2026")

## How It Works

This skill uses Claude in Chrome to browse the Substack notes page, scroll to load posts from the
target period, and extract structured data from each note. The reason we use browser automation
rather than an API is that Substack Notes don't have a public API — the data only lives on the
rendered page.

## Step-by-Step Workflow

### 1. Open the Page

Navigate to the user's notes URL using Claude in Chrome browser tools.

### 2. Scroll to Load the Target Period

Substack notes load progressively as you scroll. You need to scroll far enough to load all posts
from the target period. The approach:

- Use JavaScript to scroll aggressively: `window.scrollBy(0, 20000)` with short waits between
  scrolls to let content load
- Take periodic screenshots to check what dates are visible
- Keep scrolling until you see posts **older** than the target period (this confirms all target
  posts are loaded)
- Relative timestamps ("19h", "2d", "6d") appear for recent posts; older posts show dates like
  "Feb 27" or "Mar 12"

### 3. Extract Post Data via JavaScript

Once all target posts are loaded in the DOM, use JavaScript to extract data from the feed items.

**Finding feed items:**
```javascript
document.querySelectorAll('[class*="feedItem-"]')
```

**Identifying the author:** Each feed item's `innerText` starts with the author name. Only process
items where the text starts with the exact author name the user specified. This filters out
restacked posts from other authors.

**Getting the date:** Each post has a date link with a `title` attribute containing the full date
(e.g. `title="Feb 28, 2026, 9:26 PM"`). The visible text shows abbreviated dates like "Feb 28".

**Extracting the post body:** Split the innerText by newlines, skip the author name (line 0) and
date (line 1), and collect body lines until you hit "See more" or the engagement numbers at the
end.

### 4. Get Engagement Numbers Correctly

This is the most important detail to get right. Do NOT parse engagement numbers from raw innerText
— the order of numbers in the text doesn't reliably map to likes, comments, and restacks.

Instead, use the **aria-label** attribute on the action buttons:

```javascript
const likeBtn = item.querySelector('[aria-label="Like"]');
const commentBtn = item.querySelector('[aria-label="Comment"]');
const restackBtn = item.querySelector('[aria-label="Restack"]');

const likes = likeBtn ? (likeBtn.textContent.trim() || '0') : '0';
const comments = commentBtn ? (commentBtn.textContent.trim() || '0') : '0';
const restacks = restackBtn ? (restackBtn.textContent.trim() || '0') : '0';
```

This approach is reliable because each button is semantically labeled regardless of its visual
position.

### 5. Build the Post Link

Find the `<a>` tag within each feed item whose `pathname` contains `/note/`:

```javascript
const allLinks = item.querySelectorAll('a');
for (const a of allLinks) {
  const p = new URL(a.href).pathname;
  if (p.includes('/note/')) { notePath = p; break; }
}
```

The path will look like `/@handle/note/c-221107504`.

**The link domain must be `substack.com`**, not the publication's custom domain. So the final link
format is:

```
https://substack.com/@handle/note/c-XXXXXXXXX
```

Extract the handle from the path (e.g. `@thepycoach`) and the note ID, then construct the link
with the `substack.com` domain.

### 6. Create the Spreadsheet

Use openpyxl to create a formatted .xlsx file. Run the bundled script:

```bash
python <skill-path>/scripts/create_spreadsheet.py \
  --output "<output-path>/AuthorName_Notes_MonthYear.xlsx" \
  --data '<JSON array of post objects>'
```

Each post object in the JSON array should have these fields:
```json
{
  "date": "Feb 28, 2026",
  "text": "Post body text...",
  "likes": 148,
  "comments": 3,
  "restacks": 22,
  "link": "https://substack.com/@handle/note/c-XXXXXXXXX"
}
```

The script produces a professional spreadsheet with:
- Headers: Date, Text of Post, Likes (Hearts), Comments, Restacks, Link of Post
- Blue header row with white bold text (Arial font)
- Alternating row colors for readability
- Frozen top row and auto-filter enabled
- Links styled as blue underlined text
- Appropriate column widths

### 7. Present the File

Save the spreadsheet to the outputs folder and present it to the user with `present_files`.

## Edge Cases

- **Posts with zero engagement:** A button with no visible number means 0. The `textContent` will
  be empty, so default to "0".
- **Multiple posts on the same date:** This is normal — just include all of them.
- **Date range vs. full month:** If the user asks for a specific date range (e.g. "March 1–15"),
  filter posts to only those within that range. If they say a month name, include all posts from
  that calendar month.
- **The page may show restacked posts from other authors** interleaved with the target author's
  own posts. These are often preceded by "You restacked" text. Always filter by author name to
  skip these.
