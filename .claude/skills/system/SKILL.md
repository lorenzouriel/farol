---
name: system
description: >
  CompanyOS management and utility hub. Routes to sub-skills for system setup,
  memory updates, file organization, session management, and critical thinking.
  Trigger on: "install", "update memory", "open session", "save to github",
  "organize files", "new project", "map routines", "pressure test", "open".
---

# System — CompanyOS Management

Orchestrator for all CompanyOS system and utility tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/system install` | `install/SKILL.md` | "install companyos", "set up for my business", "configure memory", "first time setup" |
| `/system update` | `update/SKILL.md` | "update memory", "sync context", "update companyos", "my context is outdated" |
| `/system open` | `open/SKILL.md` | "open session", "start session", "load context", "what's my focus today" |
| `/system save` | `save/SKILL.md` | "save to github", "commit", "push changes", "backup companyos" |
| `/system new-project` | `new-project/SKILL.md` | "new project", "start a project", "new client", "create project folder" |
| `/system organize` | `file-organizer/SKILL.md` | "organize files", "clean up folders", "find duplicates", "tidy workspace" |
| `/system map-routines` | `map-routines/SKILL.md` | "map my routines", "automate tasks", "create custom skills", "what can be a skill" |
| `/system last-30-days` | `last-30-days/SKILL.md` | "research topic", "last 30 days on", "what's happening with", "trend research" |
| `/system pressure-test` | `sycophancy/SKILL.md` | "pressure test", "challenge this", "what am I missing", "steelman the opposite", "critique my plan" |
