---
name: ebook-write
description: >
  Phase 3 of the ebook hub. Writes one book chapter at a time from an
  approved outline, merging source articles/posts into book prose while
  preserving code blocks and the author's voice. Saves each chapter to
  disk and waits for "next" before continuing. Use when asked to "write
  the next chapter", "draft chapter X", "continue the book".
---

# Ebook Write — Phase 3

Requires an approved `02-outline.md` from `ebook-outline`. If it doesn't
exist, stop and run `ebook-outline` first.

## Step 1: Find where we are

List `chapters/*.md` in the project folder. The next chapter to write is
the first one in the outline's order without a corresponding file. If the
user names a specific chapter, write that one instead (out-of-order
writing is fine — the outline already fixed the structure).

## Step 2: Merge the source material

Pull the source files listed for this chapter in `02-outline.md`.
- Eliminate repetition across sources — don't say the same thing twice
  because two posts said it.
- Resolve contradictions in favor of the most recent piece (check
  frontmatter dates). If the older take is more nuanced or the shift in
  thinking is itself interesting, keep the nuance and note the evolution
  in one line rather than silently picking one.
- Unify terminology — if one post says "replica" and another says
  "secondary," pick one term and use it consistently within the chapter.

## Step 3: Rewrite for book flow

- Remove platform artifacts: LinkedIn hooks ("Here's what nobody tells
  you about..."), "follow me for more," Medium CTAs, engagement bait
  ("Agree?", "Thoughts?").
- Add transitions between merged sections so it reads as one argument, not
  stitched posts.
- Convert post-style fragments (short punchy lines meant for a feed) into
  full prose appropriate for a book page.
- Preserve **all code blocks verbatim** unless they contain an actual
  error. If you fix one, add an inline editor's note directly after the
  block: `> Editor's note: fixed <what was wrong> — original used <X>.`
  Keep the author's SQL/code style conventions (casing, formatting)
  intact otherwise.

## Step 4: Chapter shape

Every chapter follows:
1. **Framing** (2-3 sentences) — the problem, stated the way the author
   would state it, not a textbook restatement.
2. **Substance** — the merged, rewritten content.
3. **"In practice"** closing — a short, concrete takeaway. Not a generic
   summary ("In this chapter we covered...") — an actionable point the
   reader leaves with.

## Step 5: Cross-references

Where this chapter's topic connects to another chapter, add an inline
pointer: "see Chapter 6 for the AG failover mechanics." Only add these
where genuinely useful — don't force a cross-reference into every
paragraph.

## Voice check before saving

Re-read against `ebook/SKILL.md`'s "About the author and voice" section:
direct, practical, concrete, real commands/SQL/tradeoffs. No fluff, no
motivational filler, no "in today's fast-paced world" openers, no
generic AI-book cadence. If a paragraph could have been written about any
topic by swapping nouns, cut or rewrite it.

## Output

Save to `chapters/NN-<chapter-slug>.md` (zero-padded chapter number
matching the outline's global order, not per-part), with a small header:

```markdown
---
chapter: <N>
title: <chapter title>
part: <part name>
sources: <file>, <file>
---

# <Chapter title>

<content>
```

Then output the chapter in the chat and **stop — wait for the user to say
"next" (or name a specific chapter) before writing another one.** Never
chain multiple chapters in one turn even if the user approved the whole
outline earlier; each chapter gets its own read.
