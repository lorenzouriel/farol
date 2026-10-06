---
name: ingest
description: >
  Feeds the PARA second brain. Takes raw input (a file in `inbox/`, a URL, a
  pasted note, a meeting transcript) and files it as atomic, linked notes into the right
  PARA folder, updating existing notes instead of duplicating. Use when the user says
  "ingest", "/ingest", "save this to my brain", "add to second brain", "capture this",
  "file this note", or drops a file in `inbox/` and asks to process it.
---

# /ingest - Feed the Second Brain

Turns raw input into clean, linked PARA notes. The brain **rewrites itself**: you do not
append blindly, you update what already exists and reconcile what changed.

## Context to read

- **Business context:** `memory/company.md` (to know what the input is about)
- **Current focus:** `memory/strategy.md` (to decide what is an active *project* vs an ongoing *area*)
- **Existing knowledge:** `index.md` and the relevant `projects/`, `areas/`, `resources/` folders (to update instead of duplicate)
- **Tone:** `memory/preferences.md` (for any prose you write)

## Flow

### Step 1 - Gather the input

In priority order:
1. An explicit URL or file path the user passed → read it (fetch the URL, or read the file).
2. Anything sitting in `inbox/` (skip the README) → process each item.
3. Text the user pasted in chat.

If nothing is found, ask: "What should I ingest? Paste it, give me a URL, or drop a file in `inbox/`."

### Step 2 - Extract atomic notes

Break the input into **discrete, self-contained ideas** — one concept, entity, fact, or
decision per note. A single article may yield 3-10 notes. Do not create one giant note.

Classify each note as one of: `entity` (person, company, tool), `concept` (idea, framework,
method), `decision`, or `reference` (raw fact, quote, stat).

### Step 3 - Route into PARA

Decide where each note belongs:

| Folder | Use when the note is... |
|---|---|
| `projects/<name>/` | Tied to an active project or client in `strategy.md` (has a goal + deadline) |
| `areas/<domain>/` | About an ongoing responsibility (marketing, seo, sales, finance, ops) |
| `resources/<topic>/` | Reusable reference not tied to current work — **default when unsure** |

### Step 4 - Update, don't duplicate

Before writing, search `projects/`, `areas/`, and `resources/` for an existing note on the same entity/concept.

- **Exists →** open it and merge. Add new claims, refresh changed ones, and if the new input
  **contradicts** an existing claim, keep both with dates and flag it (see recency markers).
- **New →** create the file. Filename: `kebab-case-title.md`.

### Step 5 - Write in the AI-first note format

Every note follows this shape:

```markdown
---
title: <Title>
type: entity | concept | decision | reference
tags: [<topic>, <topic>]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
source: <url or file name>
---

> For future Claude: <one line on why this note exists and when to use it>

<Body. Each claim carries a recency marker so staleness is visible:>

- <Claim> (as of <YYYY-MM>, <source>)
- <Claim that changed> — previously <old>, now <new> (as of <YYYY-MM>, <source>)

Related: [[other-note]], [[another-note]]
```

Rules for the format:
- **Wikilinks are mandatory.** Every note links to at least one related note via `[[name]]`.
  A `[[link]]` to a note that does not exist yet is fine — it marks a gap to fill later.
- **Recency markers are mandatory.** Every claim says when it was true and where it came from.
- Keep the "For future Claude" line — it is how the next session knows what the note is for.

### Step 6 - Update the catalog

Add or update the note's line in `index.md` under its PARA section
(`- [[note-name]] — one-line hook`). Create `index.md` if it does not exist.

### Step 7 - Clear the inbox

After a source file is filed, move it to `archive/ingested/<YYYY-MM-DD>-<name>`
(raw source stays recoverable) and confirm. Never silently delete an inbox file.

## Output

Reply with a short manifest, nothing more:

```
Ingested: <source>

→ resources/<topic>/<note>.md        (new)
→ areas/<domain>/<note>.md           (updated, +2 claims)
⚠ contradiction flagged in <note>.md

Index updated. Inbox cleared.
```

## Rules

- Never invent claims the source does not support. If something is unclear, leave it out.
- Always keep the `source:` so a claim can be traced back.
- Prefer updating an existing note over creating a near-duplicate.
- One concept per note — split rather than bloat.
- Follow `memory/preferences.md` for any prose tone.
- This skill only writes inside `projects/`, `areas/`, and `resources/`. Generated deliverables still go to their respective area/project folder or `resources/documents/`.
