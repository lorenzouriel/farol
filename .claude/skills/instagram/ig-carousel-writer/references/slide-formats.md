# IG Carousel Slide Formats

Five carousel structures for Instagram. Each includes a skeleton and worked example.

---

## Format 1 — Listicle

**Use when:** "N tips/tools/lessons/mistakes about X"

**Length:** 6-10 slides (cover + items + close)

**Structure:**
```
Slide 1 (cover): "[N] [things/tools/reasons] [audience] needs to know about [topic]"
Slide 2 (item 1): [Item name] — [one sentence what it is] + [one sentence why it matters]
Slide 3 (item 2): [Same structure]
...
Slide N-1 (last item): [Same structure, optionally the most surprising one]
Slide N (CTA): [One specific action: save, comment, follow, DM]
```

**Cover slide rules:**
- The number must be specific (7 > "several")
- The audience must be named ("data engineers", not "professionals")
- Don't give away what's on the slides — create curiosity

**Body slide rules:**
- Each slide: item name as headline + 20-50 word body
- Don't assume the reader saw the previous slide (they might screenshot just slide 4)
- Most surprising or counterintuitive item should be mid-carousel, not last (drop-off is highest at end)

**Worked example:**
```
Slide 1: "7 dbt features most data engineers never use"

Slide 2:
Incremental models
You don't need to rebuild your entire table every run. Incremental lets you process only new rows. At scale, this cuts run time from hours to minutes.

Slide 3:
Snapshots
dbt tracks slowly changing dimensions for you. One config file replaces 100 lines of custom SCD logic. Most teams don't know it exists.

...

Slide 8 (CTA):
Save this for your next dbt project.
Or comment "dbt" and I'll send you my starter template.
```

---

## Format 2 — Step-by-Step

**Use when:** Tutorial, process, how-to, workflow

**Length:** 5-8 slides (cover + numbered steps + close)

**Structure:**
```
Slide 1 (cover): "How to [achieve result] in [N steps / X time]"
Slide 2 (step 1): "Step 1: [Action]" + [What you do + what you get at the end of this step]
Slide 3 (step 2): Same structure
...
Slide N-1 (last step): Same structure + common mistake at this step
Slide N (CTA): "Save this" / "Comment [X]" / next-step resource
```

**Rules:**
- Action verb first on each step ("Build", "Configure", "Test", not "The next thing is...")
- Include the OUTPUT of each step, not just the action — readers want to know what they'll have
- At least one step should include "common mistake here:" — readers love the warning

**Worked example:**
```
Slide 1: "How to set up a Medallion Architecture in 5 steps"

Slide 2:
Step 1: Define your layers
Create three schemas: bronze (raw), silver (cleaned), gold (aggregated).
Don't skip the bronze layer — you'll regret not having the raw data when something breaks.

Slide 3:
Step 2: Build your ingestion layer
Raw data lands in bronze as-is. No transformations here. Preserve the source format exactly.
Common mistake: cleaning data in ingestion. That's silver's job.

...

Slide 7 (CTA):
Save this as a reference.
Full architecture diagram → link in bio.
```

---

## Format 3 — Before / After

**Use when:** Transformation, results, comparison, "then vs now"

**Length:** 4-7 slides (cover + before + bridge + after + lesson)

**Structure:**
```
Slide 1 (cover): "Before vs After: [what changed]" or "[X months later, here's what's different]"
Slide 2 (the before): [Specific snapshot of the before state — numbers, details, emotions]
Slide 3 (the bridge): [What changed / the decision / the turning point]
Slide 4 (the after): [Specific snapshot of the after state — equally concrete]
Slide 5 (the lesson): [What anyone else can learn from this]
Slide 6 (CTA): [One action]
```

**Rules:**
- Both before AND after must be specific (numbers, dates, names)
- Avoid: vague befores ("I was struggling") and inflated afters ("everything changed")
- The bridge slide is the most important — it's the actionable part
- The lesson must be replicable, not just inspirational

**Worked example:**
```
Slide 1: "6 months ago vs now — what actually changed"

Slide 2 (before):
January 2025
- 0 inbound leads
- Cold outreach for every client
- Posting 5x/week with no strategy
- 1,200 followers

Slide 3 (bridge):
I stopped posting content. For 3 weeks.
Then I picked one problem I actually solve and started writing only about that.

Slide 4 (after):
July 2025
- 3 inbound leads/month
- 0 cold outreach
- Posting 3x/week with a plan
- 4,100 followers

Slide 5 (lesson):
You don't need more content. You need clearer positioning.
The audience finds you when they know exactly what you're for.

Slide 6 (CTA):
Save this and revisit in 90 days.
```

---

## Format 4 — Breakdown

**Use when:** Explaining a concept, dissecting how something works, making complex accessible

**Length:** 6-10 slides (cover + layers + implication + close)

**Structure:**
```
Slide 1 (cover): "[Concept] explained simply" or "How [X] actually works"
Slide 2 (surface): What most people think it is
Slide 3 (reality): What it actually is
Slide 4-7 (layers): Each slide goes one layer deeper
Slide 8 (implication): What this means for the reader's work/life
Slide 9 (CTA): One action
```

**Rules:**
- Slide 2 (surface) must be generous — state the common understanding fairly before correcting it
- Each "layer" slide builds on the previous; don't repeat or summarize
- Implication slide is mandatory — abstract explanations without "so what" lose readers

---

## Format 5 — Myth-Busting

**Use when:** Correcting misconceptions, taking a contrarian position, reframing a common belief

**Length:** 5-9 slides (cover + myths + truth + close)

**Structure:**
```
Slide 1 (cover): "[N] myths about [topic] (and what's actually true)"
Slide 2 (myth 1): "Myth: [common belief]" → "Truth: [the correction]"
Slide 3 (myth 2): Same structure
...
Slide N-1 (final myth, the most surprising one): Same structure
Slide N (CTA): One action
```

**Rules:**
- Each myth must be something people actually believe (not a strawman)
- The truth correction must be equally sharp — not "well, it depends"
- Order: easiest myths first, hardest (most surprising) myth second-to-last
- Include one myth that the reader probably believed until now (create a small revelation)

---

## CTA slide patterns

| CTA | When |
|---|---|
| "Save this for [specific use case]" | Educational content worth bookmarking |
| "Comment [word] and I'll DM you [specific thing]" | Lead magnet, resource |
| "Which one surprised you most? Comment below." | Discussion-driver, genuine question |
| "Follow for [specific content promise]" | When the carousel is the first touchpoint |
| No CTA — just the strongest final point | When a hard sell would undercut the value |

**Never:** "Like and save if this helped!", "Share with someone who needs this!", or any generic engagement beg.
