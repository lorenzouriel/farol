---
name: x-tweet-writer
description: Write a single tweet or thread-opener using proven X hook formulas (contrarian, number-shock, confession, hot-take, pattern-interrupt, comparison, question, reveal, thread-bait, how-I). Runs a humanizer pass before output. Use when the user asks to write a tweet, needs a hook, or wants a short-form post. For full threads use x-thread-writer.
---

# X Tweet Writer

Ship high-performing tweets using hook formulas validated on X in 2025-2026.

## When to use

- User says "write me a tweet about X"
- User has a topic and needs a punchy single tweet
- User wants to write a thread opener (the hook tweet before the full thread)
- User needs to pick a format and fill in their voice

## Formulas

| Code | Formula | Best for |
|---|---|---|
| T1 | Contrarian Opener | Hot takes, counter-intuitions |
| T2 | Number Shock | Data posts, breakdowns, costs |
| T3 | Confession/Mistake | Vulnerability, credibility resets |
| T4 | Hot Take + Thread | Opinion-first threads |
| T5 | Pattern Interrupt | "Stop doing X, do Y instead" |
| T6 | Comparison | Head-to-head, tool comparisons |
| T7 | Question | Engagement hooks, polls setup |
| T8 | The Reveal | "The real reason X happens is Y" |
| T9 | Thread Bait | "I spent N [time] studying X. Here's what I found 🧵" |
| T10 | How-I | "How I [result] in [timeframe]:" |

Full skeletons in `references/hook-formulas.md`.

## Steps

1. **Gather inputs.** Topic, angle, audience (tech founders / operators / developers), tweet type (single tweet / thread opener), desired tone (analytical / personal / provocative).
2. **Pick the formula.** If user didn't specify, suggest 2-3 that fit the topic. Show the formula code.
3. **Draft the tweet.** Apply formula skeleton with user voice. Respect the 2026 X algorithm rules:
   - First 5-8 words are everything (visible in feed before truncation)
   - Hard limit: 280 chars for single tweet
   - No external links in tweet body — move to reply below the tweet
   - 0-1 hashtags max; place at end if used at all
   - No "follow me for more" closers
   - Double-check: is the first line interesting enough to stop the scroll?
4. **Humanizer pass.** Strip em dashes, AI vocab, bullet-point lists in single tweets. Vary sentence length. Add one concrete specific (number, name, date) per tweet.
5. **Approval card.** Show: formula used, full tweet, char count, suggested posting window.
6. **On approval.** Optionally publish via configured integration.

## Algorithm rules (2026)

See `references/algorithm-heuristics.md` for full detail. Summary:

- **No links in the tweet** — algo deprioritizes by ~50%. Always put links in the first reply.
- **Replies > RTs > likes** for reach. Write tweets that provoke a response.
- **Post timing:** 8-10 AM, 12-1 PM, 7-9 PM local (pick one per day).
- **0-1 hashtags.** More = spam signal. None is usually better.
- **First-hour engagement** is the boost window. Be ready to reply to early comments.
- **Images boost impressions 40%** but don't always boost replies. Video > image > text.

## Hard rules

- Never write tweets that beg: "follow me", "RT if you agree", "what do you think?"
- No emoji spam. Max 1 emoji per tweet, at the end. Never lead with emoji.
- No all-caps words.
- No parenthetical asides (the algo sees them as filler).
- No hedging: "might", "could", "perhaps", "sort of". Commit to the claim.

## Anti-patterns (skill will refuse)

- "In today's fast-paced world..."
- "Game-changer", "deep dive", "leverage", "fundamentally"
- Em dashes (—) anywhere
- Sentences all the same length
- Closing with a question when the tweet was already weak

## Resources

- `references/hook-formulas.md` — 10 formula skeletons with worked examples
- `references/algorithm-heuristics.md` — 2026 X posting rules

## Related skills

- `x-thread-writer` — write the full thread after the opener
- `x-hook-extractor` — reverse-engineer a hook from a viral tweet
- `x-reply-drafter` — draft replies to replies on your tweet
