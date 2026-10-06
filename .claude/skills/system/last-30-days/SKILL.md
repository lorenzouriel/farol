---
name: last-30-days
description: "Deep research skill that investigates any topic across Reddit, Hacker News, the web, and X/Twitter (via Grok) over the past 30 days. Returns a synthesized research briefing with real citations and engagement data, saved as a markdown file and displayed in chat. Trigger this skill whenever the user says 'research [topic]', 'last-30-days on [topic]', 'what's happening with [topic]', 'what are people saying about [topic]', 'find me info on [topic]', 'run last-30-days on [topic]', or any variation where the goal is a multi-source research brief on a specific topic. Also use for competitor research, trend discovery, tool comparisons, and audience sentiment analysis."
---

# Last 30 Days Research

Multi-source research agent that synthesizes what people are actually saying about a topic across Reddit, Hacker News, the web, and X/Twitter — all within the past 30 days.

## Invoking the skill

The user will provide a topic. It might come as:
- "last-30-days on [topic]"
- "research [topic] for me"
- "what's the word on [topic] lately"
- Or they'll just name a topic after invoking the skill

If no topic is specified, ask for one before proceeding.

## Workflow

Run Phases 1–3 in parallel (they're independent). Then run Phase 4 (Grok). Then synthesize.

---

### Phase 1: Reddit

Use WebFetch to hit Reddit's public search JSON API — no API key needed:

```
https://www.reddit.com/search.json?q=TOPIC&sort=top&t=month&limit=25
```

Also run a `new` sort to catch recent posts that haven't had time to rank:
```
https://www.reddit.com/search.json?q=TOPIC&sort=new&t=month&limit=15
```

From each result, extract:
- Post title
- Subreddit
- Score (upvotes)
- Number of comments
- Date posted
- URL

Then for the top 3–5 posts by score, fetch the comment thread:
```
https://www.reddit.com/r/SUBREDDIT/comments/POST_ID.json?sort=top&limit=10
```

Look for recurring themes, complaints, praise, and questions in the comments. These are gold.

---

### Phase 2: Hacker News

Use WebFetch to hit the Algolia HN search API:

```
https://hn.algolia.com/api/v1/search?query=TOPIC&tags=story&numericFilters=created_at_i>TIMESTAMP&hitsPerPage=20
```

Calculate TIMESTAMP as Unix epoch for 30 days ago. Today's date is in your context — subtract 30 days and convert: `int(datetime.timestamp())`.

Also search HN comments for deeper discussion:
```
https://hn.algolia.com/api/v1/search?query=TOPIC&tags=comment&numericFilters=created_at_i>TIMESTAMP&hitsPerPage=15
```

Extract:
- Story title and URL
- Points and comment count
- Author and date
- Notable comment excerpts

---

### Phase 3: Web Search

Use WebSearch with 2–3 targeted queries to catch recent news, reviews, and analysis:

- `"[TOPIC]" news site:techcrunch.com OR site:theverge.com OR site:wired.com`
- `[TOPIC] review` followed by the current year
- `[TOPIC] problems OR complaints OR "worth it"` — for honest opinions

For the 3–4 most relevant results, use WebFetch to pull actual page content — not just headlines. Grab the key points, quotes, and conclusions.

---

### Phase 4: X/Twitter via Grok

Since X requires authentication, use Claude in Chrome for this phase.

1. Navigate to `https://grok.com/`
2. Wait for the page to fully load
3. Find the message input field
4. Type and submit this prompt (swap in the actual topic):

> "What are people saying about [TOPIC] on X/Twitter in the last 30 days? Summarize the main discussions, opinions, complaints, praise, and any notable posts or accounts. Give me specific examples where you can."

5. Wait for Grok's full response
6. Extract the complete response text

This gives real X/Twitter signal without an API key.

If the page shows a login wall or Grok is unavailable, note that in the output and skip this section — don't get stuck.

---

### Phase 5: Synthesize

Combine all four sources into a coherent briefing. The goal is synthesis, not a dump of raw data. Look for:

- **Consensus** — What do people broadly agree on across platforms?
- **Controversy** — Where is there real disagreement or debate?
- **Pain points** — What frustrations keep surfacing?
- **Excitement** — What are people genuinely enthusiastic about?
- **Emerging patterns** — What's new or gaining momentum vs. settled wisdom?
- **Gaps** — What questions aren't being answered well anywhere?

Cross-platform convergence is your strongest signal. If something shows up on Reddit AND HN AND X, that's real.

---

## Output Format

Use this exact structure for the markdown file:

```markdown
# [TOPIC] — Last 30 Days Research
*Generated: [DATE]*

## TL;DR
2–3 sentences. What's the most important thing someone should know right now?

## Reddit
### Top Posts
- **[Post Title]** (r/subreddit) — [X upvotes, Y comments] — [one-line summary] — [URL]

### What Reddit Is Saying
Narrative paragraph. What's the overall tone? What themes keep coming up? Any notable comment threads?

## Hacker News
### Notable Stories
- **[Story Title]** — [X points, Y comments] — [one-line summary] — [URL]

### What HN Is Saying
Narrative paragraph. HN skews technical/builder — note that lens in your synthesis.

## Web
### Key Sources
- **[Article Title]** ([Publication]) — [key takeaway] — [URL]

### What the Web Is Saying
Paragraph synthesizing the broader coverage. Who's covering it, what angle, what conclusions.

## X/Twitter (via Grok)
Grok's response, lightly cleaned up. Keep specific handles or post references where Grok provided them.

## Cross-Platform Patterns
What showed up consistently across multiple sources? This is the highest-confidence signal.

## Key Takeaways
- [Most important thing]
- [Second most important thing]
- [Third most important thing]

## Content Angles (if relevant)
If this research is for content creation, list 2–3 specific video/post angles the data actually supports.
```

---

## Saving and delivering the output

1. Save the markdown file to a `last-30-days/` subfolder inside the user's research folder. Create the subfolder if it doesn't exist. Name the file `[TOPIC]-[YYYY-MM-DD].md`.

2. Provide a link to the file.

3. **Also paste the full research briefing directly in chat.** Don't make the user open a file to see the results — show them everything right there.

---

## Troubleshooting

- **Reddit blocks the fetch**: Try appending `?raw_json=1` or fetching a specific subreddit directly (`reddit.com/r/SUBREDDIT/search.json?q=TOPIC&restrict_sr=1`)
- **HN returns no results**: Broaden the query — try shorter keywords, or drop the timestamp filter to see if the topic is just older
- **Grok shows a login wall**: Skip the X section and note it. Don't retry endlessly.
- **WebFetch times out on a long article**: Take what loaded, note it was truncated
