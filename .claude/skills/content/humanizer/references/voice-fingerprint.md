# Voice Fingerprint

How to preserve the user's voice while scrubbing AI tells. The goal is not a generic clean text — it's this person's clean text.

---

## What to extract from a voice sample

Before rewriting, if the user provides a sample of their own writing, extract:

| Dimension | What to look for | How to apply |
|---|---|---|
| **Sentence length pattern** | Short and punchy? Long and flowing? Mixed? | Match the ratio in the rewrite |
| **Word choice level** | Casual ("stuff", "things")? Technical? Academic? | Don't upgrade or downgrade without reason |
| **Paragraph starts** | Jump right in? Set context first? | Match the pattern |
| **Punctuation habits** | Lots of dashes? Parentheticals? Semicolons? `..` pauses? | Preserve these — they're voice |
| **Recurring phrases** | Any verbal tics or signature expressions? | Keep 1-2 per piece; don't over-repeat |
| **Transitions** | Explicit connectors? Or just start the next point? | Match their style |
| **Hedging level** | Do they commit to claims, or qualify? | Match their actual confidence level |
| **First-person density** | Heavy "I"? Or rarely personal? | Keep the ratio |

---

## Platform-specific voice preservation

### LinkedIn
- **Lowercase starts** (many LinkedIn creators do this deliberately) — preserve
- **`..` soft pause** — preserve, do not convert to em dash or period
- **Specific capitalization style** — if they capitalize mid-sentence for emphasis, keep it
- **Personal idioms** — phrases that appear in multiple posts are intentional

### X
- **Ultra-short sentences as punches** — if their natural voice is 4-word lines, keep it
- **Single-word reactions** ("Exactly.", "No.", "Right.") — preserve, these are voice not grammar errors
- **No-cap tweets** — some creators write entirely lowercase; preserve if consistent
- **Abbreviations** — if they use "bc", "tbh", "ngl" naturally, keep them

### Instagram
- **Emoji density** — if the user naturally uses 1-2 emoji and they're on-brand, keep them; only remove if beyond threshold
- **Line break rhythm** — some creators use single-sentence paragraphs; match the pattern
- **Colloquial signoffs** — if they always end with a dash and a PS, preserve the format

### TikTok
- **Natural speech quirks** — "right?" as rhetorical, "here's the thing:", sentence fragments
- **Pacing rhythm** — if they naturally speak in short punches, don't force longer sentences
- **Direct address** — "you" used frequently is natural for TikTok; keep it
- **Reaction language** — "honestly", "no joke", "I'm not kidding" — these are human tells, not AI

---

## What to never flatten

Even during aggressive scrubbing, never remove:

- **Intentional repetition** — if they repeat a phrase for emphasis, it's not AI; it's rhetoric
- **Self-corrections mid-text** — "(actually, I realized later this was wrong)" — human signal, keep it
- **Acknowledged uncertainty** — "I could be wrong, but..." — vulnerability is a feature, not a bug
- **Specific numbers and named entities** — these are the most important human fingerprints; never remove, always add more
- **Unusual specificity** — if they mention a weird detail only they would know, that's the most important line in the piece
- **Era-specific references** — slang, events, or in-jokes that date the text are human signals

---

## When no sample is provided

Fall back to:
- **Natural, varied cadence** — mix short and long sentences
- **Opinionated** — don't be neutral when the topic isn't neutral
- **Specific** — replace every vague quantity with a specific one (ask user if needed)
- **Active voice** — subject → verb → object, nearly always
- **First person where appropriate** — don't hide behind "one" or "we" if it's clearly personal content

---

## The test: read aloud

After rewriting, read the full text aloud.

- If it sounds like a person talking to someone they know → done
- If it sounds like a press release → something is still wrong
- If it sounds like someone reading a script → for TikTok/Reel, rewrite spoken sections
- If any sentence makes you stumble → rewrite that sentence; if you stumble, the reader will too

The read-aloud test catches what pattern-matching misses: rhythm, naturalness, and whether the voice feels like a real person or a well-trained chatbot pretending to be one.
