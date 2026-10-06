---
name: instagram
description: >
  The Instagram creator skill. Covers content strategy, carousel copy, Reel
  scripting, visual asset generation, and media downloading. Routes to specialized
  sub-skills for each task. Triggers on: "instagram", "IG", "reel", "carousel",
  "instagram post", "instagram strategy", "write a carousel", "reel script",
  "download reel", "download instagram", "save instagram", "instagram content plan",
  "instagram hook", "ig growth", "instagram algorithm", "carousel slides".
tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - Edit
  - Grep
  - Glob
  - Agent
---

# Claude Instagram — Instagram Creator Skill

> Orchestrator for Instagram content creation, scripting, strategy, and media
> management. Routes to the right sub-skill based on your request. Sub-skills
> and reference files do the work — this file routes, delegates, and quality-checks.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/instagram strategy` | `ig-content-strategy/SKILL.md` | "Instagram strategy", "grow on IG", "IG algorithm", "why isn't my IG growing", "content plan", "format mix", "Instagram positioning" |
| `/instagram carousel` | `ig-carousel-writer/SKILL.md` | "write carousel slides", "carousel copy", "carousel about X", "Instagram carousel text", "swipeable post" |
| `/instagram reel` | `ig-reel-script-writer/SKILL.md` | "Reel script", "write a Reel about X", "IG video script", "hook for a Reel", "15-second script", "60-second Reel" |
| `/instagram visual` | `ig-carousel/SKILL.md` | "create carousel image", "visual carousel", "generate carousel PNG", "Instagram visual post", "design a post", "/carousel" |
| `/instagram download-reel` | `ig-reel-downloader/SKILL.md` | "download this reel", "save this IG reel", paste an `instagram.com/reel/` URL, "grab this Instagram video" |
| `/instagram download-image` | `ig-image-downloader/SKILL.md` | "download this Instagram image", "save this IG photo", paste an `instagram.com/p/` URL, "get images from this post" |

If a request spans multiple sub-skills (e.g., "write a carousel and generate the visual"),
run carousel-writer first for the copy, then pass the approved copy to ig-carousel for rendering.

## Context-Gathering Protocol

Before invoking content sub-skills (`strategy`, `carousel`, `reel`, `visual`), collect:

1. **Account niche/topic** — What is the account about? Be specific (not "fitness" — "strength training for women over 40").
2. **Profile size tier:**
   - New: < 1K followers
   - Growing: 1K–10K followers
   - Established: 10K–100K followers
   - Authority: 100K+ followers
3. **Primary goal:** Reach / Saves / Community / Sales / Brand Awareness

For `download-reel` and `download-image` sub-skills, only the Instagram URL is needed.

## Instagram's Four Surfaces

Each surface serves a different algorithmic purpose. Content strategy must span all four.

| Surface | Primary Signal | Primary Goal |
|---------|---------------|-------------|
| **Reels** | Shares to Stories, Completion rate | Reach new audiences |
| **Carousels** | Saves, Swipe-through rate | Authority, save magnets |
| **Feed (single image)** | Likes, Comments | Brand presence, trust |
| **Stories** | Replies, Sticker interactions | Community, retention |

## Sub-Skill Capabilities

### Content Sub-Skills
- **`ig-content-strategy`** — Full platform strategy: format mix, posting cadence, hashtag rules, algorithm optimization, content pillars, creator collaboration
- **`ig-carousel-writer`** — Slide-by-slide carousel copy: cover slide hook, body slides (one idea/slide), CTA slide, optional caption. Formats: Listicle, Step-by-step, Before/After, Breakdown, Myth-busting
- **`ig-reel-script-writer`** — Reel scripts with timing, on-screen text cues, spoken lines: 7–90 second range, dual-channel hook (visual + audio)
- **`ig-carousel`** — Visual HTML + PNG carousel generation via Playwright: styled 1080×1350 assets, brand identity integration, caption generation

### Utility Sub-Skills
- **`ig-reel-downloader`** — Download Reels as .mp4 via fastdl.app + curl. Requires Chrome MCP and `media.fastdl.app` in network allowlist
- **`ig-image-downloader`** — Download single images and carousel images as .jpg + combined PDF. Requires Chrome MCP and `*.cdninstagram.com` in network allowlist

## Reference Files

Load on-demand when a sub-skill requires them.

| File | Content |
|------|---------|
| `ig-carousel-writer/references/slide-formats.md` | Full skeletons for all 5 carousel formats |
| `ig-reel-script-writer/references/script-formats.md` | Full scripts for tutorial, story, listicle, opinion, contrarian formats |

## Hook Rule (First 3 Seconds for Reels / Cover Slide for Carousels)

The dual-channel rule: hook must work with sound OFF (on-screen text) AND eyes off screen (spoken line). Both channels must be independently compelling.

**Never start with:** "Hey guys", "So today", "Welcome back", intro animations, title cards, logos.

## Quality Gates

Every sub-skill output MUST pass before delivery:

1. **Specificity** — Every recommendation must be actionable for THIS account's niche and tier.
2. **Platform accuracy** — No advice contradicting 2026 Instagram algorithm rules. Never hallucinate benchmarks.
3. **Format integrity** — Carousel slides: one idea per slide, 20–60 words per body slide. Reel scripts: proper timing columns, dual-channel hooks.

## Self-Anneal Loop

If a sub-skill output fails a quality gate:
1. Identify which gate failed and why
2. Re-read the relevant reference file
3. Re-generate only the failing sections
4. If still failing after 2 attempts, deliver with explicit caveats

## Output Format

Default to markdown. Carousel output: numbered slides with headline + body + char count. Reel scripts: timing column + on-screen text column + spoken column. Strategy: structured report with surface-by-surface analysis. Always end with "Next Steps" pointing to the logical next sub-skill.

## Pipeline position

**Receives from:** `/content plan` — the weekly calendar defines which carousels and Reels to produce
**Then:** `/content humanize` — run on caption drafts before approving
**Outputs to:** `/business approve` — finished PNGs + caption.md → approve-post for publishing
**Or:** `/content buffer` — schedule the post instead of publishing immediately
