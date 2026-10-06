---
name: ebook-assemble
description: >
  Phase 4 of the ebook hub. Assembles all written chapters plus front
  matter (title page, introduction, TOC) and back matter (script/command
  appendix, About the Author) into a single Pandoc-ready Markdown
  manuscript. Use when asked to "assemble the book", "put the book
  together", "final manuscript", "export the ebook".
---

# Ebook Assemble — Phase 4

Requires all chapters listed in `02-outline.md` to exist under
`chapters/` (or the user explicitly accepts an incomplete assembly, e.g.
"assemble what we have so far as a draft"). If chapters are missing,
list them and ask before proceeding.

## Step 1: Front matter

- **Title page** — final title (from `02-outline.md`, confirm it hasn't
  changed), author name, one-line subtitle if useful.
- **Introduction** — short, no-fluff: why this book exists, who it's for
  (pull from the outline's reader definition), how to read it (linear vs.
  reference — say which this book is). Written in the author's voice, not
  publisher-speak.
- **Table of contents** — generated from the actual part/chapter
  structure in `chapters/`, not re-derived from the outline (the outline
  is the plan; the chapter files are the ground truth).

## Step 2: Back matter

- **Appendix: scripts & commands** — scan every chapter for code blocks,
  consolidate them organized by topic/pillar (not by chapter number), with
  a one-line caption for each pointing back to its source chapter.
- **About the author** — draft from what's known via `memory/company.md`
  and the source material's byline info. Mark it clearly as a draft: `_Draft — edit before publishing._`

## Step 3: Concatenate

Build `ebook-manuscript.md` with consistent heading hierarchy:
- `#` — book title (used once, at the very top)
- `##` — parts
- `###` — chapters
- `####` and below — chapter-internal structure, as already written

Strip the per-chapter YAML frontmatter blocks (`chapter:`, `sources:`,
etc.) when concatenating — that metadata was for the writing phase, not
the reader. Keep chapters in the outline's global order regardless of the
order they were written in.

## Step 4: Sanity pass

Before delivering, check:
- [ ] Every chapter in `02-outline.md` appears exactly once
- [ ] Heading levels are consistent throughout (no chapter accidentally at `##`)
- [ ] No leftover platform artifacts, editor placeholder text, or `[TODO]` markers
- [ ] Code blocks render with correct language tags
- [ ] Cross-references ("see Chapter X") point to chapters that actually exist at that number

## Output

Write the full manuscript to
`areas/products/ebook-<slug>/ebook-manuscript.md`. Report: total
word count, chapter count, and note this file is Pandoc/typst-ready for
PDF/EPUB conversion (e.g. `pandoc ebook-manuscript.md -o ebook.epub`) —
do not run the conversion yourself unless asked.
