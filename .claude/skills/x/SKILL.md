---
name: x
description: >
  The X (Twitter) creator skill. Covers tweet writing, hook formulation,
  content strategy, account growth, algorithm optimization, thread planning,
  and reply engagement. Routes to specialized sub-skills for each task.
  Triggers on: "x", "twitter", "tweet", "thread", "hook", "reply drafter",
  "x strategy", "x content", "x growth", "followers", "impressions",
  "engagement", "for you page", "FYP", "x algorithm", "write a tweet",
  "content plan for x", "x calendar".
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

# Claude X — X (Twitter) Creator Skill

> Orchestrator for X content creation, strategy, and growth. Routes to the right
> sub-skill based on your request. Sub-skills and reference files do the work —
> this file routes, delegates, and quality-checks.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/x tweet` | `x-tweet-writer/SKILL.md` | "write me a tweet", "tweet about X", "hook for X", "short post for X", "thread opener" |
| `/x strategy` | `x-content-strategy/SKILL.md` | "X strategy", "grow on X", "X content plan", "X algorithm", "why isn't my X growing", "build an X presence from scratch", "X positioning", "content pillars for X" |

> **Planned sub-skills** (pending creation — use `/x tweet` or `/x strategy` as proxy):
> - `x-thread-writer` — write full threads after the opener
> - `x-hook-extractor` — reverse-engineer a hook from a viral tweet in your niche
> - `x-reply-drafter` — draft substantive replies to comments on your tweets
> - `x-content-planner` — build the 7-day tactical calendar from a strategy

If a request spans multiple sub-skills (e.g., "help me plan and write my first week of X content"),
run the relevant sub-skills sequentially — strategy first, then tweet drafts.

## Context-Gathering Protocol

Before invoking ANY sub-skill, collect these inputs. If any are missing, ask:

1. **Account niche/topic** — What is the account about? Be specific (not "tech" — "data engineering for solo data teams").
2. **Account size tier:**
   - New: < 500 followers
   - Growing: 500–5K followers
   - Established: 5K–50K followers
   - Authority: 50K+ followers
3. **Primary goal:** Growth / Brand Authority / Traffic / Community Engagement

## How X Works (Signal Priority)

X is text-first, opinion-driven, speed-dependent. Reach comes from being
right, being interesting, or being first — not from production quality.

| Signal | Weight | Notes |
|--------|--------|-------|
| Replies | Highest | Back-and-forth thread under your tweet |
| Quote tweets | High | Someone adds their take |
| Bookmarks | Medium | "Worth returning to" signal |
| Retweets | Medium | Weaker than QTs |
| Likes | Lowest | Least impact on reach |

**Links in tweet body → ~50% algorithmic reach penalty.** Always move to first reply.

## Reference Files

Load on-demand when a sub-skill requires them. Never pre-load all at once.

| File | Content |
|------|---------|
| `x-tweet-writer/references/hook-formulas.md` | 10 formula skeletons (T1–T10) with worked examples |
| `x-tweet-writer/references/algorithm-heuristics.md` | 2026 X algorithm rules, posting windows, engagement benchmarks |

## Quality Gates

Every sub-skill output MUST pass before delivery:

1. **Specificity** — Every recommendation must be actionable for THIS account's niche and tier. No generic "post consistently" without cadence specifics.
2. **Platform accuracy** — No advice that contradicts the 2026 X algorithm rules in reference files. Never hallucinate benchmarks.
3. **Voice integrity** — No AI tells: no em dashes (—), no hedging ("might", "perhaps"), no all-caps words, no emoji spam.

## Self-Anneal Loop

If a sub-skill output fails a quality gate:
1. Identify which gate failed and why
2. Re-read the relevant reference file
3. Re-generate only the failing sections
4. If still failing after 2 attempts, deliver with explicit caveats

## Output Format

Default to markdown. For tweet drafts, always include: formula used, full tweet text, character count, suggested posting window. End every response with a "Next Step" pointing to the logical next sub-skill.
