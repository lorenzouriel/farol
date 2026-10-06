# Setup Guide

> No technical experience required. This takes about 10 minutes.

---

## What you need

One app: **Claude Code**.

That is it. No terminal experience needed, no coding, no configuration files. Claude Code is a chat interface that can also read and write files on your computer.

Download it at **[claude.ai/download](https://claude.ai/download)** — it is free to start.

---

## Step 1 — Get the files

You need to get a copy of CompanyOS onto your computer.

**Option A — Ask Claude to do it (easiest)**

1. Open Claude Code
2. Type this exactly:
   ```
   Clone https://github.com/mazzeoia/CompanyOS.git into the current folder, enter it and run /install
   ```
3. Press Enter and skip to Step 3

**Option B — Do it yourself (more control)**

If you have Git installed, open a terminal (on Mac: Terminal app; on Windows: PowerShell) and run:

```
git clone https://github.com/mazzeoia/CompanyOS.git
```

This creates a `CompanyOS` folder wherever you ran the command.

If you do not have Git:
1. Go to the repository URL
2. Click the green **Code** button → **Download ZIP**
3. Unzip the file — you now have a `CompanyOS` folder

---

## Step 2 — Open the folder in Claude Code

1. Open Claude Code
2. Click **Open folder** (or File → Open Folder)
3. Select the `CompanyOS` folder you just downloaded
4. Claude Code opens with the folder loaded

You should see a chat input at the bottom. That is where you type commands.

---

## Step 3 — Run the setup

In the chat input, type:

```
/system install
```

Press Enter.

CompanyOS will start a short interview. It asks one question at a time — answer honestly and naturally. There are no wrong answers. The system adapts to whatever you tell it.

The questions cover:
- What your business is called and what it does
- Who your clients are
- How you write (paste a real example — an email, an Instagram caption, anything)
- What you do not like in writing (jargon, emojis, corporate tone)
- What your biggest bottleneck is right now
- Whether you have a logo and brand colors

**This takes about 5-7 minutes.** You only do this once.

---

## Step 4 — Rename the folder

When setup finishes, CompanyOS will suggest a name for your folder based on your business.

Close Claude Code, rename the `CompanyOS` folder to your business name (e.g., `acme-consulting`), then open Claude Code again from the renamed folder.

**Why:** the folder becomes your business's workspace. "CompanyOS" is a generic name — your business deserves its own.

On Mac: right-click the folder in Finder → Rename
On Windows: right-click the folder in Explorer → Rename

---

## Step 5 — Start every session with /open

From now on, each time you open Claude Code in your business folder, type:

```
/open
```

This loads your business context and tells you what is in focus. It takes 3 seconds. Think of it as clocking in.

---

## Daily use — examples

Once setup is complete, just talk to Claude normally. Examples:

| What you want | What to type |
|---|---|
| Plan this week's content | `/content plan` |
| Write an Instagram carousel about X | `/instagram carousel` |
| Run full SEO research for my business | `/content seo` |
| Build a Google Ads campaign | `/business google-ad` |
| Analyze last week's ad results | `/business ads-report` |
| Write a professional email | `/business email` |
| Research a topic deeply | `/research deep` |
| Create a Word document | `/formats docx` |
| Save everything to GitHub | `/system save` |

You do not need to remember all of these. Just describe what you want in plain language and Claude will route to the right skill automatically.

---

## If something goes wrong

**"I don't see a chat input"**
Make sure you opened Claude Code with the CompanyOS folder loaded, not just the Claude Code app by itself. File → Open Folder → select your business folder.

**"/system install didn't work"**
Try typing just `/install` instead. If that does not work, type: `Run the install skill`.

**"The folder rename broke something"**
Open Claude Code from the renamed folder. If Claude seems confused about context, type `/system update` to rescan.

**"I want to redo the setup"**
Type `/system install` again. It will ask whether to overwrite the existing setup or update it.

**"I need help"**
Describe what you are trying to do in plain language in the chat. CompanyOS is designed to understand natural language — you do not need to use slash commands for everything.

---

## What you have set up

After following these steps, your workspace contains:

```
your-business/
├── CLAUDE.md              ← operating rules (auto-configured to your profile)
├── memory/
│   ├── company.md         ← who you are, what you do, your clients
│   ├── preferences.md     ← your tone of voice, what to avoid
│   └── strategy.md        ← your current focus and priorities
├── inbox/                 ← drop zone for raw files (PARA method)
├── projects/               ← active work with a deadline
├── areas/                  ← ongoing responsibilities
│   └── marketing/          ← content, SEO files, campaigns land here
├── resources/              ← reusable reference + one-off outputs
│   ├── identity/
│   │   └── design-guide.md   ← your brand colors, fonts, style
│   └── documents/          ← analyses, emails, one-off documents
├── archive/                ← finished projects and inactive areas
└── .claude/skills/        ← 70+ skills, all loaded and ready
```

Everything Claude generates goes into `projects/`, `areas/`, or `resources/`. Nothing is published without your confirmation. You are always in control.
