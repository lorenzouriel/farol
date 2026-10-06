---
name: ig-carousel-writer
description: Write a complete Instagram carousel post — cover slide hook, body slides (one idea per slide), and CTA slide. Carousels are Instagram's highest-save format. Outputs slide-by-slide text with on-screen copy and optional caption. Use for educational content, listicles, step-by-step guides, and before/after reveals.
---

# IG Carousel Writer

Write Instagram carousels that get saved and shared. Carousels are the highest-save format on Instagram — the algorithm pushes them because saves signal "worth returning to."

## When to use

- User says "write me a carousel about X"
- User has a list, a process, a breakdown, or a lesson to teach in slides
- User wants a swipeable post with text-heavy slides

## Carousel formats

| Format | Slides | Best for |
|---|---|---|
| **Listicle** | 6-10 | "N tips/tools/lessons about X" |
| **Step-by-step** | 5-8 | Tutorials, processes, how-tos |
| **Before/After** | 4-6 | Transformation, comparison, results |
| **Breakdown** | 6-10 | Explaining a concept layer by layer |
| **Myth-busting** | 5-8 | Contrarian content, correcting misconceptions |

Full structures in `references/slide-formats.md`.

## Steps

1. **Gather inputs.** Topic, format preference (or skill picks), audience, number of slides (optional — defaults to shortest that covers the topic), and whether a caption is needed alongside the slides.
2. **Pick format.** Map topic → format. Listicle if enumerable. Step-by-step if procedural. Breakdown if conceptual.
3. **Draft slide 1 (cover).** The cover slide is the hook — it decides the swipe rate. Must:
   - State the promise in 5-8 words ("7 things every data engineer should know")
   - Make the reader want to swipe before seeing the rest
   - Not give away the punchline
4. **Draft body slides.** One idea per slide. Each slide:
   - Headline (3-7 words) + body text (20-60 words)
   - Self-contained: someone screenshot-ing this slide gets value even without context
   - Micro-hook at the end if it leads to the next slide ("but here's the catch →")
5. **Draft last slide (CTA).** One action. Options: save, comment a specific word, follow for more, DM for a resource. No generic "let me know what you think."
6. **Draft caption.** Optional. Short (under 150 chars) teaser that matches the cover slide hook. Or use ig-caption-writer for a full caption.
7. **Humanizer pass.** Strip AI tells. Vary slide text length. Each slide must sound like a person, not a bullet deck.
8. **Approval output.** Show all slides numbered, with headline + body per slide and character counts.

## Slide text rules

- **Headline:** 3-7 words. Short enough to read at a glance.
- **Body text:** 20-60 words per slide. Enough to be useful; not so much it becomes a wall.
- **Font contrast:** All-caps headlines work visually but use sparingly (2-3 slides max in a carousel). Don't SHOUT.
- **Slide consistency:** Each slide should feel like part of the same visual system. Don't change tone mid-carousel.
- **No bullet lists inside a single slide.** One idea, one sentence or short paragraph. Bullets inside slides look broken on mobile.
- **The "2-3 slides in" rule:** By slide 3, the reader must have already gotten some value. If slide 3 is still setup, you've lost them.

## Anti-patterns

- Cover slide that's just the topic title with no hook ("Data Engineering Tips")
- Slides that are just the same idea said slightly differently
- Last slide that only says "Follow for more!"
- All slides exactly the same length
- Excessive design text ("Swipe to learn more →") on every slide
- Carousel with fewer than 4 slides (not worth the swipe investment)

## Resources

- `references/slide-formats.md` — full skeletons for all 5 formats

## Related skills

- `ig-caption-writer` — write the post caption that goes with the carousel
- `ig-humanizer` — scrub AI tells from slide copy
- `ig-content-planner` — plan which weeks to use carousels
