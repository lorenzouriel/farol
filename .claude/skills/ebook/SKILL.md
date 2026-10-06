---
name: ebook
description: >
  Knowledge Archive → Ebook hub. Turns existing Medium articles and LinkedIn
  posts into a cohesive, professionally structured ebook through four
  gated phases (Inventory → Outline → Write → Assemble). Routes to
  specialized sub-skills for each phase. Trigger on: "turn my articles into
  a book", "build an ebook from my content", "compile my posts into a book",
  "knowledge archive to ebook", "book architect", "write my book from my
  articles", "ebook from my archive".
---

# Ebook — Knowledge Archive → Ebook Hub

Orchestrator for turning a body of written work (Medium articles, LinkedIn
posts, newsletter archive) into a single coherent ebook. This is not
summarization — it's curation, restructuring, and elevation into one
narrative, in the author's own voice.

A full book is never written in one sitting. Each phase below produces a
durable artifact on disk so the process can resume in a later session
without re-deriving prior decisions.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/ebook inventory` | `ebook-inventory/SKILL.md` | "start a new ebook", "inventory my articles for a book", "scan my archive for a book", "what would go in a book from my content" |
| `/ebook outline` | `ebook-outline/SKILL.md` | "outline the book", "propose chapters", "book architecture", "design the table of contents" |
| `/ebook write` | `ebook-write/SKILL.md` | "write the next chapter", "draft chapter X", "continue the book" |
| `/ebook assemble` | `ebook-assemble/SKILL.md` | "assemble the book", "put the book together", "final manuscript", "export the ebook" |

Run phases in order. Each phase ends with a **hard stop for approval** —
never skip ahead to the next phase without the user explicitly approving
the current one's output.

## Project state

Every ebook project lives under:

```
areas/products/ebook-<slug>/
  00-scope.md          ← source folders, date range, language (from Phase 1 kickoff)
  01-inventory.md       ← Phase 1 output: content inventory table + proposed pillars
  02-outline.md         ← Phase 2 output: title, chapter architecture, gaps
  chapters/
    01-<chapter-slug>.md
    02-<chapter-slug>.md
    ...
  ebook-manuscript.md   ← Phase 4 output: final assembled single Markdown file
```

`<slug>` is a short kebab-case version of the working title (e.g.
`sql-server-internals`). If the user doesn't name the project and only one
`ebook-*` folder exists under `areas/products/`, assume that one.
If several exist, ask which project to resume.

Each sub-skill's first move is to check whether its phase file already
exists — if so, treat this as **resuming**, not starting over, and confirm
with the user before overwriting anything.

## About the author and voice (applies to all phases)

Senior Data Engineer / SQL Server DBA / Analytics & AI Engineer, writing
engineer-to-engineer. Direct, practical, concrete: real commands, real SQL,
real tradeoffs. No fluff, no motivational filler, no "in today's
fast-paced world" openers. This voice **overrides** the default social/
newsletter tone in `memory/preferences.md` for this product line — the
ebook reads like the source articles, not like a generic AI book or a
LinkedIn post. Default source/output language is English unless the user
says otherwise; confirm once during `ebook-inventory` and record it in
`00-scope.md`.

## Hard rules (apply to every phase)

- Never fabricate facts, benchmarks, or code the source material doesn't support.
- Never flatten technical depth to make it "accessible" — the reader is a mid-to-senior practitioner.
- When source posts conflict in opinion, keep the more nuanced take; note the evolution if it's interesting.
- A shorter, tighter book beats a padded one — thin or off-topic material gets excluded, not stretched.
- Preserve all code blocks verbatim unless they contain errors; if fixed, log it as an editor's note.

## Sub-Skill Capabilities

### `ebook-inventory` — Phase 1: Inventory
Recursively reads every file in the given source folders (defaults to
`areas/marketing/content/` if the user has run `/content archive` before,
otherwise asks for a path). Builds a content inventory table, flags
duplicates/near-duplicates (a LinkedIn post condensing an article loses to
the article), clusters everything into 4-8 thematic pillars, and proposes
them. **Stops for approval.**

### `ebook-outline` — Phase 2: Book architecture
Takes the approved pillars and designs the book: working title + 2-3
alternatives, parts/chapters with source files and a one-sentence core
argument per chapter, an explicit reader definition (promise + exclusions),
and a gap list (topics the outline needs but the archive doesn't cover —
never filled in without asking). **Stops for approval.**

### `ebook-write` — Phase 3: Writing
Writes one chapter at a time from the approved outline: merges sources,
removes platform artifacts (hooks, "follow me", CTAs, engagement bait),
adds transitions, keeps the problem → substance → "In practice" shape, and
cross-references other chapters. Saves each chapter to
`chapters/NN-<slug>.md` and **waits for "next" before starting the next
chapter.**

### `ebook-assemble` — Phase 4: Assembly
Concatenates all chapters plus front matter (title page, intro, TOC) and
back matter (script/command appendix by topic, About the Author draft)
into one `ebook-manuscript.md` with consistent heading hierarchy (`#` book
title, `##` parts, `###` chapters), ready for Pandoc/typst conversion.

## Self-check before delivering any phase

1. Does the output match the author's voice (direct, concrete, no filler)? Re-read the "About the author and voice" section if unsure.
2. Did this phase stop for approval instead of cascading into the next one?
3. Was the phase artifact actually written to `areas/products/ebook-<slug>/`, not just shown in chat?
