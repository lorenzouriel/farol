---
name: linkedin
description: >
  The LinkedIn creator skill. Covers post writing, comment drafting, content
  planning, strategy, profile optimization, algorithm mechanics, and inbound
  generation. Routes to specialized sub-skills for each task.
  Triggers on: "linkedin", "linkedin post", "linkedin comment", "linkedin strategy",
  "linkedin content plan", "linkedin growth", "linkedin algorithm", "linkedin hook",
  "write a linkedin post", "comment on linkedin", "plan my linkedin week",
  "build my linkedin presence", "linkedin inbound", "linkedin authority".
tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - Edit
  - Grep
  - Glob
  - Agent
---

# Claude LinkedIn — LinkedIn Creator Skill

> Orchestrator for LinkedIn content creation, engagement, planning, and strategy.
> Routes to the right sub-skill based on your request. Sub-skills and reference
> files do the work — this file routes, delegates, and quality-checks.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/linkedin post` | `linkedin-post-writer/SKILL.md` | "write me a LinkedIn post", "post about X", "LinkedIn hook", "draft a post", "F1–F10 formula" |
| `/linkedin comment` | `linkedin-comment-drafter/SKILL.md` | "comment on this post", "draft a LinkedIn comment", "be first commenter", "engage with this post", paste a LinkedIn post URL |
| `/linkedin plan` | `linkedin-content-planner/SKILL.md` | "plan my week", "LinkedIn content calendar", "what should I post this week", "7-day plan", "monthly plan" |
| `/linkedin strategy` | `linkedin-content-strategy/SKILL.md` | "LinkedIn strategy", "grow on LinkedIn", "LinkedIn algorithm", "why isn't my LinkedIn growing", "build a LinkedIn presence", "inbound from LinkedIn", "LinkedIn positioning" |

If the request spans multiple sub-skills (e.g., "build a 4-week LinkedIn strategy and draft the first week's posts"),
run strategy first, then plan, then post-writer — passing output from each as input to the next.

## Context-Gathering Protocol

Before invoking ANY sub-skill, collect these inputs. If any are missing, ask:

1. **Professional niche/domain** — What is the creator's expertise? Be specific (not "tech" — "data engineering for mid-market companies").
2. **Profile size tier:**
   - New: < 500 connections/followers
   - Growing: 500–5K
   - Established: 5K–20K
   - Authority: 20K+ followers
3. **Primary goal:** Inbound Leads / Brand Authority / Career Positioning / Community Building / Hiring

For `comment` sub-skill, also collect the LinkedIn post URL.

## How LinkedIn Works (Signal Priority)

LinkedIn is professional-credibility-first. The audience reads deeply — 2–3 minutes
on a carousel is normal. Depth and specificity win. Overt selling triggers distrust.

| Signal | Weight | Notes |
|--------|--------|-------|
| Comments | Highest (8–10× likes) | Every reply extends reach window |
| Shares / Reposts | High | To external audiences |
| Saves | High | "Worth returning to" signal |
| Clicks ("see more") | High | Dwell time signal |
| Likes | Low | Nice to have, minimal reach impact |

**External links in post body → algorithmic reach penalty.** Move to first comment.

**The "see more" cutoff:** LinkedIn truncates at ~210 characters. First 210 chars = your hook.
First-hour engagement → algorithm's primary boost window. Reply to every comment within 2 hours.

## The 3-Pillar System

| Pillar | Share | Purpose |
|--------|-------|---------|
| Authority | 40–50% | Expert positioning — data, breakdowns, frameworks |
| Personal Narrative | 30–40% | Trust — stories, confessions, behind-the-scenes |
| Community | 20–30% | Engagement — polls, questions, spotlights |
| *(Product/Offer)* | *(10–15% max)* | *Sell rarely. Trust first.* |

## Reference Files

Load on-demand when a sub-skill requests them. Never pre-load all at once.

| File | Content |
|------|---------|
| `linkedin-post-writer/references/hook-formulas.md` | F1–F10 formula skeletons with reference engagement numbers |
| `linkedin-post-writer/references/algorithm-heuristics.md` | 2026 LinkedIn posting rules, timing, format guidance |
| `linkedin-post-writer/references/humanizer-checklist.md` | AI-tell scrub list for LinkedIn copy |
| `linkedin-comment-drafter/references/comment-templates.md` | T1–T7 comment templates with fill-in slots |
| `linkedin-comment-drafter/references/examples.md` | Worked comment examples per template |
| `linkedin-comment-drafter/references/voice-rules.md` | Voice rules from user feedback |
| `linkedin-content-planner/references/example-plan-week.md` | Filled-in 7-day plan example |
| `linkedin-content-planner/references/pillars-framework.md` | The 3-pillar discipline explained |

## Parallel Agent Rules

**`strategy` sub-skill** — when diagnosing a stalled account, spawn 3 parallel agents:
- Agent A: Content audit (pillar mix, formula diversity, posting frequency)
- Agent B: Engagement audit (comment volume, reply rate, first-hour activity)
- Agent C: Profile audit (headline, about section, featured, creator mode)

All other sub-skills run inline. If Agent tool is unavailable, fall back to sequential inline execution.

## Quality Gates

Every sub-skill output MUST pass before delivery:

1. **Specificity** — Every recommendation must be actionable for THIS profile's niche and tier. No generic "post consistently" without exact cadence.
2. **Platform accuracy** — No advice that contradicts 2026 LinkedIn algorithm rules. Never hallucinate benchmark numbers.
3. **Voice integrity** — No AI tells: no em dashes (—), no "game-changer", no "deep dive", no "leverage", no "fundamentally". No external links in post bodies.

## Self-Anneal Loop

If a sub-skill output fails a quality gate:
1. Identify which gate failed and why
2. Re-read the relevant reference file for missing data
3. Re-generate only the failing sections
4. If still failing after 2 attempts, deliver with explicit caveats

## Output Format

Default to markdown. For posts: formula used, full draft, char count, suggested posting window. For plans: markdown table. For strategy: structured report with pillar scores. Always end with "Next Steps" pointing to the logical next sub-skill.

## Pipeline position

**Receives from:** `/content plan` — the weekly calendar defines which posts to write
**Then:** `/content humanize` — scrub AI tells and apply brand voice before publishing
**Outputs to:** manual post (LinkedIn does not have a public scheduling API)
**Or:** `/content buffer` — Buffer supports LinkedIn scheduling
