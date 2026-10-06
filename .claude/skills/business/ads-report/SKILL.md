---
name: ads-report
description: >
  Generates a weekly paid ads performance report (Google Ads + Meta Ads). Reads CSV
  exports, compares with the previous period when possible, and returns an executive
  summary with alerts and recommendations. Use when the user asks for an ads report.
---

# /ads-report - Weekly Google Ads + Meta Ads Report

Turns raw platform exports into an executive report the owner can understand without opening Google or Meta.

## Context

- **Context:** `memory/company.md`, `memory/strategy.md`
- **Tone of voice:** `memory/preferences.md`
- **History:** `areas/marketing/campaigns/reports/` (create if missing)

## How to run

Expected files can be in `inbox/`, for example:

```text
inbox/google-ads-2026-05-12.csv
inbox/meta-ads-2026-05-12.csv
```

Then run:

```text
/ads-report
```

If files are missing, ask where the week's exports are.

## Flow

1. Read exports and identify date range, platform, campaign/ad group names, spend, impressions, clicks, conversions, CPA, CTR, CPC, CPM, and revenue when available.
2. Look for the previous report in `areas/marketing/campaigns/reports/` and calculate week-over-week changes when possible.
3. Write an executive summary with what improved, what worsened, biggest risk, and next action.
4. Detail performance by channel.
5. Generate automatic alerts for high spend without conversions, rising CPA, low CTR, low conversion rate, fatigue, and winners worth scaling.
6. Recommend concrete next actions for the next week.
7. Save in:

```text
areas/marketing/campaigns/reports/<YYYY-MM-DD>-report.md
```

8. Show the executive summary in chat and point to the full file.

## Rules

- Never invent numbers.
- If the export is truncated or unreadable, say "incomplete data" and proceed only with what is available.
- Concrete recommendations: "Pause Group X" beats "optimize campaigns".
- Follow `memory/preferences.md` for language.
- When reporting loss, be direct.
