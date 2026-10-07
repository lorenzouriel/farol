---
name: publish-study
description: >
  Publishes a finished Farol study from the dev branch to the public main
  branch: copies only the study folder from `projects/studies/<slug>/` (dev)
  to `studies/<slug>/` (main), checks it is ready, and updates the study index.
  Use when the user says "publish study", "publish the study", "send study to
  main", "the study is done", or "/publish-study".
---

# /publish-study - Publish A Study From Dev To Main

Farol has two branches:

- `dev` - the workshop. Studies are built in `projects/studies/<slug>/` or
  `projects/studies/<topic>/<slug>/`, next to the CompanyOS layer.
- `main` - the public study repository. Only `README.md`, `AGENTS.md`,
  `studies/`, and `template/`.

Publishing copies one study folder from dev to main. **Never merge dev into
main**, never cherry-pick dev commits onto main, and never copy anything
outside the study folder.

## Step 1 - Pick the study

1. Run `git status`. If the working tree is dirty, stop and ask the user to
   save (commit) on dev first. The copy reads from the committed `dev` tree.
2. List study folders under `projects/studies/` (skip `template/` and
   `README.md`). Ask which one to publish if the user did not say.
3. Confirm the target path on main: `projects/studies/<path>` on dev becomes
   `studies/<path>` on main (a `<topic>/<slug>` path keeps its topic folder).

## Step 2 - Readiness check (on dev)

Read the study's `README.md`, `ANALYSIS.md`, `ANALYSIS.html`,
`sources/sources.yaml`, and `docs/methodology.md`. Report every problem found,
then ask whether to fix first or publish anyway. Check:

- No template placeholders left (`[Study title]`, `[One bounded question`,
  "Template only", other `[...]` placeholder text, `Not yet verified`).
- README has question, countries, period covered, status, and last verified date.
  Status should be `reviewed` (or the user explicitly accepts another status).
- `ANALYSIS.md` and `ANALYSIS.html` agree: same findings, numbers, citations,
  dates, and limitations. Flag any claim present in one but not the other.
- Every source ID cited in `ANALYSIS.md` exists in `sources/sources.yaml`, and
  each source has a retrieval date.
- Unused template folders and sections were removed.
- No secrets, credentials, private personal data, or files that cannot be
  redistributed (check `data/` especially; large or restricted inputs should
  be referenced, not stored).
- Change history in the README has an entry for this version.

Do not edit findings yourself during this check. Fixes to the research
happen on dev, are committed, and then the skill runs again.

## Step 3 - Copy to main

Show the user the exact commands and the list of files that will be copied
(`git ls-tree -r --name-only dev -- projects/studies/<path>`), then run:

```bash
git switch main
git pull --ff-only
mkdir -p studies
git archive dev projects/studies/<path> | tar -x --strip-components=2 -C studies
```

`--strip-components=2` removes the `projects/studies/` prefix, so the files
land at `studies/<path>/`.

If `studies/<path>/` already exists on main (a republish or revision), show
`git diff --stat` after the copy so the user sees what changed. Files deleted
from the study on dev must also be removed on main: compare the two file lists
and `git rm` the extras.

## Step 4 - Update the index on main

Edit `studies/README.md` on main:

- Remove the "No studies have been started yet" line if it is still there.
- Add (or update) one table row: relative link to the study README, question,
  countries, period covered, status. Take the values from the study README.
- Group by topic when the study sits under a topic folder.

Mirror the same row in `projects/studies/README.md` on dev in Step 6.

## Step 5 - Review and commit on main

1. Run `git status` and confirm only `studies/` changed. If anything outside
   `studies/` is staged or modified, stop and tell the user.
2. Show the diff summary and ask for confirmation.
3. Commit: `git add studies/ && git commit -m "feat: publish <slug> study"`
   (use `"docs: update <slug> study"` for a revision).
4. Ask before pushing: `git push origin main`.

## Step 6 - Back to dev

1. `git switch dev`
2. Update `projects/studies/README.md` on dev with the same index row and the
   status `reviewed` (published).
3. Commit on dev and offer to push.
4. Suggest the next step: content about the study (`/content`), following the
   rule that content links to the published study on main and claims no more
   than its findings support.

## Rules

- Main never receives CompanyOS files, memory, skills, marketing content, or
  in-progress studies.
- Changes to `template/` or `AGENTS.md` on main are separate tasks, not part
  of publishing a study.
- If any git command fails, stop, show the error, and make sure the user ends
  up back on `dev`.
