---
name: seo
description: >
  Complete SEO, GEO, and Google Ads flow in 8 steps: demand research, competition,
  Google Business Profile, on-page optimization, content strategy, Google Ads,
  monitoring, and AI-answer optimization. Use when the user asks for SEO, GEO,
  keywords, Google Ads, Google Business Profile, competitor SEO analysis, niche
  research, or Google Trends.
---

# /seo - 8-Step SEO + GEO + Ads Flow

## Context

- **Business context:** `memory/company.md`
- **Tone of voice:** `memory/preferences.md`
- **Current strategy:** `memory/strategy.md`

## Step 1 - Demand: What People Search For

Read `memory/company.md` and extract products/services, region, audience, differentiators, and use cases.

Research keyword groups:

- Direct product/service terms
- Problem/symptom terms
- Local terms
- Comparison/decision terms
- Informational terms

For each term, record intent, relevance, funnel stage, and suggested use.

**Output:** `areas/marketing/seo/01-demand-research.md`

## Step 2 - Competition: Who Shows Up

Use the top 10 terms from Step 1. For each term, use WebSearch/WebFetch to inspect:

- SERP type
- Local pack / Maps competitors
- Competitor pages, titles, headings, offers, proof, content depth
- Google Business Profile quality
- Minimum benchmark the business must reach

**Output:** `areas/marketing/seo/02-competition-analysis.md`

## Step 3 - Google Business Profile

Research the current profile if it exists. Create a document with:

- Business description
- Categories
- Services/products
- Photos checklist
- Posts ideas
- Review request strategy
- Reply templates using `/reply-reviews`

**Output:** `areas/marketing/seo/03-google-business-profile.md`

## Step 4 - On-Page Optimization

For the existing site or planned pages, create:

- URL structure
- Title tags and meta descriptions
- H1/H2/H3 structure
- Internal links
- Schema markup suggestions
- Page-specific recommendations

**Output:** `areas/marketing/seo/04-on-page-optimization.md`

## Step 5 - Content Strategy

Build an authority plan from informational and commercial terms:

- Pillar page
- Satellite articles
- Content clusters
- Suggested titles, target keyword, heading structure, and size estimate

**Output:** `areas/marketing/seo/05-content-strategy.md`

This list feeds `/publish-topic`: each item can become a blog post + carousel + captions.

## Step 6 - Google Ads

Structure campaign recommendations from the research:

- Campaign goal
- Campaign/ad group structure
- Keyword groups
- Negative keywords
- RSA angles
- Extensions
- Landing page recommendations

**Output:** `areas/marketing/seo/06-google-ads.md`

The `/google-ad` skill consumes this file and generates import-ready CSVs.

## Step 7 - Monitoring

Create a monthly checklist:

- Google Search Console metrics
- Google Business Profile metrics
- Review replies
- Google Ads metrics
- Content updates
- Competitor refresh
- Next actions

**Output:** `areas/marketing/seo/07-monitoring-checklist.md`

## Step 8 - GEO: Appear In AI Answers

Optimize presence so generative AIs cite the company when users ask about the niche:

- Test prompts in ChatGPT/Gemini/Perplexity/Copilot when possible
- Add direct-answer sections to content
- Create FAQ + schema suggestions
- Include concrete verifiable facts
- Track whether the company appears, who appears, and cited sources

**Output:** `areas/marketing/seo/08-ai-geo-optimization.md`

## Execution

When running `/seo`, execute all 8 steps in sequence and save each output to the corresponding file. Between steps, show a short summary of what was found.

If the user wants only one step, allow `/seo step 3`, `/seo gmb`, or `/seo geo`.

## Rules

- Research must be real. Use WebSearch/WebFetch; never invent volume or competition data.
- Copy and text follow `memory/preferences.md`.
- If data is uncertain, say so.
- For local B2B/B2C, prioritize commercial/transactional intent.
