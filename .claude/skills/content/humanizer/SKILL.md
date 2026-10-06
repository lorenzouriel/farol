---
name: social-humanizer
description: Unified humanizer for all social media content — LinkedIn posts, X tweets/threads, Instagram captions/carousel slides/Reel scripts, and TikTok scripts. Auto-detects platform from text shape and applies universal AI-tell scrub rules (30 Wikipedia patterns) plus platform-specific rules on top. Tiered: forensic / strict / aesthetic / audit. Replaces running ig-humanizer, linkedin-humanizer, and tiktok-humanizer separately.
---

# Social Humanizer

One skill. All platforms. Universal AI-tell removal first, then platform-specific scrub on top.

Based on the Wikipedia "Signs of AI writing" taxonomy (30 patterns) extended with LinkedIn, Instagram, TikTok, and X-specific tells collected from 2025-2026 platform audits.

## When to use

- Before posting any AI-drafted social content
- When a post "feels off" but you can't pinpoint why
- Audit mode: check if a draft passes the human-sounding test without rewriting
- Replacing: `linkedin-humanizer`, `ig-humanizer`, `tiktok-humanizer`

## Platform auto-detection

If no platform is specified, the skill detects it from the text:

| Signal | Detected as |
|---|---|
| ≤280 chars, or `1/` `2/` thread format, or `@handle` patterns | X (tweet / thread) |
| 900-1800 chars, professional tone, career/business topic | LinkedIn |
| "Link in bio", "swipe", emoji clusters, visual reference | Instagram caption |
| Timing cues `[0:00]`, `On-screen:`, `Spoken:`, or conversational spoken-word rhythm | TikTok script |
| Slide structure (Slide 1 / Slide 2...) | Instagram carousel |
| None of the above | General (universal rules only) |

## Modes

```
# Default: auto-detect platform, forensic + strict tiers
social-humanizer <text>

# Force platform
social-humanizer --platform linkedin <text>
social-humanizer --platform x <text>
social-humanizer --platform ig <text>
social-humanizer --platform tiktok <text>

# Tier control
social-humanizer --mode forensic <text>     # Model leakage only
social-humanizer --mode strict <text>       # Forensic + platform corporate-speak
social-humanizer --mode aesthetic <text>    # Strict + style rules (em dash, rule-of-three)
social-humanizer --mode audit <text>        # Detection only — no rewrite

# Voice calibration
social-humanizer --voice-sample <path_or_inline> <text>
```

## Two-layer architecture

### Layer 1 — Universal scrub (all platforms, always)

30 patterns from the Wikipedia "Signs of AI writing" taxonomy. Applied regardless of platform. See `references/universal-scrub-rules.md`.

Key universal rules:
- AI tool markers (oaicite, contentReference, grok_card, etc.)
- Knowledge-cutoff disclaimers ("As of my last update...")
- Phrasal templates ([Your Name], [Insert X], 202X-XX-XX)
- Em dash overuse (3+ in < 300 words = forensic; single use = aesthetic)
- AI vocabulary: delve, leverage, utilize, foster, harness, seamless, holistic, nuanced, tapestry, vibrant, testament, pivotal, underscore, highlight (verb), garner, showcase
- Filler adverbs: fundamentally, essentially, ultimately, crucially, notably, arguably
- Rule of three overuse (3 adjectives, 3 parallel clauses)
- Negative parallelisms ("It's not just X, it's Y" / "Not X, but Y")
- Passive voice + subjectless fragments
- Vague attributions ("experts say", "industry observers note", "some argue")
- Outline closers ("In conclusion", "To summarize", "Looking ahead")
- Generic positive conclusions ("The future looks bright", "Exciting times ahead")
- Filler phrases ("In order to", "Due to the fact that", "At this point in time")
- Excessive hedging ("could potentially possibly be argued")
- Sycophantic tone ("Great question!", "You're absolutely right!")
- Collaborative artifacts ("I hope this helps", "Would you like me to expand")
- Significance inflation ("pivotal moment", "testament to", "marks a shift")
- Promotional language ("vibrant", "breathtaking", "nestled", "groundbreaking")
- Copula avoidance ("serves as", "stands as", "boasts", "features")
- Emoji decorating bullet points or headers
- Curly quotation marks ("" → "")
- Bold overuse (**every** phrase bolded)
- Superficial -ing analyses ("highlighting how X contributes to Y")
- Diff-anchored writing ("This was added to replace the previous approach")
- Signposting ("Let's dive in", "Here's what you need to know", "Without further ado")

### Layer 2 — Platform scrub (applied after Layer 1)

Platform-specific patterns that Layer 1 doesn't cover. See `references/platform-scrub-rules.md`.

**LinkedIn additions:**
- Negative parallelism full ban (all 6 forms per 2026-04-27 update)
- Engagement bait: "What do you think?", "Tag someone who needs this", "Drop a comment below"
- Announcement openers: "I'm excited to announce", "Honored to be featured", "Thrilled to share"
- CTA closers: "Let me know in the comments!", "Share your thoughts below!"
- Algorithm tells: external links in post body, 3+ hashtags in body

**Instagram additions:**
- Emoji spam: 3+ consecutive unrelated emoji, emoji at end of every line
- Generic engagement bait: "Double tap if you agree!", "Save this post!", "Let me know in the comments!"
- Caption tells: "Here I am at [place]..." (describes image), "In today's post I'm sharing..."
- Weak authority vocab: "curated", "authentic", "vibe", "aesthetic" as empty adjectives, "content creator" as self-description
- "Link in bio!" without specifying what's there
- Carousel: slides all same length, bullet lists inside a single slide

**TikTok additions:**
- Presenter openers: "Hey guys", "Welcome back", "So today I wanted to talk about", "In this video I will"
- YouTube-leak CTAs: "Don't forget to like and subscribe!", "Hit that follow button!"
- Filler: "So basically", "You know what I mean?", "And that wraps up today's video"
- Uniform sentence rhythm (all 12-18 words = scripted tell)
- List-reading voice (every item "Number N: [identical structure]")
- Scripted transitions: "Moving on to our next point", "As I mentioned earlier"

**X additions:**
- Engagement bait: "RT if you agree", "Follow me for more content like this"
- External link in tweet body (algorithm penalty signal)
- Hashtag body spam (hashtags mid-tweet)
- Hedge openers: "I think maybe...", "Some might say..."

## The three passes

### Pass 1 — SCRUB

Apply Layer 1 universal rules, then Layer 2 platform rules. Delete or replace each flagged pattern. Full patterns in `references/universal-scrub-rules.md` and `references/platform-scrub-rules.md`.

### Pass 2 — BREAK (burstiness)

**For all written text (LinkedIn, X, IG captions):**
- No two consecutive sentences the same length
- At least 1 sentence fragment per 100 words ("Worth it.", "Every time.", "Still does.")
- Break any perfect parallel structure with one asymmetric sentence
- Target: Flesch reading ease > 55

**For spoken scripts (TikTok, IG Reels):**
- Alternate short punches (under 6 words) and longer sentences
- Add natural speech markers: "Right?", "Here's the thing:", "Seriously.", "No joke."
- Add `[beat]` cues where natural pauses belong
- Read aloud at 130-150 WPM — cut if over length, don't speed up delivery

**For carousel slides:**
- Not all slides same length
- At least 1 slide with only a headline + one-sentence body
- No bullet lists inside a single slide

### Pass 3 — ADD (human fingerprints)

Per 100 words of text (or per 30 seconds of script):
- 1 specific number (replace "many", "a lot", "tons of")
- 1 named entity (real person, company, tool, date, place)
- 1 first-person concrete detail
- 1 moment of genuine opinion or mild vulnerability

If missing, ask the user for the specific. Never fabricate.

## Voice calibration

If the user provides a writing sample:
1. Read it first. Note: sentence length patterns, word choice level, paragraph start habits, punctuation quirks, verbal tics.
2. Match their voice in the rewrite — don't just remove AI patterns, replace with patterns from the sample.
3. Preserve: intentional lowercase starts, `..` soft pauses, sentence fragments used deliberately, contractions, specific numbers and named entities.

## Output

- Rewritten copy with all tells removed
- Diff summary: what changed and which rule triggered it
- Platform detected (if auto-mode)
- Tier applied
- Confidence: "human", "mixed", "AI-likely"
- For scripts: read-aloud timing estimate (word count / 130 WPM)

## Non-negotiables (all platforms)

- Preserve the user's actual claim — humanizing does not change meaning
- Never introduce facts not in the input
- Keep the user's voice quirks
- Specific numbers and named entities: add more, never remove
- If a required human fingerprint is missing, ask — don't invent

## Files

- `SKILL.md` — this file
- `references/universal-scrub-rules.md` — 30 Wikipedia AI-tell patterns with regex/replacement logic
- `references/platform-scrub-rules.md` — platform-specific additions (LinkedIn / X / Instagram / TikTok)
- `references/voice-fingerprint.md` — how to preserve user voice while scrubbing

## Related skills

**Write before humanizing:**
- `linkedin-post-writer`, `x-tweet-writer`, `x-thread-writer`
- `ig-caption-writer`, `ig-carousel-writer`, `ig-reel-script-writer`
- `tiktok-script-writer`, `tiktok-hook-writer`

**Plan before writing:**
- `social-content-planner` — unified weekly calendar across all platforms
