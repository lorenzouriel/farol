# Skills Catalog

External skills ready to install. Use this as a reference when creating
new skills with `/map-routines`, or install the ones that make sense
for your business directly.

> Global skills live in `~/.claude/skills/` and work in any project.
> Local skills live in `.claude/commands/` and only work in this project.

---

## Write Copy And Sales Text

### Schwartz Copy (direct response)
**What it does:** Writes sales copy using Eugene Schwartz's methodology (Breakthrough Advertising). Diagnoses market awareness and sophistication before generating any text.
**Good for:** Landing pages, sales emails, VSLs, sales letters, capture pages
**How to install:** Already comes as a global skill. Call with `/schwartz-copy`
**Source:** Skill validated by CompanyOS

### Ogilvy Copy (brand and positioning)
**What it does:** Generates institutional copy using David Ogilvy's methodology. Deep research, big idea, informative headlines.
**Good for:** Brand manifestos, institutional campaigns, taglines, brand voice, positioning
**How to install:** Already comes as a global skill. Call with `/ogilvy-copy`
**Source:** Skill validated by CompanyOS

---

## Create Interfaces And Web Pages

### Frontend Design
**What it does:** Creates complete web interfaces with high-quality design. Generates ready-to-use HTML/CSS/React code with a professional look that avoids generic AI aesthetics.
**Good for:** Landing pages, dashboards, web components, product pages
**How to install:** Already native in Claude Code. Call with `/frontend-design`
**Source:** Native Claude Code skill

---

## Create Visuals And Art

### Canvas Design
**What it does:** Creates visual art in PNG and PDF using design principles. Posters, covers, graphic pieces.
**Good for:** Ebook covers, banners, visual pieces, thumbnails
**How to install:** Already native in Claude Code. Call with `/canvas-design`
**Source:** Native Claude Code skill

---

## Work With Documents

### PDF
**What it does:** Handles PDFs: extracts text and tables, creates new PDFs, joins/splits documents, fills forms.
**Good for:** Extracting data from contracts, creating PDF reports, filling forms
**How to install:** Already native in Claude Code. Call with `/pdf`
**Source:** Native Claude Code skill

### DOCX
**What it does:** Creates and edits Word documents with formatting, tracked changes, and comments.
**Good for:** Formal proposals, contracts, documents for clients who request Word
**How to install:** Already native in Claude Code. Call with `/docx`
**Source:** Native Claude Code skill

### PPTX
**What it does:** Creates and edits PowerPoint presentations with layouts, speaker notes, and formatting.
**Good for:** Client presentations, sales decks, training materials
**How to install:** Already native in Claude Code. Call with `/pptx`
**Source:** Native Claude Code skill

### XLSX
**What it does:** Creates and edits spreadsheets with formulas, formatting, and charts.
**Good for:** Financial reports, spreadsheet dashboards, data analysis
**How to install:** Already native in Claude Code. Call with `/xlsx`
**Source:** Native Claude Code skill

---

## Write Documents And Specs

### Doc Co-Authoring
**What it does:** Guided flow for co-writing documents. Interviews you, iterates drafts, and validates that the document works for the reader.
**Good for:** Technical proposals, specs, decision documents, SOPs
**How to install:** Already native in Claude Code. Call with `/doc-coauthoring`
**Source:** Native Claude Code skill

---

## Extract Video Transcripts

### YT Transcript
**What it does:** Extracts transcripts from YouTube videos using yt-dlp. Supports multiple languages.
**Good for:** Creating content from videos (carousels, newsletters, posts)
**Requires:** yt-dlp installed (`brew install yt-dlp`)
**How to install:** Already comes as a global skill. Call with `/yt-transcript`
**Source:** Skill validated by CompanyOS

---

## Test Sites And Apps

### Webapp Testing
**What it does:** Tests local web applications using Playwright. Captures screenshots, verifies functionality, reads browser logs.
**Good for:** Testing landing pages before publishing, checking that everything works at different sizes
**How to install:** Already native in Claude Code. Call with `/webapp-testing`
**Source:** Native Claude Code skill

---

## Create New Skills

### Skill Creator
**What it does:** Guide for creating new skills from scratch. Helps structure, define triggers, and test.
**Good for:** When `/map-routines` does not cover what you need and you want to create something more complex
**How to install:** Already native in Claude Code. Call with `/skill-creator`
**Source:** Native Claude Code skill

---

## How To Add New Skills To This Catalog

If you tested a skill and want to add it here for future reference:

```markdown
### Skill Name
**What it does:** [one-sentence description]
**Good for:** [practical use cases]
**How to install:** [command or instruction]
**Source:** [where it came from - native skill, created by you, or third party]
```
