---
name: map-routines
description: >
  Maps repetitive tasks the user does day to day and generates personalized skills
  to automate them. Use when the user asks "/map-routines", "create custom skills",
  "automate my tasks", or "what can be automated".
---

# /map-routines - Turn Repetitive Tasks Into Skills

Discovery + creation skill. The goal is to turn what the user repeats into active automations.

## Step 1 - Discovery interview

Ask:

1. "Which 3 tasks do you repeat every week and wish you did not have to think about anymore?"
2. "For each one, what is the typical input?"
3. "What output do you expect?"

## Step 2 - Check catalog

Read `resources/templates/skills/catalog.md` to see whether any mentioned task is already covered by a native Claude Code skill or a CompanyOS-validated skill. If yes, suggest the existing skill instead of creating a new one.

## Step 3 - Skill proposals

For each uncovered task, propose:

```markdown
### Skill: /<name>
**What it does:** [one sentence]
**Input:** [what the user provides]
**Output:** [what it creates]
**Dependencies:** [context files, identity files, or external tools]
```

Ask:

> "Which skills from this list do you want me to create now?"

## Step 4 - Create approved skills

For each approved skill:

1. Create `.claude/skills/<name>/`
2. Create `SKILL.md` with name, description, trigger rules, workflow, output format, and dependencies
3. If templates or examples are needed, create them inside the skill folder
4. Calibrate tone and rules using `memory/preferences.md` and `memory/company.md`

## Step 5 - Summary

Show:

```
Created:
- /skill-one -> .claude/skills/skill-one/SKILL.md
- /skill-two -> .claude/skills/skill-two/SKILL.md

To use: type / and the skill name in any session.
To adjust later: edit the corresponding SKILL.md.
```

## Rules

- Do not create a skill for a one-off task.
- Do not create more than 5 skills per mapping session.
- Prefer simple, reliable skills over broad generic automations.
- If a skill depends on a tool the user does not have, warn before creating it and offer a simplified version.
