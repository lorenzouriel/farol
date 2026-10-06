---
name: new-project
description: >
  Creates a new project folder with a dedicated `CLAUDE.md`, after a short interview
  about the project (client, goal, expected deliverables). Use when the user says
  "new project", "new client", "/new-project", or asks to structure new work.
---

# /new-project - New Project Folder With Dedicated Context

When the user starts a new project, client, initiative, or product, create a folder with its own `CLAUDE.md` that inherits root context and adds project-specific rules.

## Step 1 - Interview

Ask:

1. "What is the project or client name?"
2. "Is it a new client, internal project, or personal initiative?"
3. "What is the goal?"
4. "What deliverables will it have? (ads, site, content, automation, proposal - can be more than one)"

## Step 2 - Choose location

Projects live under the PARA structure. Based on answer 2:

- **New client:** create in `projects/<Name>/`
- **Internal project:** create in `projects/<name>/`
- **Personal initiative:** create in `projects/<name>/` (or ask if the user prefers elsewhere)

A project is an effort with a goal **and** an end. When it ships or stalls, move the folder to `archive/`.

## Step 3 - Basic structure

Create:

- Project folder
- Project `CLAUDE.md` (inherited + specific instructions)
- Subfolders according to mentioned deliverables

## Step 4 - Project `CLAUDE.md`

Use:

```markdown
# [Project name]

> Project-specific context. This file complements the root CLAUDE.md.

## What this is

[Answer from step 1]

## Goal

[Answer from question 3]

## Deliverables

- [deliverable 1]
- [deliverable 2]

## Where to save things

- Briefings and context: this root folder
- Final outputs: according to deliverable folders

## Inherited context

This project automatically inherits tone of voice, brand, and business context from `memory/` and `resources/identity/` at the root. Do not duplicate that information here.

## Specific to this project

[Empty - fill with rules that only apply to this project as they are discovered]
```

## Step 5 - Summary

Reply:

```
Created: <path>

✓ Dedicated CLAUDE.md
✓ Folders: <list>

When working on this project, open the terminal inside the folder so I load the project CLAUDE.md together with the root one.
```

## Rules

- Folder name: preserve the user's recognizable name; spaces can become hyphens.
- Do not create unrequested subfolders.
- If a project/client already exists, ask whether to add inside it or create a suffixed folder.
