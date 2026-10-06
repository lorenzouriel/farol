---
name: ebook-outline
description: >
  Phase 2 of the ebook hub. Turns approved content pillars into a book
  architecture: title options, part/chapter structure with source mapping
  and core arguments, reader definition, and a gap list. Stops for
  approval before Phase 3 (writing). Use when asked to "outline the book",
  "propose chapters", "design the table of contents", "book architecture".
---

# Ebook Outline — Phase 2

Requires an approved `01-inventory.md` from `ebook-inventory`. If it
doesn't exist or the pillars in it were never explicitly approved by the
user in this or a prior session, stop and run `ebook-inventory` first —
do not invent pillars from scratch here.

If `02-outline.md` already exists, this is a **resume**: show it and ask
whether to revise or move on to `ebook-write`.

## Step 1: Title

Propose a working title and 2-3 alternatives. Titles should read like the
source voice (direct, concrete) — avoid generic "The Complete Guide to X"
phrasing unless that's genuinely the sharpest option.

## Step 2: Chapter architecture

Each approved pillar becomes a **part**. Each part contains 2-5
**chapters**. For every chapter:
- Title
- Source files it draws from (by filename, from the inventory)
- Single core argument, in one sentence — if you can't compress a chapter
  to one sentence, it's covering too much; split it or narrow it

Order parts and chapters so the book builds — foundational material before
material that depends on it (e.g., internals before tuning, tuning before
HA/DR).

## Step 3: Define the reader

State explicitly:
- Who this book is for (default: mid-to-senior data practitioners — adjust
  if the archive skews more specific, e.g. SQL Server DBAs specifically)
- What the book promises them
- What it deliberately excludes (and why — scope discipline, not a
  weakness)

## Step 4: Identify gaps

List topics the outline needs for coherence that the archive doesn't
cover — a chapter that's structurally necessary but has no source
material yet. **Do not invent content to fill gaps.** Flag them and ask
the user how to handle each: cut the chapter, write it fresh (they
provide the input), or leave a placeholder.

## Output format

Write `02-outline.md` in the project folder:

```markdown
# Outline — <title>

## Title options
1. <working title>
2. <alternative>
3. <alternative>

## Reader
- For: <description>
- Promises: <what they get>
- Excludes: <what's deliberately out of scope>

## Structure

### Part I — <pillar name>

#### Chapter 1: <title>
Sources: <file>, <file>
Core argument: <one sentence>

#### Chapter 2: <title>
...

### Part II — <pillar name>
...

## Gaps
- <topic> — needed for <reason>, not covered in archive. Resolution: <pending user decision>
```

Then **stop**. Report the chapter count, total planned word count estimate
(sum of source word counts as a floor), and the gap list. Ask for approval
before writing begins. Do not proceed to `ebook-write` in the same turn.
