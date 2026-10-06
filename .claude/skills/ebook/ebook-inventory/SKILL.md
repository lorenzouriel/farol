---
name: ebook-inventory
description: >
  Phase 1 of the ebook hub. Recursively scans Medium articles and LinkedIn
  posts, builds a content inventory table, flags duplicates, and proposes
  4-8 thematic pillars for a book. Stops for approval before Phase 2. Use
  when starting a new ebook project or when asked to "inventory my
  articles", "scan my archive for a book", "start a new ebook".
---

# Ebook Inventory — Phase 1

You are acting as a senior technical editor and book architect. This phase
only inventories and clusters — it does not write or outline yet.

## Step 1: Establish scope

Ask (skip any the user already gave you):
1. **Source path(s)** — default to `areas/marketing/content/` (the
   content archive filled by `/content archive`). The user may point to
   other folders too, e.g. `resources/study/` notes or a raw
   export folder.
2. **Working title / slug hint** — even a rough topic ("SQL Server book")
   is enough to derive `<slug>` (kebab-case, e.g. `sql-server-internals`).
3. **Language** — English, Portuguese, or "keep the source language per
   piece." Default English per `ebook/SKILL.md`.

Create `areas/products/ebook-<slug>/` and write `00-scope.md`:

```markdown
# Scope — <working title hint>

- Source paths: <list>
- Language: <choice>
- Started: <date>
```

If `areas/products/ebook-<slug>/01-inventory.md` already exists,
this is a **resume**: show the existing inventory and ask whether to
re-scan (pick up new files since last run) or move straight to Phase 2.

## Step 2: Recursively read every file

Read every article/post file under the source path(s). For each one, capture:
- Filename and full path
- Type: article (Medium) or post (LinkedIn)
- Main topic (one phrase)
- Subtopics (comma list)
- Approximate word count
- Code languages present (T-SQL, Python, Bash, PowerShell, etc.), or "none"
- Publish date if available in frontmatter

## Step 3: Flag duplicates and near-duplicates

A LinkedIn post that condenses an article is a duplicate — **the article
wins** and gets kept as the source; the post is marked `[condensed into: <article filename>]`
and excluded from the writing phase, but stays in the table for
completeness.

Two articles covering near-identical ground (not just the same topic tag,
but substantially the same argument) get flagged `[near-duplicate of: <file>]`
with a one-line note on what, if anything, differs.

## Step 4: Cluster into pillars

Group the inventory into 4-8 thematic pillars. Typical shape for this
author (adjust to what the archive actually contains — don't force content
into a pillar it doesn't fit):

- SQL Server internals & performance tuning
- HA/DR (Always On, failover, backups)
- Modern data stack (pipelines, Fabric, Redshift)
- AI/agentic engineering
- Career & project management

For each pillar, list: pillar name, one-sentence description, source files
that belong to it (by filename), and a rough total word count.

## Output format

Write `01-inventory.md` in the project folder:

```markdown
# Inventory — <working title hint>

## Content table

| File | Type | Topic | Subtopics | Words | Code | Status |
|---|---|---|---|---|---|---|
| sql-clean-code-guideline.md | article | T-SQL style | naming, formatting | 1400 | T-SQL | keep |
| 2025-11-02-post.md | post | T-SQL style | naming | 180 | none | condensed into sql-clean-code-guideline.md |

## Duplicates / near-duplicates

- <file> — condensed into <file>
- <file> — near-duplicate of <file>: <what differs>

## Proposed pillars

### 1. <Pillar name>
<one-sentence description>
Sources: <file>, <file>, ...
~<N> words total

### 2. <Pillar name>
...
```

Then **stop**. Report the inventory summary (file counts, total usable
word count, duplicate count, pillar list) in the chat and ask for approval
or adjustment of the pillars before any outlining begins. Do not proceed
to `ebook-outline` in the same turn.
