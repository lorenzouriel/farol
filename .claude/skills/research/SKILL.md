---
name: research
description: >
  Research and knowledge management hub. Routes to sub-skills for web scraping,
  second brain ingestion, deep research, and knowledge synthesis. Trigger on:
  "scrape", "research", "ingest this", "add to brain", "synthesize notes",
  "what do I know about", "apify", "last 30 days", "deep dive", "file this note".
---

# Research — Research & Knowledge Management

Orchestrator for all research and knowledge management tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/research apify` | `apify/SKILL.md` | "scrape this site", "run apify actor", "extract data from", "scrape linkedin", "web scraping" |
| `/research ingest` | `ingest/SKILL.md` | "ingest this", "add to brain", "file this note", "save to second brain", "process inbox", "add to vault" |
| `/research deep` | `research-deep/SKILL.md` | "research", "deep dive", "what do I know about", "investigate", "last 30 days on", "find info on" |
| `/research synthesize` | `synthesize/SKILL.md` | "synthesize notes", "find patterns", "what's emerging", "connect my notes", "compound brain" |
