---
name: market
description: >
  Market and product strategy hub. Routes to sub-skills for go-to-market planning,
  pricing strategy, strategic roadmaps, and feature prioritization. Trigger on:
  "go to market", "GTM", "launch plan", "pricing", "price tiers", "roadmap",
  "OKR roadmap", "feature prioritization", "RICE", "what to build next".
---

# Market — Product & Market Strategy

Orchestrator for market and product strategy tasks. Routes to the right sub-skill based on your request. All reports are saved to `resources/market-product-strategy/`.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/market gtm` | `go-to-market/SKILL.md` | "go to market", "GTM plan", "launch plan", "90-day plan", "acquisition channels" |
| `/market pricing` | `pricing-strategy/SKILL.md` | "pricing", "pricing strategy", "price tiers", "how much to charge", "Van Westendorp" |
| `/market roadmap` | `strategic-roadmap/SKILL.md` | "roadmap", "strategic roadmap", "OKR roadmap", "18-month plan", "product roadmap" |
| `/market prioritize` | `feature-prioritization/SKILL.md` | "feature prioritization", "RICE", "ICE score", "what to build next", "value-effort" |

## Recommended Flow

Skills chain their outputs (each detects prior reports in `resources/market-product-strategy/`). Foundation work in `strategy/` feeds these:

1. `pricing-strategy` → set the model and tiers
2. `feature-prioritization` → decide what to build
3. `go-to-market` → plan the launch
4. `strategic-roadmap` → map the next 18 months
