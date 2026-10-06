---
name: strategy
description: >
  Foundation strategy hub. Routes to sub-skills for business idea validation,
  market sizing, business model design, personas, value proposition, positioning,
  and competitive analysis. Trigger on: "validate idea", "business idea",
  "market opportunity", "TAM", "business model", "canvas", "persona",
  "value proposition", "positioning", "competitive analysis", "competitors", "SWOT".
---

# Strategy — Foundation

Orchestrator for foundation strategy tasks. Routes to the right sub-skill based on your request. All reports are saved to `resources/foundation-strategy/`.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/strategy validate` | `business-idea/SKILL.md` | "validate my idea", "business idea validation", "is this idea viable", "go/no-go" |
| `/strategy market` | `market-opportunity/SKILL.md` | "market opportunity", "market size", "TAM SAM SOM", "market analysis" |
| `/strategy model` | `business-model/SKILL.md` | "business model", "business model canvas", "revenue model", "how do we make money" |
| `/strategy persona` | `customer-persona/SKILL.md` | "customer persona", "buyer persona", "target customer", "ideal customer profile" |
| `/strategy value-prop` | `value-proposition/SKILL.md` | "value proposition", "JTBD", "jobs to be done", "why would they buy" |
| `/strategy positioning` | `product-positioning/SKILL.md` | "positioning", "product positioning", "positioning statement", "differentiation" |
| `/strategy competitive` | `competitive-intelligence/SKILL.md` | "competitive analysis", "competitors", "competitive intelligence", "SWOT", "Porter" |

## Recommended Flow

Skills chain their outputs (each detects prior reports in `resources/foundation-strategy/`):

1. `business-idea` → validate before investing time
2. `market-opportunity` → size the market
3. `business-model` → design the model
4. `customer-persona` → know the buyer
5. `value-proposition` → craft the promise
6. `product-positioning` → own a position
7. `competitive-intelligence` → map the battlefield

Then continue in `market/` (pricing, GTM, roadmap) and `growth/`.
