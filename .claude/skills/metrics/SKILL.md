---
name: metrics
description: >
  Retention and metrics hub. Routes to sub-skills for metrics dashboards,
  retention optimization, onboarding flows, and customer feedback systems.
  Trigger on: "metrics dashboard", "north star metric", "AARRR", "KPIs",
  "retention", "churn", "cohort analysis", "onboarding", "activation",
  "customer feedback", "NPS", "CSAT".
---

# Metrics — Retention & Measurement

Orchestrator for retention and metrics tasks. Routes to the right sub-skill based on your request. All reports are saved to `resources/retention-metrics/`.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/metrics dashboard` | `metrics-dashboard/SKILL.md` | "metrics dashboard", "north star metric", "AARRR", "KPIs", "what to measure" |
| `/metrics retention` | `retention-optimization/SKILL.md` | "retention", "churn", "cohort analysis", "win-back", "keep customers" |
| `/metrics onboarding` | `onboarding-flow/SKILL.md` | "onboarding", "activation", "activation funnel", "product tour", "first-run experience" |
| `/metrics feedback` | `customer-feedback/SKILL.md` | "customer feedback", "NPS", "CSAT", "CES", "feedback loop", "voice of customer" |

## Recommended Flow

Skills chain their outputs (each detects prior reports in `resources/retention-metrics/`):

1. `metrics-dashboard` → define the north star and funnel metrics
2. `onboarding-flow` → optimize activation
3. `retention-optimization` → reduce churn
4. `customer-feedback` → close the loop
