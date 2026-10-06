---
name: save
description: >
  Saves CompanyOS work to GitHub (commit + push). On first use, configures the
  remote repository. Use when the user says "save", "save to GitHub", "commit",
  "push", or "/save".
---

# /save - Save To GitHub

## First-time setup

1. Check whether the folder is already a git repository.
2. If there is no remote, ask:
   > "I do not see a GitHub remote yet. Do you already have a repository URL?"
   > 1. Yes, I will send the URL
   > 2. No, I will create one now - give me a repository name
3. If the user sends a URL: run `git init` if needed, `git add .`, `git commit -m "Initial CompanyOS setup"`, `git branch -M main`, `git remote add origin <URL>`, `git push -u origin main`.
4. If the user wants to create one and `gh` is installed: run `git init`, create the initial commit, and `gh repo create <name> --private --source=. --push`.

## Normal save

1. Run `git status`.
2. Summarize changed files.
3. If the user provides a message, use it. Otherwise generate one line, such as "Update X", "Add Y", or "Create proposal for client Z".
4. Run `git add .`, `git commit -m "<message>"`, and `git push`.

## Rules

- Never commit secrets from `.env`.
- If push fails, show the error and suggest the next concrete fix.
- Keep commit messages short and human.
