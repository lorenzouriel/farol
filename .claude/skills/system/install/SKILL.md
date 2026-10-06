---
name: install
description: >
  Installs CompanyOS for the user's business. Interviews the user about the company,
  tone of voice, current focus, and visual identity, then fills `memory/company.md`,
  `memory/preferences.md`, `memory/strategy.md`, `resources/identity/design-guide.md`, and adapts
  `CLAUDE.md` according to the selected profile. Use when the user asks to run /install.
---

# /install - Initial CompanyOS Setup

This is the first command the user runs after cloning the repository. Treat it as a discovery conversation: ask one thing at a time, listen carefully, and keep the setup moving. The goal is for the system to know who the company is, how it speaks, and where day-to-day friction lives.

## Phase 0 - Pre-check

### Folder name

Check the current folder name. If it is `companyos`, `CompanyOS`, `CompanyOS-main`, `company-os`, `new-company`, `meu-negocio`, or another generic variation, say:

> "I noticed this folder still has a generic name ('<current-name>'). Ideally, the folder should have your business name, not 'CompanyOS'. When we finish setup, I will remind you to rename it. Shall we continue?"

### Existing setup

Check whether any memory file already has real content:

- `memory/company.md`
- `memory/preferences.md`
- `memory/strategy.md`
- `resources/identity/design-guide.md`

If one already has real content, ask whether to update it or keep it.

## Phase 1 - Profile

Ask which profile best fits:

1. **Solopreneur / solo creator** - one person, personal brand + business
2. **Freelancer** - serves clients, organizes by project/client
3. **Agency / consultancy** - small team delivering for several clients
4. **Company** - established company with departments

This determines which template from `resources/templates/profiles/` to apply.

## Phase 2 - Interview

Ask these questions one by one:

**Business**
1. "What do you call what you do? (company name, or your name if it is a personal brand)"
2. "What does your company deliver, in one sentence as you would explain it to a neighbor?"
3. "Who pays you? Describe the real client profile in one or two sentences."
4. "Do you work alone or with a team? If there is a team, how many people and what does each person do?"

**Tone**
5. "Paste a real recent writing sample: an Instagram caption, client email, anything. I will use it to calibrate your writing style."
6. "What annoys you in writing? Examples: guru jargon, formal corporate greetings, too many emojis, 'synergy', 'leverage'."

**Current focus**
7. "What is the bottleneck in your business today?"
8. "If I could take one weekly repeated task off your plate, what would it be?"

**Visual identity**
9. "Do you already have a visual identity? If yes, send the main colors and font."
10. "Do you have a logo? If yes, put it in `identity/logo.png` or `.svg` and confirm."

## Phase 3 - Fill files

### `memory/company.md`
Fill from questions 1-4. Keep it simple: name, what it does, client profile, team.

### `memory/preferences.md`
- **Tone of voice:** derive from the real writing sample.
- **What to avoid:** use the answer to question 6.
- **General style:** concise summary.

### `memory/strategy.md`
- **Current bottleneck:** answer 7.
- **To take off the user's plate:** answer 8, marked as a candidate for `/map-routines`.

### `resources/identity/design-guide.md`
If colors/fonts/logo were provided, fill the corresponding fields. If not, leave placeholders and say:

> "I left `resources/identity/design-guide.md` blank. When you define a visual identity, edit it there - carousel, proposal, and slide skills read it before creating visuals."

### `CLAUDE.md`
Take the matching template from `resources/templates/profiles/claude-md-<profile>.md`, adapt it with the business name and folders mentioned in the answers, and overwrite the root `CLAUDE.md`.

## Phase 4 - Summary

Show what was configured:

```
Done. CompanyOS now knows:

✓ Business context: memory/company.md
✓ Tone of voice: memory/preferences.md
✓ Current focus: memory/strategy.md
✓ Brand: resources/identity/design-guide.md [filled | blank - fill later]
✓ Workspace rules: CLAUDE.md
```

## Phase 5 - Rename folder if needed

If the folder still has a generic name, derive a slug from the business name (lowercase, hyphens for spaces, no accents or special characters — "Acme Consulting" → `acme-consulting`) and show the rename command:

**macOS / Linux:**
```
mv ../company-os ../acme-consulting
```

**Windows (PowerShell — run in the parent directory):**
```
Rename-Item company-os acme-consulting
```

Tell the user: close Claude Code, rename the folder, then reopen it from the new path so Claude Code picks up the correct working directory.

## Phase 6 - Next step

Close with:

> "Done. CompanyOS now knows you.
>
> From now on, start each session with `/open`.
> When you want content, SEO plan, campaign, or anything else, just ask.
> When you want to save to GitHub, use `/save`."

If the user mentioned a repeated weekly task, add:

> "You mentioned repeating '<answer from question 8>' every week. Later, run `/map-routines` and I can turn that into a skill."

## Rules

- Do not invent data. If an answer is vague, record it as received or leave a clear placeholder.
- Do not leave "this file will be filled by /install" notices in final files.
- Setup should take 5-7 minutes at most.
- Do not ask extra questions unless clearly needed.
