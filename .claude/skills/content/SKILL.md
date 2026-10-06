---
name: content
description: >
  Content creation and management hub. Routes to specialized sub-skills for writing,
  humanizing, archiving, planning, and scheduling content. Trigger on: "write copy",
  "content plan", "schedule post", "archive content", "humanize this", "SEO",
  "content planner", "plan my week", "buffer", "rewrite", "headline", "CTA copy".
---

# Content — Content Creation & Management

Orchestrator for all content-related tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/content archive` | `archive-content/SKILL.md` | "archive my medium posts", "import linkedin history", "save my old content", "fill content archive" |
| `/content buffer` | `buffer/SKILL.md` | "schedule post", "publish to buffer", "queue this", "social scheduling" |
| `/content plan` | `content-planner/SKILL.md` | "content plan", "plan my week", "7-day plan", "what should I post", "cross-platform plan" |
| `/content copy` | `copywriting/SKILL.md` | "write copy", "rewrite this page", "headline help", "CTA copy", "marketing copy", "landing page copy" |
| `/content humanize` | `humanizer/SKILL.md` | "humanize this", "make this sound human", "remove AI tone", "scrub AI tells", "rewrite naturally" |
| `/content seo` | `seo/SKILL.md` | "SEO", "keyword research", "rank higher", "Google Ads", "on-page SEO", "GEO" |
