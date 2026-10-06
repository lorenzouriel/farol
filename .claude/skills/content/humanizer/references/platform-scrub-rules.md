# Platform Scrub Rules

Applied AFTER universal-scrub-rules.md. Each platform block adds patterns specific to that platform's culture, format, and algorithm expectations.

---

## LinkedIn

### Negative parallelism full ban (2026-04-27 — STRICT tier, always on for LinkedIn)

All 6 forms must be rewritten as paired declaratives. This is a hard ban, not a style preference.

```python
LINKEDIN_NEG_PARALLEL = [
    r"It's not just (\w+(?:\s+\w+){0,5}), it's (\w+(?:\s+\w+){0,5})",
    r"(\w[\w\s]{0,20}) isn't (\w[\w\s]{0,20}), it's (\w[\w\s]{0,20})",
    r"Not (\w[\w\s]{0,20}), but (\w[\w\s]{0,20})",
    r"It's not about (\w[\w\s]{0,20}), it's about (\w[\w\s]{0,20})",
    r"The question isn't (\w[\w\s]{0,20}), it's (\w[\w\s]{0,20})",
    r"This isn't (\w[\w\s]{0,20})\. This is (\w[\w\s]{0,20})",
    r"The real (\w+) isn't (\w[\w\s]{0,20}), it's (\w[\w\s]{0,20})",
]
# Rewrite as: "nobody's playing for unit economics. they're playing to own distribution."
# Never auto-substitute — meaning preservation requires judgment.
```

### LinkedIn engagement bait (delete/replace)
```python
LINKEDIN_ENGAGEMENT_BAIT = [
    r"What do you think\??",
    r"Thoughts\?",
    r"Agree or disagree\?",
    r"Let me know (in the comments|below|your thoughts)[!.]?",
    r"Tag someone who needs (this|to hear this)[!.]?",
    r"Drop a comment below[!.]?",
    r"Share your thoughts[!.]?",
    r"I'd love to hear (from you|your thoughts)[!.]?",
]
# Replacement: end on the strongest line. Or a specific question that expects a real answer.
```

### LinkedIn announcement openers (rewrite)
```python
LINKEDIN_ANNOUNCEMENTS = [
    r"I'm (so )?(excited|thrilled|delighted) to (announce|share|reveal)[^.]*\.",
    r"I'm (honored|humbled|proud) to (be|announce|share)[^.]*\.",
    r"Excited to share[^.]*\.",
    r"Big (news|announcement)[^.]*\.",
]
# Replace: lead with the concrete moment or result, not the feeling about it.
# Bad: "I'm excited to announce we raised $2M."
# Good: "We raised $2M. Here's what we're building:"
```

### LinkedIn CTA closers (rewrite)
```python
LINKEDIN_CTAS = [
    r"Save this (post )?for later[!.]?",
    r"Repost this if[^.]*\.",
    r"Like if you (agree|found this helpful)[!.]?",
]
# Keep: specific PS with a reason ("PS — full breakdown in the comments.")
# Remove: generic save/like/repost asks without a reason
```

### LinkedIn algorithm tells (flag)
- External links in post body → move to first comment
- 3+ hashtags in post body → trim to 0-2 at the end
- All-caps first line → rewrite

---

## Instagram

### Emoji spam (strict tier)
```python
EMOJI_SPAM = {
    "consecutive_limit": 2,             # Max 2 emoji in a row anywhere
    "per_caption_limit": 3,             # Max 3 total per caption
    "opening_line_ban": True,           # No emoji in first 2 lines
    "every_line_end": True,             # Flag if emoji at end of every line
    "filler_emoji": [                   # These in non-humor context = remove
        "🙏", "💯", "🔥", "✨", "💫", "🚀",
        "👇", "🌟", "💪", "🎯", "👊", "🤩", "❤️", "🙌"
    ]
}
```

### Instagram engagement bait (delete/replace)
```python
IG_ENGAGEMENT_BAIT = [
    r"Double tap if you agree[!.]?",
    r"(Like|Save) this post[!.]?",
    r"(Comment|Let me know) (below|in the comments)[^.]*\.",
    r"Tag (a friend|someone) who (needs this|would love this)[!.]?",
    r"Drop a ❤️ if[^.]*\.",
    r"Share this with[^.]*\.",
    r"Smash that like button[!.]?",
    r"What do you think\? 👇",
]
# Replace with a specific CTA that gives a reason:
# "Save this for the next time you [specific situation]."
# "Comment [word] and I'll send you [specific thing]."
```

### Instagram caption tells (rewrite opener)
```python
IG_OPENER_TELLS = [
    r"^Here (I am|we are) at [^.]*\.",     # Describes image — redundant
    r"^In today's post, I('m| am) sharing",
    r"^So excited to share",
    r"^I'm thrilled to (announce|share)",
    r"^Welcome back to my (page|feed|account)",
    r"^Today I want to talk about",
]
```

### Instagram weak authority vocab (replace)
```python
IG_VOCAB_REPLACE = {
    "curated": "selected / chosen / built",     # Overused
    "authentic": "[remove — show it, don't say it]",
    "aesthetic": "[replace with the specific look/feel it IS]",
    "vibe": "feel / energy / atmosphere",
    "intentional": "deliberate",
    "passionate": "[remove — show the work instead]",
    "journey": "process / path",
    "content creator": "[describe what they actually make]",
}
```

### Instagram link pattern (rewrite)
```python
IG_LINK_BAIT = [
    r"Link in bio!?$",              # No context — what's there?
    r"Check (the|my) link in (my )?bio[!.]?",
    r"More in (the )?bio[!.]?",
]
# Replace: "Full breakdown in bio — [what specifically is there and why it's worth clicking]."
```

### Instagram carousel tells (flag)
- All slides same word count → vary
- Bullet lists inside a single slide → one-idea paragraphs
- "Swipe for more →" on every slide → keep only on cover if used at all
- Slide with just a title and no body → add content or merge

---

## TikTok

### Presenter-voice openers (delete entirely — rewrite from sec 0)
```python
TIKTOK_PRESENTER_OPENERS = [
    r"Hey guys,?",
    r"Hey everyone,?",
    r"Welcome back (to my channel|to my page|everyone)[!.]?",
    r"So today I (want to|wanted to|am going to) (talk about|show you|cover)",
    r"In this video,? I (will|am going to|want to)",
    r"(So,? )?[Ww]ithout further ado",
    r"[Bb]efore we get started",
    r"[Ll]et's (get into it|dive in|get started)[!.]?",
    r"[Aa]lright,? (guys,? )?so",
]
# Replacement: start mid-action or mid-statement. The hook begins at word 1.
```

### TikTok filler phrases (delete)
```python
TIKTOK_FILLERS = [
    r"[Ss]o basically",
    r"[Yy]ou know what I mean\??",
    r"[Aa]nd,? um,? so",
    r"[Ss]o yeah,? that's (pretty much )?it",
    r"[Ii] hope that (makes sense|was helpful)",
    r"[Dd]oes that make sense\??",
    r"[Ii]f that makes sense",
    r"[Kk]ind of like",
    r"[Ss]ort of",
]
```

### YouTube-leak CTAs (delete/replace)
```python
YOUTUBE_CTAS = [
    r"[Dd]on't forget to (like and )?subscribe[!.]?",
    r"[Hh]it that (follow|subscribe|like) button[!.]?",
    r"[Dd]rop a like if (you found this helpful|this helped)[!.]?",
    r"[Ss]ubscribe for more content like this[!.]?",
    r"[Ss]mash that like button[!.]?",
    r"[Ii]f you (got|found) value from this (video|content)[^.]*\.",
    r"[Aa]nd if you (enjoyed|liked) today's video[^.]*\.",
]
# Replace:
# "Comment [word] if you want part 2."
# "Save this for when you need it."
# "Follow for [specific content type]."
# Or: end on the strongest line — no CTA.
```

### TikTok uniform rhythm (flag for rewrite)
```python
def detect_tiktok_uniform_rhythm(script: str) -> bool:
    sentences = split_sentences(script)
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 4:
        return False
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg)**2 for l in lengths) / len(lengths)
    return variance < 10 and avg > 10
# If flagged: break at least 1 in 3 sentences into a short punch under 6 words.
# Add at least 1 sentence fragment per 15 seconds of script.
```

### TikTok list-reading voice (flag for rewrite)
```python
LIST_READING = r"(Number|Step|Tip|Point) \d+:?\s+\w[^.]{10,25}\."
# Flag if 3+ consecutive items follow identical rhythm pattern.
# Rewrite: vary each item — one is a fact, one is a fragment, one is a question, one is an instruction.
```

### TikTok scripted transitions (replace with natural ones)
```python
SCRIPTED_TRANSITIONS = {
    "Now, moving on to": "",            # just start the next point
    "Our next point is": "",
    "As I mentioned (earlier|before)": "",   # TikTok is not linear; restate directly
    "Let's talk about": "",
    "Now I want to cover": "",
    "That brings us to": "",
    "Moving on to our next point": "",
}
```

---

## X (Twitter)

### X engagement bait (delete/replace)
```python
X_ENGAGEMENT_BAIT = [
    r"RT if you agree[!.]?",
    r"Retweet if you (agree|relate)[!.]?",
    r"Follow me for more (content|tweets) like this[!.]?",
    r"Like and retweet if[^.]*\.",
    r"Drop a ❤️ if[^.]*\.",
    r"What do you think\?$",
    r"Thoughts\?$",
    r"Agree\?$",
]
# Replace: end on the strongest line. Or a specific open question with a real answer expected.
```

### X hedge openers (rewrite — commit to the claim)
```python
X_HEDGE_OPENERS = [
    r"^I (think|feel|believe) (maybe|perhaps|possibly)",
    r"^Some might (argue|say|suggest)",
    r"^It could be argued that",
    r"^One might say that",
    r"^In my (humble|personal) opinion,?",
]
# X rewards conviction. Hedged takes die. Commit or don't post.
```

### X algorithm tells (flag)
- External link in tweet body → move to first reply
- 2+ hashtags in tweet body → remove or move to end (0-1 max)
- All-caps words → rewrite
- "follow me for more" → delete

---

## Cross-platform: never scrub

Applies to all platforms — these are signs of genuine human writing:

- **Specific, unusual, hard-to-fabricate details** (exact amounts, real company names, precise dates)
- **Mixed feelings without resolution** ("I think this is mostly right, but it still bothers me")
- **Intentional lowercase starts** (creator's voice)
- **`..` as soft pause** (deliberate, not a typo)
- **Sentence fragments used intentionally** ("Worth it.", "Every time.")
- **Genuine asides** ("(I keep second-guessing this, but here's what I landed on)")
- **Contractions** (don't, it's, you're, they're)
- **Specific numbers and named entities** (add more, never remove)
- **Era-specific slang** that maps to a real time and community
