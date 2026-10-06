# Tools Catalog

Reference for APIs, CLIs, and connectors that can be used inside Claude
Code skills. Check this file before creating new skills to see what is
already available.

---

## Create Visuals (HTML To PNG)

### Playwright CLI
**What it does:** Renders any HTML as a PNG image (carousels, slides, proposals, cards)
**Requires an account:** No, runs locally
**How to install:**
```bash
npx playwright install chromium
```
**How to use in a skill:**
```bash
npx playwright screenshot --viewport-size=1080,1350 --full-page "file:///path/slide.html" "slide.png"
```
**Common sizes:**
- Instagram feed: 1080x1350
- Instagram/TikTok story: 1080x1920
- 16:9 slide: 1920x1080
- Square card: 1080x1080

---

## Publish On The Web

### Cloudflare Pages API
**What it does:** Publishes HTML files with a public link (proposals, landing pages, studies)
**Requires an account:** Yes, Cloudflare (free)
**Configure:** Save `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` in `.env`
**When to use:** Whenever a skill generates HTML that needs to be shared through a link

---

## Schedule Social Media

### Buffer API
**What it does:** Queues posts to Instagram, LinkedIn, X, Facebook, TikTok with scheduled publish times
**Requires an account:** Yes, Buffer (free up to 3 channels)
**Configure:** Save `BUFFER_ACCESS_TOKEN` in `.env`
**How to use in a skill:**
```bash
curl -X POST "https://api.bufferapp.com/1/updates/create.json" \
  -d "access_token=$BUFFER_ACCESS_TOKEN&profile_ids[]=<id>&text=<text>"
```
**When to use:** When the user wants to schedule posts instead of publishing immediately
**Connected to:** `/content buffer` skill

---

## Publish On Social Media

### Post for Me API
**What it does:** Publishes posts to Instagram and TikTok directly from Claude Code
**Requires an account:** Yes, postforme.dev
**Configure:** Save `POSTFORME_API_KEY` in `.env`
**How to use in a skill:**
```bash
node --env-file=.env scripts/publish-postforme.js
```
**When to use:** Carousel, visual content, and automatic publishing skills

---

## Scrape The Web

### Apify API
**What it does:** Runs cloud scraping actors — LinkedIn profiles, Instagram data, Google results, e-commerce, maps
**Requires an account:** Yes, Apify (free tier available — $5 free credit/month)
**Configure:** Save `APIFY_TOKEN` in `.env`
**How to use in a skill:**
```bash
curl -X POST "https://api.apify.com/v2/acts/{actor-id}/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": [{"url": "https://..."}]}'
```
**Common actors:** `apify/instagram-scraper`, `apify/linkedin-profile-scraper`, `apify/google-search-scraper`
**When to use:** `/research apify` skill — competitor research, lead scraping, market data
**Connected to:** `/research apify` skill

---

## Fetch Web Content

### WebFetch (native)
**What it does:** Reads the content of any URL and returns it as text
**Requires an account:** No, already included in Claude Code
**When to use:** Reference research, reading articles, fetching website data

### WebSearch (native)
**What it does:** Searches Google and returns results
**Requires an account:** No, already included in Claude Code
**When to use:** When the user needs research before creating content

### Jina Reader
**What it does:** Converts any URL into clean markdown (better than WebFetch for long articles)
**Requires an account:** No
**How to use:** Access `https://r.jina.ai/{URL}` via WebFetch
**When to use:** Extracting text from articles, blog posts, and pages with heavy HTML

---

## Extract Video Content

### yt-dlp (CLI)
**What it does:** Downloads transcripts/captions from YouTube videos
**Requires an account:** No, runs locally
**How to install:**
```bash
brew install yt-dlp
```
**When to use:** Skills that start from a video to create content (carousel, newsletter, script)

---

## Generate Images With AI

### Gemini (Google AI)
**What it does:** Generates images from text
**Requires an account:** Yes, Google AI Studio (free up to a limit)
**Configure:** Save `GEMINI_API_KEY` in `.env`
**When to use:** Covers, illustrations, images for posts

### DALL-E (OpenAI)
**What it does:** Generates images from text
**Requires an account:** Yes, OpenAI (paid)
**Configure:** Save `OPENAI_API_KEY` in `.env`
**When to use:** Alternative to Gemini for image generation

---

## Connect Platforms (MCPs)

MCPs are connectors that give direct access to platforms inside Claude
Code. Claude starts using these connectors automatically when it makes
sense.

To check which MCPs are already installed: `claude mcp list`
To remove an MCP: `claude mcp remove mcp-name`

### Notion
**What it does:** Accesses projects, databases, briefings, and tasks in Notion
**Requires an account:** Yes, API key at notion.so/my-integrations
**How to install:**
```bash
claude mcp add notion -- npx -y @notionhq/notion-mcp-server
```
**When to use:** Skills that need to read/write tasks, client bases, documents

### Gmail
**What it does:** Reads and composes emails without leaving Claude Code
**Requires an account:** Yes, Google OAuth
**How to install:**
```bash
claude mcp add gmail -- npx -y @gongrzhe/server-gmail-autoauth-mcp
```
**When to use:** Email, follow-up, and client communication skills

### Google Calendar
**What it does:** Views calendar, creates events, and finds available times
**Requires an account:** Yes, Google OAuth
**How to install:**
```bash
claude mcp add google-calendar -- npx -y @gongrzhe/server-google-calendar-autoauth-mcp
```
**When to use:** Scheduling, planning, and meeting organization skills

### Canva
**What it does:** Accesses designs and creates new visual assets directly through Claude
**Requires an account:** Yes, Canva Pro
**How to install:**
```bash
claude mcp add canva -- npx -y @canva/canva-mcp-server
```
**When to use:** Design, visual creation, and brand material skills

### Facebook Ads (Meta)
**What it does:** Manages Meta campaigns (Facebook/Instagram Ads)
**Requires an account:** Yes, Meta Business token
**When to use:** Paid media management and performance reporting skills

### Google Ads
**What it does:** Accesses and edits campaigns, fetches performance data
**Requires an account:** Yes, Google Ads credentials
**When to use:** Paid media management and performance reporting skills

### N8N
**What it does:** Triggers automations and workflows in N8N
**Requires an account:** Yes, N8N instance + API key
**How to install:**
```bash
claude mcp add n8n -- npx -y n8n-mcp
```
**When to use:** Skills that need to trigger external automations

### Supabase
**What it does:** Database and complete backend
**Requires an account:** Yes, Supabase project
**When to use:** Skills that need to store data, authentication, backend

### Telegram
**What it does:** Sends and receives messages through a Telegram bot
**Requires an account:** Yes, bot token from BotFather
**When to use:** Notification and automated communication skills

---

## How To Add New Tools

If you use an API or tool that is not on this list, add it here using
this format:

```markdown
### Tool Name
**What it does:** [one-sentence description]
**Requires an account:** [Yes/No]
**Configure:** [what to save in .env, if applicable]
**How to use in a skill:** [command or instruction]
**When to use:** [what type of skill it makes sense for]
```
