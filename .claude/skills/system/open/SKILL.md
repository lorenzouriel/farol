---
name: open
description: >
  Opens a work session by loading the business memory (company, preferences, strategy, identity)
  and returns a short summary to the user. Use when the user says "open",
  "start the day", "/open", or on the first turn of a session after /install.
---

# /open - Start Session

Short and direct. The goal is to load context and return a one-sentence synthesis so the user can start working.

## Steps

1. Read, if they exist:
   - `memory/company.md`
   - `memory/preferences.md`
   - `memory/strategy.md`
   - `resources/identity/design-guide.md` (only to know whether it is filled or blank)
2. If `memory/company.md` is blank or contains only template placeholder text, stop here. Do not generate the session card. Say:
   > "CompanyOS is not configured yet. Run `/system install` — it takes 5 minutes and the system will know your business."
   Do not list which files are missing. Do not offer to continue anyway.
3. If the files have content, respond in this format:

```
[Business name] - [what it does in 5-8 words]
Current focus: [one line from strategy]
Style: [one short line from preferences/design]

Ready. What are we doing?
```

## Rules

- Do not list which files were read. Do not confirm reading. Just use the context.
- If there is no strategy, use: "Current focus: not defined yet."
- If there is no visual identity, do not mention it unless the task is visual.
- Do not ask questions beyond "what are we doing?"
