---
name: research-deep
description: >
  Vault-first research. Before searching the web, scans the second brain for what is already
  known, then researches only the gaps, flags contradictions with existing notes, and files
  the result back into `projects/`, `areas/`, or `resources/`. Use when the user says "research-deep", "/research-deep",
  "what do we already know about X", or wants research that builds on the brain instead of
  starting from zero.
---

# /research-deep - Research That Builds on the Brain

Most research throws away what you already learned. This starts from the brain: it reads
your existing notes first, researches only what is missing, and feeds the answer back in —
so the brain gets smarter every time instead of accumulating duplicates.

This is the deep counterpart to `/last-30-days` (which always researches fresh). Reach for
this one when the topic is something the company has touched before.

## Context to read

- **Existing knowledge:** search `projects/`, `areas/`, `resources/`, and `index.md` for the topic and related notes.
- **Business context:** `memory/company.md`, `memory/strategy.md`.

## Flow

### Step 1 - Scan the brain first

Search `projects/`, `areas/`, and `resources/` for the topic. Pull every related note. Summarize, internally:
- **What we already know** (with the recency markers already on those claims).
- **What is stale** (claims older than a few months that may have changed).
- **What is missing** (the actual gaps to research).

If the brain already answers the question well, say so and stop — do not research for nothing.

### Step 2 - Research the gaps only

Research **only** the missing or stale pieces. Use available research tools
(`/last-30-days`, web fetch, the research toolkit) for the gaps, not the whole topic.
Keep real citations.

### Step 3 - Reconcile

Compare findings against the existing notes:
- **Confirms** an existing claim → refresh its recency marker.
- **Contradicts** an existing claim → keep both with dates and flag it.
- **Net-new** → a new claim or note.

### Step 4 - File it back

Hand the findings to the `/ingest` flow: write atomic notes in the AI-first format, route
them into PARA, update existing notes instead of duplicating, and update `index.md`.

## Output

```
Topic: <topic>

Already knew: <N> notes ([[a]], [[b]])
Researched gaps: <N> new findings
⚠ <Contradiction>: brain said <X> (as of <date>); source now says <Y>

Filed: <new/updated notes>. Index updated.
```

## Rules

- Brain first, web second. Never research what the brain already answers.
- Carry real citations and dates into the notes — no unsourced claims.
- Surface contradictions, do not silently overwrite the older belief.
- Follow `memory/preferences.md` for tone.
