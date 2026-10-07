# CompanyOS - Business operating system

Your company runs on top of this file. This is where the CompanyOS
operating rules live - how Claude reads context, learns from corrections,
keeps everything updated, and creates new skills as the operation evolves.

This file is editable. When `/install` runs, it appends the specific
rules for your business to the end of this page.

---

## Business context

At the start of every conversation, read the following files (when they
exist and are filled in):

1. `memory/company.md` - who the user is, what they do, how the business works
2. `memory/preferences.md` - tone of voice, writing style, what to avoid
3. `memory/strategy.md` - current focus, priorities, deadlines

Use this information as the basis for any answer or decision. When
suggesting priorities, formats, or approaches, consider the current focus
described in `strategy.md`.

For any visual task (carousel, post, landing page), consult
`resources/identity/design-guide.md` as the style reference.

There is no need to list what was read or confirm the reading. Just use
the context naturally.

Never reference memory files by name in your responses. Do not say "your company.md says..." or "based on strategy.md..." or "I can see in preferences.md...". Never announce that you are reading files. The context is invisible: it shapes your answers without appearing in them.

---

## Workflow

Before executing any task, check whether a relevant skill exists in
`.claude/skills/`. If you find one, follow the skill instructions. If
you do not find one, execute the task normally.

When completing a task that did not have a skill but seems repeatable
(the user will probably ask for it again in the future), ask:

> "This could become a skill for next time. Do you want me to create it?"

Do not ask for one-off tasks or simple questions. Only ask when the
repetition pattern is clear.

---

## Learn from corrections

When the user corrects something, improves an answer, or gives an
instruction that seems permanent (phrases like "actually it is like
this", "do not do this anymore", "I prefer it this way", "whenever...",
"avoid...", "next time..."), ask:

> "Do you want me to save this so you do not have to repeat it?"

If yes, identify where it makes the most sense to save:

- **About the business** (clients, services, market) -> `memory/company.md`
- **About preferences and style** (tone of voice, format, what to avoid) -> `memory/preferences.md`
- **About priorities and focus** (projects, goals, deadlines) -> `memory/strategy.md`
- **Behavior rule in this folder** -> this `CLAUDE.md`

Save with one clear new line, without reformatting the whole file.
Confirm by showing the added line.

Do not ask if the correction is obvious from the immediate context (for
example: "actually the file is called X"). Only ask when the information
has lasting value.

---

## Keep context updated

After finishing a task that changed something relevant (new client, new
skill, change of focus, new process, installed tool, changed structure),
ask:

> "This changed something in your context. Do you want me to update the memory?"

If yes, identify what to update:

- **Client, service, tool, team** -> `memory/company.md`
- **Priority or focus change** -> `memory/strategy.md`
- **Tone or style** -> `memory/preferences.md`
- **Folder, organization rule, created skill** -> `CLAUDE.md`
- **Visuals (colors, fonts, logo)** -> `resources/identity/design-guide.md`

Show the proposed change as a diff (the exact line being added or edited) before saving. Only then write it. Do not reformat the whole file, only add or edit the relevant line.

**When NOT to ask:**
- One-off tasks with no context impact (writing a standalone email, creating a post)
- Simple questions or conversations without action
- Changes already saved by the "Learn from corrections" block

**Tip:** run `/update` for a full scan when in doubt.

---

## Skill creation

When the user asks for a new skill:

1. Check whether a relevant template exists in `resources/templates/skills/`. If
   it does, use it as a base and adapt it to the context
2. Ask whether it is specific to this project or useful anywhere:
   - Specific -> `.claude/skills/skill-name/SKILL.md` (local)
   - Universal -> `~/.claude/skills/skill-name/SKILL.md` (global)
3. Read `memory/company.md` and `memory/preferences.md` to calibrate
   the skill content to the business context
4. If the skill needs support files (templates, examples), create them
   inside the skill folder
5. Follow Claude Code's native skill-creator flow

---

# Farol - CompanyOS

> Profile: **solo creator**. One person, one project, and the open
> research is the main asset.

## What this workspace is

The operations side of Farol: producing and scheduling content about the
studies, keeping supporters engaged, and running the creator's routines.
It is also where studies are researched and built before publication.

**Branches:**
- `dev` - the workshop. This CompanyOS layer (memory, skills, marketing,
  scripts) plus studies in progress under `projects/studies/<slug>/` or
  `projects/studies/<topic>/<slug>/`, created from `projects/studies/template/`.
  Data analysis, research, and everything else is controlled here.
- `main` - the public study repository. Only `README.md`, `AGENTS.md`,
  `studies/`, and `template/`. No CompanyOS files.

**Publishing a study:** when a study is finished on dev, copy only its
folder to main at `studies/<slug>/` (or `studies/<topic>/<slug>/`) and add
it to `studies/README.md`. Use `/publish-study`. Never merge dev into main:
it would delete `AGENTS.md`, overwrite `README.md`, and push the whole
CompanyOS layer into the public repo.

**Folder structure:**
- `memory/` - who Farol is, how it speaks, what is in focus
- `resources/identity/` - colors, fonts, logo, visual pattern
- `areas/marketing/` - content, SEO, campaigns (skill outputs)
- `resources/documents/` - analyses, emails, one-off documents
- `resources/scripts/` - utilities (generate image, post, render)
- `projects/` - time-bound initiatives
- `projects/studies/` - studies in progress (dev only; published to main's `studies/`)
- `inbox/` - files to analyze (CSV, PDF, spreadsheet)

## Who I am

Farol is a solo open-source project: open studies on countries,
economies, and societies, with sources, methods, and findings you can
inspect and build on. The name means "lighthouse": each study lights up
part of a country without claiming to describe all of it.

## What I produce

- Studies, each published as a dated report (`ANALYSIS.md` + `ANALYSIS.html`)
- Content that brings each study's findings to a wider audience (channels not defined yet)

## My audience

Supporters of the open-source project, who fund it through Buy Me a
Coffee, plus readers who want evidence they can check for themselves.

## Tone of voice

Short, calm, and built around evidence. Example: "Open questions.
Traceable evidence."

Avoid: guru jargon, stiff corporate greetings, too many emojis, and hype
words like "revolutionary" or "game-changing".

## Positioning

Transparency over authority: every claim comes with its source, method,
and limitations, so readers can inspect, challenge, reproduce, and extend it.

## System rules

- Save new content in `areas/marketing/content/<type>-<topic>-<date>/`
- Content about a study links to the study and cites its sources. Do not
  claim more than the study's findings support.
- Use `resources/identity/design-guide.md` for every visual

## Connected tools

- [ ] Google Calendar
- [ ] Google Drive
- [ ] Gmail
- [ ] Canva (needs authorization)

*(Check as MCPs are installed)*

## Recommended skills

**Core:**
- `/publish-study` — copy a finished study from dev to main
- `/system` — open, update, save, map-routines, new-project
- `/content` — content-planner, copywriting, humanizer, seo
- `/business` — approve-post, publish-topic, buffer

**Platform (pick once channels are defined):**
- `/linkedin`, `/x`, `/newsletters`, `/instagram`, `/youtube`

**Visual / formats:**
- `/visual` — diagrams and visual explainers for findings
- `/formats pdf` — downloadable study summaries

**Research:**
- `/research research-deep`, `/research synthesize`
