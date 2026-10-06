---
name: motion-approved
description: >
  Finalizes an approved motion-design video. Once the user approves the video and wants no
  more changes, this deletes the entire Remotion project that produced it (src, public,
  node_modules, configs, scripts) and keeps only the final video file in the content folder.
  Use after a video is approved, or when the user says "motion approved", "video approved",
  "finalize the video", "clean the video folder", or "keep only the mp4".
---

# Motion Approved

Post-processing companion to `motion-design`. Once a video is approved, this turns the
working folder into a clean deliverable: **just the final video, nothing else.** The
Remotion project that built it is removed.

> Destructive. It deletes files. Always confirm the target folder and show the deletion list
> before removing anything. Verify the final video exists FIRST.

---

## What it keeps vs. deletes

| Keep | Delete |
|---|---|
| Final video files (`.mp4 .mov .gif .webm`) | `src/`, `public/`, `out/` (after moving the video out) |
| | `node_modules/`, `package*.json`, `remotion.config.ts`, `tsconfig.json` |
| | any `.ts`, `.tsx`, `.js`, `.json`, `.md`, or other project file |

Net result: `<name>.mp4` (at the content folder root) and nothing else.

---

## Inputs

- **Target folder** — the video's content working folder
  (e.g. `areas/marketing/content/<YYYY>/<MM>/WEEK <NN>/<platform>/<name>/`).
  If the user doesn't name one, list candidate folders and ask, or offer the most recent.

---

## Workflow

### 1. Locate + verify
Identify the target folder. Confirm a final video file exists (`.mp4` / `.mov` / `.gif`).
**If no video is present, stop** — there is nothing approved to keep; do not delete.

### 2. Surface the video
If the render landed in a subfolder (Remotion's default is `out/`), move it to the content
folder root and give it a clean name (`<name>.mp4`):
```bash
# example
mv out/*.mp4 "./<name>.mp4"
```

### 3. Confirm
Show the folder contents and state exactly what will be kept and deleted.
**Get explicit confirmation before any deletion.**

### 4. Clean the folder
Delete everything except video files.

**PowerShell** (run from inside the content folder):
```powershell
Remove-Item -Recurse -Force .\node_modules -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File | Where-Object { $_.Extension -notmatch '(?i)\.(mp4|mov|gif|webm)$' } | Remove-Item -Force
Get-ChildItem -Recurse -Directory | Where-Object { @(Get-ChildItem $_.FullName -Recurse -File).Count -eq 0 } | Remove-Item -Recurse -Force
```

**Bash:**
```bash
rm -rf node_modules
find . -type f ! -iregex '.*\.\(mp4\|mov\|gif\|webm\)' -delete
find . -type d -empty -delete
```

### 5. Report
Show the final folder (just the video) and the file path.

---

## Rules

- Never delete before confirming the final video exists.
- Never delete before showing the keep/delete list and getting confirmation.
- Operate only on the single target folder — never recurse into sibling content folders.
- Keep every video file; everything else (the Remotion project) goes.
