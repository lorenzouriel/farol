# Universal Scrub Rules

Applied to ALL platforms before platform-specific rules run. Source: Wikipedia "Signs of AI writing" taxonomy + forensic model-leakage patterns.

---

## TIER: FORENSIC (always on — no platform exception)

No human writer ever produces these. Delete immediately.

### AI tool markers
```python
FORENSIC_MARKERS = [
    r"\boaicite\b",
    r"\bcontentReference\b",
    r"\bturn\d+search\d+\b",       # turn0search0, turn1search3, etc.
    r"\battached_file\b",
    r"\bgrok_card\b",
    r"\boai_citation\b",
    r"\bcontentReference\[\^\d+\]",
]
```

### Knowledge-cutoff disclaimers (delete sentence)
```python
CUTOFF_DISCLAIMERS = [
    r"As of my (last update|knowledge cutoff|training cutoff)[^.]*\.",
    r"As of (January|June|October|November) 202\d[^.]*\.",
    r"Based on (information|data) (available|up to) [^.]*\.",
    r"My (knowledge|training data) (cuts off|extends to) [^.]*\.",
    r"I cannot provide (real-time|current|up-to-date) [^.]*\.",
    r"While specific details (are|remain) (limited|scarce)[^.]*\.",
    r"maintains a low profile[^.]*\.",
    r"keeps personal details private[^.]*\.",
    r"it is believed that[^.]*\.",
    r"likely (grew up|studied|began)[^.]*\.",
]
```

### Phrasal templates (flag for user fill — do NOT auto-fill)
```python
PHRASAL_TEMPLATES = [
    r"\[Your Name\]", r"\[Your Company\]", r"\[Your Brand\]",
    r"\[Describe [^]]+\]", r"\[Insert [^]]+\]",
    r"202\d-XX-XX",
    r"\[NAME\]|\[DATE\]|\[TOPIC\]|\[PLATFORM\]",
]
```

### Collaborative artifacts (delete entirely)
```python
COLLABORATIVE_ARTIFACTS = [
    r"I hope this helps[!.]?",
    r"Let me know if you'd like me to (expand|elaborate|add)[^.]*\.",
    r"Would you like me to[^?]*\?",
    r"Here is (an overview|a summary|an essay)[^.]*\.",
    r"(Of course|Certainly|Absolutely)!",
    r"Great question!",
    r"You're absolutely right[^.]*\.",
    r"That's an excellent point[^.]*\.",
]
```

### Em dash overuse (3+ in < 300 words = forensic)
```python
def detect_em_dash_overuse(text: str) -> bool:
    word_count = len(text.split())
    em_count = text.count("—") + text.count(" — ") + text.count("--")
    return word_count < 300 and em_count >= 3
# Single em dash = aesthetic tier only
# Spaced em dash ( — ) and double hyphen (--) = always flag
```

### Outline-formula closers (delete/rewrite)
```python
OUTLINE_CLOSERS = [
    r"In conclusion,[^.]+\.",
    r"To (summarize|sum up),[^.]+\.",
    r"In summary,[^.]+\.",
    r"Despite (its|the|these) [^,]+, (faces|will continue)[^.]*\.",
    r"Looking ahead, [^.]+ (will|must|should)[^.]*\.",
    r"The future (looks|remains) (bright|promising)[^.]*\.",
    r"Exciting times (lie|are) ahead[^.]*\.",
]
```

---

## TIER: STRICT (default on)

### AI vocabulary — replace
```python
STRICT_VOCAB_REPLACE = {
    # Verbs
    "leverage": "use",          "leveraging": "using",       "leveraged": "used",
    "utilize": "use",           "utilizing": "using",        "utilized": "used",
    "facilitate": "help",       "facilitating": "helping",
    "streamline": "simplify",   "streamlining": "simplifying",
    "delve": "look",            "delving": "looking",
    "navigate": "handle",       "navigating": "handling",
    "unlock": "find",           "unlocking": "finding",      "unlocked": "found",
    "harness": "use",           "harnessing": "using",       "harnessed": "used",
    "foster": "build",          "fostering": "building",     "fostered": "built",
    "cultivate": "grow",        "cultivating": "growing",
    "garner": "get",            "garnering": "getting",
    "showcase": "show",         "showcasing": "showing",
    "underscore": "show",       "underscoring": "showing",
    "highlight": "show",        # only when used as filler verb
    "bolster": "strengthen",    "bolstered": "strengthened",
    # Nouns
    "landscape": "field",       "ecosystem": "space",
    "paradigm": "approach",     "realm": "area",
    "tapestry": "mix",          "interplay": "relationship",
    # Adjectives
    "seamless": "smooth",       "holistic": "full",
    "nuanced": "specific",      "pivotal": "key",
    "groundbreaking": "new",    "meticulous": "careful",
    "robust": "solid",          "vibrant": "active",
    "intricate": "detailed",    "valuable": "useful",
}

STRICT_VOCAB_DELETE = {
    # Filler adverbs — delete word + surrounding comma if present
    "fundamentally", "essentially", "ultimately", "crucially", "notably",
    "arguably", "certainly", "definitely", "undoubtedly", "importantly",
}
```

### Significance inflation (rewrite sentence)
```python
SIGNIFICANCE_PHRASES = [
    r"\bstands as (a|an)\b",
    r"\bserves as (a|an)\b",
    r"\bmarks a (pivotal|significant|key|crucial)\b",
    r"\brepresents? (a|an) (significant|major|key|pivotal)\b",
    r"\bis a testament to\b",
    r"\bunderscores? (its|their|the) (importance|significance)\b",
    r"\breflects? broader\b",
    r"\bsetting the stage for\b",
    r"\bindelible mark\b",
    r"\bdeeply rooted\b",
    r"\bshaping the (future|landscape|narrative)\b",
]
```

### Promotional language (rewrite)
```python
PROMOTIONAL_PHRASES = [
    r"\bnestled (in|within|at)\b",
    r"\bin the heart of\b",
    r"\bbreathtaking\b",
    r"\bstunning\b",
    r"\brenowned\b",
    r"\bboasts (a|an)\b",
    r"\benhancing its\b",
    r"\bmust-visit\b",
    r"\brich (cultural|historical)\b",
    r"\bvibrant (community|culture|city)\b",
    r"\bprofound (impact|effect|influence)\b",
]
```

### Vague attributions (rewrite or delete)
```python
VAGUE_ATTRIBUTIONS = [
    r"\bindustry (reports?|observers?|experts?)\b",
    r"\bobservers? have (noted|cited|argued)\b",
    r"\bexperts? (argue|believe|suggest|say)\b",
    r"\bsome critics? (argue|say|suggest)\b",
    r"\bseveral sources?\b",
    r"\bwidely (regarded|considered|seen)\b",
]
```

### Negative parallelisms (flag for user rewrite)
```python
NEG_PARALLEL_PATTERNS = [
    r"It's not just (\w+(?:\s+\w+){0,5}), it's (\w+(?:\s+\w+){0,5})",
    r"(\w+(?:\s+\w+){0,3}) isn't (\w+(?:\s+\w+){0,5}), it's (\w+(?:\s+\w+){0,5})",
    r"Not (\w+(?:\s+\w+){0,5}), but (\w+(?:\s+\w+){0,5})",
    r"It's not about (\w+(?:\s+\w+){0,5}), it's about (\w+(?:\s+\w+){0,5})",
    r"The question isn't (\w+(?:\s+\w+){0,5}), it's (\w+(?:\s+\w+){0,5})",
    r"This isn't (\w+(?:\s+\w+){0,5})\. This is (\w+(?:\s+\w+){0,5})",
]
# Rewrite as paired declaratives — never auto-substitute (meaning preservation needs human judgment)
```

### Filler phrases (delete + restructure)
```python
FILLER_PHRASES = [
    (r"In order to (\w)", r"To \1"),
    (r"Due to the fact that", "Because"),
    (r"At this point in time", "Now"),
    (r"In the event that", "If"),
    (r"has the ability to", "can"),
    (r"It is important to note that", ""),
    (r"It is worth noting that", ""),
    (r"It is (worth|important) (mentioning|highlighting) that", ""),
    (r"At the end of the day", ""),
    (r"When all is said and done", ""),
    (r"In today's (fast-paced|digital|modern) world,?", ""),
    (r"In the age of (AI|technology|digital transformation),?", ""),
]
```

### Signposting and announcements (delete)
```python
SIGNPOSTING = [
    r"Let's (dive in|dive into|explore|break this down)[.!]?",
    r"Here's what you need to know[.:]?",
    r"(Now )?[Ll]et's (look at|talk about|discuss)[^.]*\.",
    r"Without further ado[,.]?",
    r"Before we (get started|begin|dive in)[,.]?",
    r"So, without further ado[,.]?",
]
```

### Superficial -ing analyses (restructure sentence)
```python
ING_ANALYSIS_PATTERN = r"\w+ing (how|that|its|their|the) \w+ (contributes?|reflects?|symbolizes?|underscores?|showcases?|highlights?)[^.]*\."
# Flag any sentence-ending participial phrase that adds fake depth
```

### Persuasive authority tropes (cut or rewrite plainly)
```python
AUTHORITY_TROPES = [
    r"\bThe real question is\b",
    r"\bAt its core,?\b",
    r"\bIn reality,?\b",
    r"\bWhat really matters (is|here)\b",
    r"\bThe deeper issue\b",
    r"\bThe heart of the matter\b",
    r"\bFundamentally,?\b",
]
```

### Copula avoidance (restore simple is/are/has)
```python
COPULA_AVOIDANCE = [
    (r"(\w[\w\s]+) serves as (a|an) (\w[\w\s]+)", r"\1 is \3"),
    (r"(\w[\w\s]+) stands as (a|an) (\w[\w\s]+)", r"\1 is \3"),
    (r"(\w[\w\s]+) boasts (a|an) (\w[\w\s]+)", r"\1 has \3"),
    (r"(\w[\w\s]+) features (a|an) (\w[\w\s]+)", r"\1 has \3"),
]
```

### Sycophantic opener removal (delete entirely)
```python
SYCOPHANTIC_OPENERS = [
    r"^Great question!",
    r"^Excellent question!",
    r"^Of course!",
    r"^Certainly!",
    r"^Absolutely!",
    r"^You're absolutely right",
    r"^That's an excellent point",
]
```

### Punctuation normalization
```python
PUNCT_NORMALIZE = [
    ("“", '"'),   # curly left quote → straight
    ("”", '"'),   # curly right quote → straight
    ("‘", "'"),   # curly left apostrophe → straight
    ("’", "'"),   # curly right apostrophe → straight
    (" — ", ". "),  # spaced em dash → period
    ("—", ". "),    # em dash → period (strict tier)
    ("–", "-"),     # en dash → hyphen
    ("--", ". "),        # double hyphen → period
]
```

### Bold overuse (reduce)
```python
def detect_bold_overuse(text: str) -> bool:
    bold_count = len(re.findall(r"\*\*[^*]+\*\*", text))
    word_count = len(text.split())
    return bold_count > (word_count / 20)  # more than 1 bold per 20 words = overuse
# Keep: genuinely important single terms. Remove: decorative bolding of ordinary phrases.
```

### False ranges (rewrite)
```python
# Pattern: "from X to Y" where X and Y aren't on a meaningful scale
FALSE_RANGE_PATTERN = r"from ([\w\s]+) to ([\w\s]+), from ([\w\s]+) to ([\w\s]+)"
# Rewrite as a simple list of the actual items
```

---

## TIER: AESTHETIC (opt-in only)

Patterns AI uses but legitimate human writers also use. Apply only when audience demands it.

```python
AESTHETIC_VOCAB = {
    "robust": "solid",
    "vibrant": "alive",
    "intricate": "detailed",
    "meticulous": "careful",
    "garner": "get",
    "showcase": "show",
    "underscore": "highlight",
    "bolster": "strengthen",
}
# Dickinson/McCarthy defense: single em dash = aesthetic tier only
# Lincoln/Churchill defense: rule of three = aesthetic tier only
# Watson/Crick defense: passive voice = aesthetic tier only in scientific/academic text
```

---

## Pass 2 — Burstiness (all tiers)

```python
def enforce_burstiness(text: str) -> str:
    sentences = split_sentences(text)
    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg)**2 for l in lengths) / len(lengths)

    if variance < 25 and avg > 12:
        # Force-break every 3rd sentence into < 8 words
        for i in range(2, len(sentences), 3):
            sentences[i] = shorten(sentences[i])

    return " ".join(sentences)
```

Minimum human fingerprints per 100 words:
- 1 specific number (not "many", "a lot")
- 1 named entity (real person, company, tool, date, place)
- 1 first-person concrete detail
- 1 opinion or mild vulnerability

---

## Preserve (never scrub — signs of human writing)

- **Specific, unusual, hard-to-fabricate detail** — a real address, a weird quote, an exact dollar amount
- **Mixed feelings and unresolved tension** — "I think this is mostly good, but it bothers me"
- **Variety in sentence length** — real alternation of short punches and longer sentences
- **Genuine asides and self-corrections** — "(I keep wanting to say 'almost' here, but it really was certain)"
- **Intentional lowercase starts** — creator's voice signature
- **`..` as soft pause** — not an AI tell; a deliberate stylistic choice
- **Sentence fragments used intentionally** — "Worth it.", "Every time.", "Done."
- **Contractions** — don't, it's, you're, they're
- **First-person sensory details** — what you actually saw, heard, felt
