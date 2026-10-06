---
name: analyze-data
description: >
  Analyzes a data file (CSV, Excel, TXT, JSON) and generates an executive summary
  with findings, risks, and recommended actions. Use when the user says "analyze this file",
  "what does this data show", "summarize these results", or provides a data file.
---

# /analyze-data - File Analysis

## Context to read

- **Business context:** `memory/company.md` (to understand what the data represents)
- **Tone of voice:** `memory/preferences.md`

## Flow

### Step 1 - Understand the context

If the user did not explain the file, ask up to two questions:

- "What is this file? (sales, ads, metrics, survey responses...)"
- "What is the main question you want to answer with this data?"

If the context is obvious from the filename or content, proceed without asking.

### Step 2 - Read the file

Read the provided file. If it is Excel (.xlsx), use the available tools to extract cell content.

### Step 3 - Analyze

Always look for:

**What is good:**
- Positive patterns in the data
- Top performers (products, campaigns, periods, etc.)
- Signals that something is working

**What is concerning:**
- Drops, anomalies, outliers
- What is below expectations
- Missing or inconsistent data

**What to do next:**
- 3 to 5 concrete recommendations
- What to stop, continue, and test

### Step 4 - Output

Write in clear executive language:

```markdown
# Analysis - [file/context name]

## Executive Summary
[3 to 5 bullets with what matters most]

## What This Data Shows
[plain-language explanation]

## What Is Working
[specific points]

## What Needs Attention
[specific points]

## Recommendations
1. [action]
2. [action]
3. [action]

## Notes / Limitations
[missing data, assumptions, caveats]
```

Save in `resources/documents/analyses/analysis-[name]-[date].md` or the most appropriate folder for the user's profile.

## Rules

- Never invent data that is not in the file.
- If the data is incomplete or problematic, say that before analyzing.
- Follow `memory/preferences.md` for tone.
- Prefer prose with tables only where they improve clarity.
