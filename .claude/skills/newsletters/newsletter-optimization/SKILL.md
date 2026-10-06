---
name: newsletter-optimization
description: Optimize Substack articles for AI Engine citation. Takes a draft, scores it 0-100 for AI discoverability, then restructures it section-by-section with answer capsules, question headings, and clean extraction patterns. Score → Optimize → Score Again.
---

# AEO Optimization - Score, Restructure, Score Again

**Philosophy:** AI models don't read like humans. They scan for extractable patterns. Restructure your content so ChatGPT, Perplexity, Claude, and Gemini can find, extract, and cite it.

**Key Stats:**
- 60% of Google searches end without a click (AI Overviews, snippets)
- 25% of search volume shifting to AI chatbots by 2026 (Gartner)
- Only 11% of websites get cited by both ChatGPT and Perplexity
- Content with answer capsules gets cited **3x more often**

---

## What This Skill Does

**3-step process:**

1. **SCORE** — Analyze the draft's AI-citation readiness, give AEO Score out of 100
2. **RESTRUCTURE** — Rewrite the article section by section for AI extraction
3. **SCORE AGAIN** — Show the new score with before/after comparison

**What gets restructured:**
- Every H2 gets a 50-80 word answer capsule INSERTED right after the heading
- Headings get question format (structure/numbering stays: "Step 1:" → "Step 1: How Do I...?")
- Links inside answer capsule zones moved to supporting text below
- Paragraphs over 100 words split at natural break points
- Keyword-stuffed sentences get semantic variations
- Intro/subtitle can be tweaked for keyword placement (first 100 words)

---

## CRITICAL: Optimization Rules

**The principle: Do everything AEO requires. Don't add anything AEO doesn't require.**

**DO — these are necessary AEO changes:**
- Add answer capsule (50-80 words) after each H2 heading — this is new content, the core of AEO
- Convert headings to question format: "Step 1: Create Bot" → "Step 1: How Do I Create a Telegram Bot?"
- Move links out of answer capsule zones into supporting text below
- Split paragraphs over 100 words at natural break points
- Replace keyword stuffing with semantic variations
- Tweak intro/subtitle for keyword placement if needed

**DON'T — these add no AEO value:**
- Adding filler sentences or paragraphs beyond answer capsules
- Rewriting existing paragraphs that are already fine
- Adding new explanatory content the author didn't write
- Changing the article structure (Step order, section order)
- Changing the author's voice or writing style
- Removing the author's content

---

## When to Use

- **Before publishing** any Substack article
- **After writing** the draft
- **Before SEO optimization** (AEO first, then `/seo-optimization`)

**Workflow:**
1. LetsDecide → validate title
2. LetsStart → build structure
3. Write article
4. **`/aeo-optimization` → restructure for AI engines** (you are here)
5. `/seo-optimization` → optimize for Google
6. Publish

---

## Usage

```
/aeo-optimization [paste draft or provide file path]
```

If article is paid/paywalled, mention it:
```
/aeo-optimization [draft] (paid article, paywall after Part 2)
```

---

## Step 1: AEO SCORE (Before Optimization)

Analyze the draft and calculate AEO Score out of 100.

### Scoring Breakdown (100 points total)

| Category | Max Points | What's Measured |
|----------|-----------|-----------------|
| **Answer Capsules** | 30 | Does every H2 have a 50-80 word direct answer immediately after it? Complete, standalone, no preamble? |
| **Question-Based Headings** | 20 | Do H2s start with How/What/Why/When/Which? Are they specific? Natural language? |
| **Link Hygiene** | 15 | Zero hyperlinks inside answer capsules? Links only in supporting text below? |
| **Paragraph Structure** | 15 | All paragraphs under 100 words? One idea per paragraph? Easy to chunk-extract? |
| **Semantic Clarity** | 10 | Natural language? No keyword stuffing? Semantic variations used? |
| **Paywall Position** | 10 | (If paid) Are answer capsules in the free preview? Is free preview standalone valuable? (If free article: auto 10/10) |

### Why This Point Distribution?

Answer capsules get 30 points because they're the **#1 citation driver**. An article with perfect capsules but mediocre everything else will still get cited. An article with zero capsules but perfect everything else will get ignored by AI.

### Score Interpretation

| Score | Citation Readiness | Action |
|-------|-------------------|--------|
| **90-100** | HIGH — AI models will likely cite this | Publish |
| **70-89** | GOOD — Citeable with minor gaps | Quick fixes, then publish |
| **50-69** | MEDIUM — Some sections citeable, others invisible | Needs restructuring |
| **30-49** | LOW — AI will mostly skip this | Major restructuring needed |
| **0-29** | INVISIBLE — Zero citation potential | Rewrite with AEO structure |

### Score Output Format

```
═══════════════════════════════════════════
  AEO SCORE (BEFORE): XX/100
═══════════════════════════════════════════

BREAKDOWN:
  Answer Capsules:        XX/30  [X/Y sections have capsules]
  Question Headings:      XX/20  [X/Y headings are questions]
  Link Hygiene:           XX/15  [X links found inside answer zones]
  Paragraph Structure:    XX/15  [X paragraphs over 100 words]
  Semantic Clarity:       XX/10  [natural / some stuffing / heavy stuffing]
  Paywall Position:       XX/10  [N/A / capsules before paywall / capsules hidden]

SECTION-BY-SECTION:
  H2: "[heading text]"
    - Capsule: ❌ missing / ✅ exists (XX words)
    - Question format: ❌ statement / ✅ question
    - Links in answer zone: ❌ X found / ✅ clean
    - Extractable: ❌ NO / ✅ YES

  H2: "[heading text]"
    - Capsule: ...
    ...

CRITICAL ISSUES:
  1. [biggest structural problem]
  2. [second problem]
  3. [third problem]

═══════════════════════════════════════════
```

---

## Step 2: RESTRUCTURE (Section by Section)

After scoring, restructure the article. Output the full optimized article.

### 2A: Answer Capsule Creation

**This is the core of AEO optimization.**

For every H2 section, write or fix the answer capsule.

**The Pattern (non-negotiable):**
```markdown
## [Question-Based Heading]

**[50-80 word answer capsule. Direct answer. No preamble. No "Well, first..." 
No "Let me explain..." No links. Complete and standalone. A reader (or AI model) 
should understand the answer without reading anything else on the page.]**

[Now the supporting content: stories, examples, links, details, personality.
This is where Gencay's voice lives. The capsule is clinical. Everything 
below it is human.]
```

**The 50-80 Word Sweet Spot:**
- Under 50 → Too brief, AI skips it (not enough context)
- 50-80 → AI extracts it cleanly, cites it confidently
- Over 80 → Too dense, AI often truncates or skips

**What makes a GOOD capsule:**
- Answers the heading question directly
- Contains specific numbers/facts when possible
- Self-contained (makes sense without the rest of the article)
- No hedging ("might", "could", "it depends") — be direct
- No links, no formatting except bold

**What makes a BAD capsule:**
- Starts with "Well," "So," "Let me explain" (preamble)
- References other parts of the article ("as I mentioned above")
- Contains hyperlinks
- Too vague ("There are many ways to do this")
- Just restates the heading as a sentence

**Real Example — BEFORE:**
```markdown
## Newsletter Growth Strategies

There are many ways to grow your newsletter. In this section, 
I'll walk you through some of the best strategies I've found 
over the years. Let's start with the basics...
```

**Real Example — AFTER:**
```markdown
## What's the fastest way to get your first 1,000 newsletter subscribers?

**Create one high-value lead magnet, publish weekly for 90 days, and 
promote each post on 2-3 platforms where your target audience gathers. 
Cross-promote with 2 similar-sized newsletters monthly. This system 
typically generates 20-50 new subscribers per week, reaching 1,000 
in roughly 3-4 months without paid advertising.**

There are many ways to grow your newsletter, but after testing dozens 
of strategies, this system consistently outperforms everything else. 
Let me walk you through each step...
```

Notice: The existing content didn't get deleted. It moved BELOW the capsule. The capsule is new — a concentrated answer that AI can extract.

---

### 2B: Heading Transformation

Convert every H2 from statement → question.

**Transformation Rules:**
- Start with How/What/Why/When/Which
- Use the exact phrases people type into ChatGPT/Perplexity
- Be specific (not "How to use AI" but "How do I build an AI agent with Claude Code?")
- Keep it natural — if it sounds weird as a question, rephrase

**Common Transformations:**

| Statement Heading | Question Heading |
|-------------------|-----------------|
| "Getting Started" | "How do I get started with [topic]?" |
| "Key Features" | "What are the most useful features of [tool]?" |
| "Setup Guide" | "How do I set up [tool] step by step?" |
| "Best Practices" | "What mistakes should I avoid when using [tool]?" |
| "Results" | "What results can I expect from [approach]?" |
| "Pricing" | "How much does [tool] cost and is it worth it?" |
| "Tips & Tricks" | "What hidden features make [tool] 10x more powerful?" |
| "Conclusion" / "Final Thoughts" | KEEP AS-IS (not every heading needs to be a question) |

**Exception:** Conclusion/Final Thoughts/CTA sections stay as statements. Only content H2s become questions.

---

### 2C: Link Cleanup

Move all links OUT of answer capsule zones.

**Answer capsule zone** = the bold text immediately after an H2 heading (the 50-80 word block).

**Process:**
1. Find links inside capsules
2. Remove the link but keep the text mention
3. Move the actual hyperlink to the supporting paragraph below

**Before:**
```markdown
## How do I automate my workflow?

**Use [Claude Code](https://claude.ai) to build agents that handle 
repetitive tasks. Check out my [automation guide](link) for details.**
```

**After:**
```markdown
## How do I automate my workflow?

**Use Claude Code to build agents that handle repetitive tasks. 
A single agent can process data, write reports, and send notifications 
autonomously. Most automations take under 30 minutes to set up 
and save 5-10 hours per week on recurring work.**

For a deeper dive, check out my [complete automation guide](link). 
And if you're new to Claude Code, [this tutorial](link) covers setup...
```

---

### 2D: Paragraph Splitting

Break any paragraph over 100 words into shorter chunks.

**Rules:**
- One idea per paragraph
- Target: 60-100 words
- Natural break points (topic shifts, new examples, new concepts)
- Don't split mid-thought — find the logical seam

**Why AI cares:** AI models extract information in chunks. A 200-word paragraph = one giant blob that's hard to extract from. Four 50-word paragraphs = four clean, extractable facts.

---

### 2E: Semantic Cleanup

Replace keyword stuffing with natural variations.

**Before (stuffed):**
```
Claude Code is the best tool. Claude Code can build apps. 
Claude Code supports MCP. With Claude Code you can...
```

**After (semantic):**
```
Claude Code is the best tool for AI-assisted development. 
This coding assistant can build full applications from a single prompt. 
It supports MCP for external integrations. With Anthropic's CLI, you can...
```

Variations: tool name → "this coding assistant", "the CLI", "Anthropic's tool", "it"

---

### 2F: Paywall Adjustment (Paid Articles Only)

If the article is paywalled, ensure:

1. **At least 2-3 answer capsules appear BEFORE the paywall**
2. **Free preview is 300-500 words of genuine value** (not a teaser)
3. **The first capsule directly answers the main topic question**

**Why:** AI crawlers and Google only see the free preview. If all your capsules are behind the paywall, they're invisible.

**Strategy:**
- Paywall after Part 2 or Part 3 (not Part 1)
- Free section should have standalone value
- Position paywall as "going deeper" not "withholding the answer"

---

## Step 3: AEO SCORE (After Optimization)

Score the restructured version using the same 100-point system.

### Final Output Format

```
═══════════════════════════════════════════
  BEFORE/AFTER COMPARISON
═══════════════════════════════════════════

                          BEFORE    AFTER
  Answer Capsules:        XX/30  →  XX/30
  Question Headings:      XX/20  →  XX/20
  Link Hygiene:           XX/15  →  XX/15
  Paragraph Structure:    XX/15  →  XX/15
  Semantic Clarity:       XX/10  →  XX/10
  Paywall Position:       XX/10  →  XX/10
  ─────────────────────────────────────────
  TOTAL:                 XX/100  →  XX/100

═══════════════════════════════════════════

SECTION-BY-SECTION CAPSULE REVIEW:

  H2: "How do I [question]?"
    ✅ Capsule: 67 words, clean, self-contained
    
  H2: "What makes [topic] different?"
    ✅ Capsule: 54 words, clean, self-contained

  H2: "Why should I use [approach]?"
    ✅ Capsule: 72 words, clean, self-contained

  [... all sections listed]

AI CITATION TEST:
  Ask these questions in ChatGPT/Perplexity to check if you get cited:
  1. "[question from H2 #1]"
  2. "[question from H2 #2]"
  3. "[question from H2 #3]"

PAYWALL STATUS: [N/A / X capsules in free preview / all capsules visible]

═══════════════════════════════════════════
```

---

## How to Verify AEO is Working

### Free (Do Monthly)
1. **HubSpot AEO Grader** — Checks visibility across GPT-4o, Perplexity, Gemini
2. **Manual test** — Copy each H2 question from your article, paste into ChatGPT and Perplexity, check if your content gets cited

### Paid (When Serious)
- **Profound** — Multi-platform AI citation tracking
- **OmniSEO** — ChatGPT and Perplexity visibility

### Monthly Routine
1. Pick 5 published articles
2. Take their H2 questions
3. Ask those questions in ChatGPT + Perplexity
4. Track: cited / not cited / partially cited
5. Double down on cited topics, restructure uncited ones

---

## Complete Execution Flow

```
User: /aeo-optimization [draft]
                │
                ▼
    ┌──── STEP 1: SCORE ────┐
    │ Analyze draft structure │
    │ Check each H2 section   │
    │ Calculate AEO Score     │
    │ Show XX/100             │
    │ List structural issues  │
    └───────────┬─────────────┘
                │
                ▼
    ┌──── STEP 2: RESTRUCTURE ─┐
    │ 2A: Write/fix capsules    │
    │   (50-80 words per H2)    │
    │ 2B: Headings → questions  │
    │ 2C: Remove links from     │
    │     capsule zones         │
    │ 2D: Split long paragraphs │
    │ 2E: Semantic cleanup      │
    │ 2F: Paywall adjustment    │
    │                           │
    │ OUTPUT: Full restructured │
    │ article (copy-paste)      │
    └───────────┬───────────────┘
                │
                ▼
    ┌──── STEP 3: SCORE ────┐
    │ Score restructured ver. │
    │ Show before/after       │
    │ Section-by-section      │
    │ AI citation test Qs     │
    └─────────────────────────┘
```

---

## The Key Difference: SEO vs AEO

| | SEO | AEO |
|---|-----|-----|
| **Goal** | Rank on Google | Get cited by AI models |
| **How** | Keywords, meta tags, links | Structure, answer capsules, question patterns |
| **What changes** | Title, meta, slug, keyword placement | Content structure, heading format, answer blocks |
| **Measurement** | Google Search Console rankings | Manual AI queries + HubSpot AEO Grader |
| **Skill** | `/seo-optimization` | `/aeo-optimization` (this one) |

**They reinforce each other.** Answer capsules also win Google featured snippets. Question headings also improve SEO. Run AEO first, then SEO — the optimizations stack.

---

## Data Sources

- **AEO Research:** Sharyph's Dual Discovery Engine Framework
- **Citation Data:** 11% of websites cited by both ChatGPT and Perplexity (Josh Blyskal / Profound)
- **Performance Data:** `stats/substack-article-statistics.csv`

---

## Notes

- **Answer capsules = 30 points for a reason** — They're the #1 citation driver by far
- **Don't touch the voice** — Capsules are clinical, everything below them is Gencay's personality
- **Questions must be natural** — If it sounds weird as a question, it's wrong
- **No links in capsules, period** — This is the most common mistake
- **Paywall kills AEO** — If capsules are behind paywall, AI can't see them
- **Test monthly** — Copy H2 questions into ChatGPT/Perplexity to verify citations
- **95% of creators don't do this** — That's your advantage window

Updated: April 2026
