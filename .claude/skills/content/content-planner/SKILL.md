---
name: social-content-planner
description: Build a unified 7-day content plan across LinkedIn, X, Instagram, and TikTok from a single weekly theme. Generates platform-native content per channel (not copy-paste), a repurposing map showing how one idea becomes 4 pieces, per-platform posting times, and a cross-platform readiness check. Use when the user wants to plan content across multiple platforms in one session.
---

# Social Content Planner

One theme. Multiple platforms. Platform-native content for each — not the same post copied everywhere.

The core value is the **repurposing engine**: take one strong idea and produce a LinkedIn long-form, an X thread, an IG carousel, and a TikTok script that each feel native to their platform while sharing the same core insight.

## When to use

- User wants to plan a week of content across multiple platforms at once
- User is tired of planning each platform separately
- User wants to repurpose content efficiently without copy-pasting
- Before a launch, growth sprint, or new topic push

## Input

- **Platforms active** (required): which of LinkedIn / X / Instagram / TikTok the user posts on
- **Weekly theme**: the central topic for the week (e.g., "data pipeline failure modes")
- **Audience**: who you're reaching (can differ per platform — ask if needed)
- **Goal for the week**: grow audience / build trust / drive inbound / launch something
- **Posting cadence per platform** (optional — defaults to platform-recommended cadence)

## Unified pillar framework

All platforms share the same 3 pillars. The expression differs per platform.

| Pillar | % | LinkedIn | X | Instagram | TikTok |
|---|---|---|---|---|---|
| **Insight / Authority** | 40% | Long-form text, carousel | Thread, number tweet | Carousel, edu Reel | Tutorial, listicle script |
| **Personal / Narrative** | 30% | Confession, year-pivot post | Confession tweet, story thread | Story Reel, single image | Story script, BTS |
| **Reach / Conversation** | 30% | Poll, community post | Reply, QT, question tweet | Short Reel, before/after | Duet, stitch, trending sound |

See `references/unified-pillars.md` for full detail and platform-specific adjustments.

## Repurposing map

One idea transforms across platforms — different entry point, same core insight.

| Source idea | LinkedIn | X | Instagram | TikTok |
|---|---|---|---|---|
| Data / insight breakdown | F7 Odd-Precision Money post | T2 Number Shock tweet | Carousel (data-driven) | Listicle script |
| Contrarian take | F10 Contrarian + receipts | T4 Hot Take thread | Reel: opinion format | Contrarian script (H4) |
| Personal mistake / lesson | F4 Time-Anchor Confession | T3 Confession tweet | Single image + caption | Story script (H1) |
| How-to / process | Authority text with steps | T10 How-I thread | Carousel: step-by-step | Tutorial script |
| Strong opinion | F5 Self-Proving Meta | T9 Thread Bait | Reel: opinion + evidence | Opinion script |

**Repurposing rule:** LinkedIn gets the full argument. X gets the sharpest line. Instagram gets the visual structure. TikTok gets the hook and spoken delivery. No platform gets a copy-paste.

Full transformation rules in `references/repurposing-map.md`.

## Steps

1. **Gather inputs.** Active platforms, weekly theme, audience, week's goal. Ask for cadence only if user wants to customize.
2. **Identify 3 core content pieces** (one per pillar). Each becomes the source for cross-platform repurposing.
3. **Build the repurposing map.** For each core piece, assign the platform-native format + hook/formula.
4. **Build the 7-day calendar.** Distribute across the week respecting per-platform cadence rules.
5. **Add daily engagement actions.** Per platform: LinkedIn comments, X replies, IG comment replies, TikTok replies + duet targets.
6. **Run the weekly readiness check.**
7. **Output as markdown.** Flag which piece to write first (usually the LinkedIn long-form — richest repurposing source).

## Output format

### Repurposing map

**Theme:** [Weekly theme]
**Goal:** [Grow / trust / inbound / launch]

| Piece | Pillar | LinkedIn | X | Instagram | TikTok |
|---|---|---|---|---|---|
| [Core insight] | Insight | F7 money post | T2 number tweet | Carousel | Tutorial script |
| [Personal story] | Personal | F4 confession | T3 confession tweet | Single image Reel | Story script |
| [Engagement play] | Reach | Poll | T7 question / QT | Short Reel | Stitch / trending sound |

---

### 7-day calendar

| Day | LinkedIn | X | Instagram | TikTok |
|---|---|---|---|---|
| Mon | Insight post (F7) — [angle] | Thread (T9) — [angle] | — | Tutorial — [angle] |
| Tue | (commenting day) | Confession tweet (T3) | Carousel — [angle] | — |
| Wed | — | QT + reply burst | Short Reel — [angle] | Stitch — [target] |
| Thu | Confession (F4) — [angle] | — | — | Story script — [angle] |
| Fri | — | Number tweet (T2) | Single image — [angle] | Listicle — [angle] |
| Sat | — | Question tweet (T7) | Short Reel — [angle] | — |
| Sun | — | (reply day only) | (Stories only) | Duet — [target] |

*(Only active platforms shown. Empty cells = engagement-only days for that platform.)*

---

### Daily engagement actions

| Platform | Daily action | Target count |
|---|---|---|
| LinkedIn | Comment on peer/aspirational posts | 10-20/day |
| X | Reply to peers, aspirationals, prospects | 10-15/day |
| Instagram | Reply to all comments within 2 hours of posting | All comments |
| TikTok | Reply to all comments within 2 hours of posting | All comments |

---

### Weekly readiness check

**Cross-platform:**
- [ ] Each active platform has at least 1 Insight piece
- [ ] Each active platform has at least 1 Personal piece
- [ ] No piece is copy-pasted identically across platforms
- [ ] No hook formula repeated within the same platform in the same week

**LinkedIn:**
- [ ] 3-5 posts total (not more)
- [ ] At least 1 vulnerability/confession post
- [ ] At least 1 data/receipt post
- [ ] No external links in post body

**X:**
- [ ] At least 1 thread this week
- [ ] Sunday = reply day only, no original posts
- [ ] All links go in first reply, not the tweet body
- [ ] Reply targets: peers + aspirationals + prospects

**Instagram:**
- [ ] At least 1 carousel (save magnet)
- [ ] At least 1 Reel (reach magnet)
- [ ] No two carousels on consecutive days
- [ ] Daily Stories (separate from feed posts)

**TikTok:**
- [ ] At least 1 video with trending sound
- [ ] At least 1 duet or stitch
- [ ] All hooks pass: muted test + screen-off test
- [ ] No videos deleted

## Platform cadence defaults

| Platform | Posts/day | Posts/week | Engagement/day |
|---|---|---|---|
| LinkedIn | 0-1 | 3-5 | 10-20 comments on others |
| X | 1-3 original | 7-14 + replies | 10-15 replies to others |
| Instagram | 0-1 feed | 4-5 feed + daily Stories | Reply all comments (2h) |
| TikTok | 1-2 | 7-12 | Reply all comments (2h) |

## Posting time defaults (2026)

| Platform | Best windows |
|---|---|
| LinkedIn | Tue-Thu 7:30-9:00 AM local |
| X | 8-10 AM, 12-1 PM, 7-9 PM local |
| Instagram | 8-10 AM or 11 AM-1 PM local |
| TikTok | 6-8 AM, 12-2 PM, 7-9 PM local |

## Platform non-negotiables (summary)

Full rules in `references/platform-rules.md`.

| Platform | Never | Always |
|---|---|---|
| LinkedIn | External links in post body | 0-2 hashtags, 900-1300 char sweet spot |
| X | Links in tweet body | 0-1 hashtags, reply in first hour |
| Instagram | Clickable links in caption | Reply within 2h, 0-5 hashtags |
| TikTok | "Hey guys" openers, deleting videos | Start mid-action, reply within 2h |

## Resources

- `references/unified-pillars.md` — cross-platform 3-pillar framework with platform-specific expression
- `references/repurposing-map.md` — how one idea transforms into 4 platform-native pieces
- `references/platform-rules.md` — algorithm rules per platform (cadence, format, timing, signals)

## Pipeline position

`/content plan` → [platform skills] → `/content humanize` → `/business approve` → publish

This skill outputs the weekly calendar and repurposing map. It does not write the individual pieces.
After this, send each planned piece to its platform skill, then run `/content humanize` on drafts, then `/business approve` to publish.

## Related skills — writing the individual pieces

| Platform | Write post | Write script/thread | Humanize |
|---|---|---|---|
| LinkedIn | `linkedin-post-writer` | — | `linkedin-humanizer` |
| X | `x-tweet-writer` | `x-thread-writer` | (built-in pass) |
| Instagram | `ig-caption-writer` | `ig-carousel-writer`, `ig-reel-script-writer` | `ig-humanizer` |
| TikTok | `tiktok-hook-writer` | `tiktok-script-writer` | `tiktok-humanizer` |
