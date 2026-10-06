---
name: fundraising
description: >
  Fundraising and operations hub. Routes to sub-skills for financial modeling,
  fundraising strategy, investor briefs, pitch decks, and operational playbooks.
  Trigger on: "financial model", "projections", "fundraising", "raise money",
  "investors", "term sheet", "investor brief", "one-pager", "pitch deck",
  "operational playbook", "org structure", "OKRs".
---

# Fundraising — Capital & Operations

Orchestrator for fundraising and operations tasks. Routes to the right sub-skill based on your request. All reports are saved to `resources/fundraising-operations/`.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/fundraising model` | `financial-model/SKILL.md` | "financial model", "projections", "3-year forecast", "unit economics", "scenarios" |
| `/fundraising strategy` | `fundraising-strategy/SKILL.md` | "fundraising", "raise money", "raise a round", "investor targeting", "term sheet" |
| `/fundraising brief` | `investor-brief/SKILL.md` | "investor brief", "one-pager", "investor email", "teaser" |
| `/fundraising deck` | `investor-pitch-deck/SKILL.md` | "pitch deck", "investor deck", "pitch presentation", "slides for investors" |
| `/fundraising playbook` | `operational-playbook/SKILL.md` | "operational playbook", "org structure", "company OKRs", "processes", "SOPs" |

## Recommended Flow

Skills chain their outputs (each detects prior reports in `resources/fundraising-operations/`):

1. `financial-model` → build the numbers
2. `fundraising-strategy` → plan the raise
3. `investor-brief` → open doors
4. `investor-pitch-deck` → close the round
5. `operational-playbook` → run the company
