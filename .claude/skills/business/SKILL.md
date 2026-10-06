---
name: business
description: >
  Business operations hub. Routes to sub-skills for ads management, data analysis,
  post approval, outreach, and revenue operations. Trigger on: "ads report",
  "analyze data", "approve post", "cold email", "google ad", "professional email",
  "publish topic", "reply reviews".
---

# Business — Operations & Revenue

Orchestrator for all business operations tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/business ads-report` | `ads-report/SKILL.md` | "ads report", "ad performance", "campaign results", "ads summary" |
| `/business analyze` | `analyze-data/SKILL.md` | "analyze data", "analyze this CSV", "data analysis", "look at these numbers" |
| `/business approve` | `approve-post/SKILL.md` | "approve post", "review this post", "check before publishing", "final review" |
| `/business cold-email` | `cold-email/SKILL.md` | "cold email", "outreach email", "prospecting email", "B2B outreach" |
| `/business google-ad` | `google-ad/SKILL.md` | "google ad", "create a google ad", "search ad copy", "google ads campaign" |
| `/business email` | `professional-email/SKILL.md` | "professional email", "write an email", "formal email", "business email" |
| `/business publish` | `publish-topic/SKILL.md` | "publish topic", "choose what to publish", "topic selection", "what to write about" |
| `/business reply` | `reply-reviews/SKILL.md` | "reply reviews", "respond to reviews", "handle reviews", "review responses" |
