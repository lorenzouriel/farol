---
name: google-ad
description: >
  Creates a complete Google Ads campaign structure from a briefing or SEO research.
  Generates CSVs ready to import into Google Ads Editor with Search campaigns organized
  by cluster, ad groups, keywords, RSAs, extensions, and negatives. Use when the user
  asks for a Google Ads campaign.
---

# /google-ad - Google Ads Campaign Structure

Builds the whole campaign as import-ready CSVs for Google Ads Editor. From briefing to CSV — no building ad groups one by one inside the Google interface.

## Context

- **Business context:** `memory/company.md` (product/service, audience, region, differentiators)
- **Tone of voice:** `memory/preferences.md`
- **SEO research if available:** `areas/marketing/seo/01-demand-research.md`, `06-google-ads.md` — use as input
- **Outputs:** `areas/marketing/campaigns/google-ads-<YYYY-MM-DD>/`

---

## Step 1 — Briefing

If no briefing was provided, ask these questions one at a time:

1. **Product/service to advertise?** (1-3 lines)
2. **Who is the audience?** (profile, the problem it solves)
3. **Region:** radius in km from which city?
4. **Daily budget?** ($/day)
5. **Goal:** calls / WhatsApp / form / in-person visit?
6. **Does a site/landing page exist?** URL?

If `areas/marketing/seo/06-google-ads.md` already exists (created by `/content seo`), use it as the base — skip questions already answered there.

## Step 2 — Keyword research

If `areas/marketing/seo/01-demand-research.md` exists, use the top 10-20 priority terms (transactional + commercial intent).

If it does not exist, generate:
- 30-50 seed terms based on the briefing
- WebSearch per group to check competition and seasonality
- Filter to **commercial/transactional intent** — discard informational ("how to X" rarely converts — leave for organic SEO)
- Group into **clusters** (e.g., "pizza-delivery", "pizza-restaurant", "pizza-catering")

## Step 3 — Campaign structure

Recommended structure for local B2B/B2C:

```
Campaign 1: <Business> — General Search
├── Group: <Cluster 1>
│   ├── 10-15 keywords (mix of exact, phrase, broad match modifier)
│   ├── 3 RSAs (15 headlines + 4 descriptions each)
│   └── 10-15 negative keywords in group
├── Group: <Cluster 2>
│   └── ...
└── ... (1 group per cluster from Step 2)

Campaign 2: <Business> — Local (optional)
├── Ads for Google Maps
└── Proximity-based targeting

Global negative keywords list: discarded generic terms, competitor brand names
```

## Step 4 — RSA copy

For each group, generate 3 RSAs (Responsive Search Ads):

**15 headlines per ad (30 chars max each):**
- 5 with the primary keyword
- 3 with concrete differentiators (certifications, turnaround, guarantee)
- 3 with CTA ("Request a quote", "Message on WhatsApp", "Talk now")
- 2 with social proof (years in business, number of clients served)
- 2 with generic value proposition

**4 descriptions (90 chars max each):**
- 1 institutional + CTA
- 1 with technical differentiator + CTA
- 1 with urgency/scarcity (if applicable)
- 1 with social proof + CTA

**Google's hard rules:**
- Headline: 30 characters max
- Description: 90 characters max
- No emojis, no ALL CAPS, no word repetition across headlines
- No unverified superlatives ("the best", "#1") without a source

Copy strictly follows `memory/preferences.md`. No marketing jargon if the audience doesn't use it.

## Step 5 — Extensions

Generate separate CSVs for each extension type:

- **Sitelinks** (4-6): "About us", "Services", "Case studies", "WhatsApp", "Location"
- **Callout:** short differentiators — "Free estimate", "Licensed & insured", "Same-day response"
- **Structured snippets:** services list, product categories
- **Call:** pull phone from `memory/company.md`
- **Price** (if applicable): price ranges for main services
- **Promotion** (if applicable): discount, special condition

## Step 6 — Campaign settings

Generate `settings.md` with:

- **Bid strategy:** "Maximize conversions" to start (migrate to "Target CPA" after 30+ conversions)
- **Daily budget:** from briefing
- **Geographic targeting:** km radius from business address
- **Language:** English (or match audience language)
- **Device adjustments:** mobile +0%, desktop +0%, tablet -20%
- **Schedule:** days and hours matching business hours
- **Conversions to configure:** WhatsApp click, form submission, phone call, time on site

## Step 7 — Generate the CSVs

Final folder structure:

```
areas/marketing/campaigns/google-ads-<YYYY-MM-DD>/
  campaigns.csv           ← one row per campaign
  ad-groups.csv           ← one row per ad group
  keywords.csv            ← keywords + match type
  keywords-negatives.csv  ← negatives per group + global list
  ads-rsa.csv             ← RSAs (headlines + descriptions)
  extensions-sitelinks.csv
  extensions-callouts.csv
  extensions-snippets.csv
  extensions-price.csv    (if applicable)
  settings.md             ← config + pre-launch checklist
  README-import.md        ← step-by-step import guide for Google Ads Editor
```

**CSV format:** follow Google Ads Editor import standard — columns: Campaign, Ad group, Keyword, Match type, Status, Max CPC, Final URL, etc. Every CSV must be valid for spreadsheet review before import.

## Step 8 — Summary

Show the user:

```
✓ Campaign ready: areas/marketing/campaigns/google-ads-<YYYY-MM-DD>/

Structure:
  <N> campaigns
  <N> ad groups
  <N> positive keywords
  <N> negative keywords
  <N> RSAs

To launch:
1. Open Google Ads Editor (desktop app)
2. Account → Import → CSV
3. Upload campaigns.csv first, then ad-groups, keywords, ads, extensions
4. Review status (everything starts PAUSED — activate manually after review)
5. Confirm conversions are configured in Google Tag Manager
6. Activate campaign only when everything checks out

Suggested starting budget: $<X>/day for <Y> days before evaluating results.
```

---

## Rules

- **Never invent CPC data.** If asked about cost, say it depends on real competition and give a range from WebSearch.
- **Always start paused.** The user reviews and activates after approving.
- **Do not advertise informational terms.** "How to X" rarely converts — leave for organic SEO.
- **Match types:** start with Phrase Match for most terms. Exact Match for premium terms. Broad Match only with consistent performance data.
- **Global negative list is mandatory.** Without it, budget burns on irrelevant searches.
- **Conversions before everything.** Without conversion tracking, Google cannot optimize. Flag this and ask for setup before the campaign goes live.
