---
name: visual
description: >
  Visual design and production hub. Routes to sub-skills for diagrams, landing pages,
  motion video, and HTML visual explainers. Trigger on: "create a diagram", "excalidraw",
  "landing page", "make a video", "motion design", "visual explainer", "architecture diagram",
  "animated video", "HTML diagram", "visualize this".
---

# Visual — Design & Production

Orchestrator for all visual design and production tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/visual diagram` | `excalidraw-diagram/SKILL.md` | "create a diagram", "excalidraw", "architecture diagram", "visualize workflow", "draw this" |
| `/visual landing-page` | `landing-page/SKILL.md` | "landing page", "create a web page", "one-pager", "sales page", "product page" |
| `/visual motion` | `motion-design/SKILL.md` | "animated video", "motion design", "make a video", "Remotion", "video composition" |
| `/visual motion-approved` | `motion-approved/SKILL.md` | "video approved", "finalize video", "clean up remotion project", "export video" |
| `/visual explainer` | `visual-explainer/SKILL.md` | "visual explainer", "HTML diagram", "visualize this", "architecture overview", "make this visual" |
