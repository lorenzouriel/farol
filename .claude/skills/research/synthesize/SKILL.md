---
name: synthesize
description: >
  Compounds the second brain. Reads recent notes across `projects/`, `areas/`, and `resources/` and surfaces unnamed
  patterns, recurring themes, and connections the user has not made explicit yet, then
  writes them up as new resource/area notes. Use when the user says "synthesize",
  "/synthesize", "what patterns are in my brain", "connect my notes", or "what's emerging".
---

# /synthesize - Surface What's Emerging

The opposite of ingest: instead of filing input, this reads what is already filed and finds
the pattern across it. Run it weekly. The brain compounds when scattered notes become a
named idea.

## Context to read

- **Recent notes:** everything in `projects/`, `areas/`, `resources/`
  touched recently (default: last 30 days by `updated:` frontmatter; ask for a different window).
- **Catalog:** `index.md`
- **Focus:** `memory/strategy.md` (to weight what matters now)

## Flow

### Step 1 - Scan

Collect notes in the window. Read titles, "For future Claude" lines, tags, and key claims —
not every word. Aim for breadth across the brain, not depth on one note.

### Step 2 - Find patterns

Look for:
- **Recurring themes** — the same idea showing up in 3+ unrelated notes.
- **Bridges** — two notes from different domains that imply a connection nobody wrote down.
- **Graduation candidates** — a `resources/` topic that has enough notes to become a real
  `projects/` effort or `areas/` responsibility.
- **Contradictions** — claims across notes that disagree (hand off to `/reconcile` if deep).

### Step 3 - Write it up

For each strong pattern, create a new note (usually in `resources/` or `areas/`)
in the AI-first format from `/ingest`, linking back to every note it synthesizes:

```markdown
---
title: <Named pattern>
type: concept
tags: [synthesis, <topic>]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
source: synthesis of brain notes
---

> For future Claude: <what this pattern is and why it surfaced>

<The pattern, in plain language. What connects the sources.>

Synthesized from: [[note-a]], [[note-b]], [[note-c]]
```

Add it to `index.md`.

## Output

```
Synthesized <N> notes from the last <window>:

◆ <Named pattern> → resources/<note>.md   (from 4 notes)
◆ <Graduation> — "<topic>" is ready to become a project
⚠ <Contradiction> between [[a]] and [[b]] — run /reconcile

Index updated.
```

## Rules

- Name patterns the user has *not* already named — do not restate an existing note.
- Every synthesis note links to its sources. No orphan conclusions.
- Suggest graduations and contradictions; do not move or resolve them without asking.
- If nothing real emerges, say so. Do not manufacture a pattern.
- Follow `memory/preferences.md` for tone.
