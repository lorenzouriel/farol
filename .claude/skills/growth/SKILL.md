---
name: growth
description: >
  Marketing and growth strategy hub. Routes to sub-skills for growth hacking,
  brand identity, brand book PDF export, community building, lifecycle email
  marketing, and content marketing strategy. Trigger on: "growth strategy",
  "growth hacking", "traction", "brand identity", "brand pyramid", "brand book",
  "brand guidelines PDF", "community", "email campaign", "drip campaign",
  "lifecycle email", "nurture sequence", "content strategy", "content pillars",
  "editorial calendar".
---

# Growth — Marketing & Growth Strategy

Orchestrator for marketing and growth strategy tasks. Routes to the right sub-skill based on your request. All reports are saved to `resources/marketing-growth/`.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/growth hacking` | `growth-hacking/SKILL.md` | "growth hacking", "growth strategy", "traction", "bullseye framework", "growth experiments" |
| `/growth brand` | `brand-identity/SKILL.md` | "brand identity", "brand pyramid", "visual identity", "brand strategy" |
| `/growth brand-book` | `brand-book/SKILL.md` | "brand book", "brand guidelines PDF", "export brand", "share my brand", "brand kit for designers" |
| `/growth community` | `community-building/SKILL.md` | "community", "community building", "community strategy", "engagement program" |
| `/growth email` | `email-marketing/SKILL.md` | "email marketing", "drip campaign", "lifecycle email", "nurture sequence", "email automation" |
| `/growth content` | `content-marketing/SKILL.md` | "content marketing strategy", "content pillars", "editorial calendar", "hub and spoke" |

## Boundaries — when NOT to use this hub

- **Cold outreach to new prospects** → `business/cold-email` (this hub's `email-marketing` is for opted-in lifecycle/drip/nurture only)
- **Weekly cross-platform content plan** → `content/content-planner` (this hub's `content-marketing` is quarter-level strategy: pillars, calendar architecture, distribution)
- **Writing actual posts/scripts** → platform hubs (`linkedin/`, `instagram/`, `tiktok/`, `x/`, `youtube/`)
- **SEO execution (keywords, GBP, Google Ads)** → `content/seo`

## Recommended Flow

Skills chain their outputs (each detects prior reports in `resources/marketing-growth/`):

1. `brand-identity` → define who you are
   - `brand-book` → package the identity as a shareable PDF once assets exist
2. `content-marketing` → plan the content engine
3. `growth-hacking` → pick traction channels
4. `email-marketing` → build the lifecycle funnel
5. `community-building` → compound retention
