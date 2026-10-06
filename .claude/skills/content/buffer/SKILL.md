---
name: buffer
category: content
description: >
  Social media scheduling via Buffer CLI. Publish and schedule posts to Instagram,
  LinkedIn, YouTube, TikTok, and X. Free plan covers 3 channels. Uses the official
  Buffer CLI (npm install -g @bufferapp/cli). Authenticate with BUFFER_API_KEY.
type: cli
version: "1.0.0"
env:
  - BUFFER_API_KEY
categories: [social-media, automation, publishing, scheduling]
---

# /buffer — Buffer Publisher

Schedule and publish posts to social media using the Buffer CLI.

## Setup (one-time)

```bash
npm install -g @bufferapp/cli   # install CLI
buffer init                     # authenticate + set defaults
buffer install claude           # installs the official Buffer skill (optional — replaces this file)
```

Or skip `buffer init` and set the env var directly:
```bash
export BUFFER_API_KEY=your-token-here
```

Get your API key: **buffer.com → Settings → API**

Free plan: 3 channels, 10 queued posts/channel, 3,000 API requests/month.

---

## Key workflow

1. **List channels** — get channel IDs for your connected accounts
2. **Create post** — schedule or add to queue for the target channel
3. **Verify** — check post status

---

## Commands

### List connected channels
```bash
buffer channels list
```

### Get a specific channel
```bash
buffer channels get --id <channel-id>
```

### Create a post (add to queue)
```bash
buffer posts create \
  --channel-id <channel-id> \
  --scheduling-type automatic \
  --mode addToQueue \
  --text "Your post text here"
```

### Create a post (schedule to specific date/time)
```bash
buffer posts create --json '{
  "channelId": "<channel-id>",
  "schedulingType": "scheduled",
  "scheduledAt": "2026-06-02T10:00:00Z",
  "text": "Your post text here"
}'
```

### Create from file (for long posts)
```bash
# Write post to file first, then:
buffer posts create --input post.json
```

### Dry run (validate without posting)
```bash
buffer posts create --json '{"channelId": "abc", "text": "test"}' --dry-run
```

### List scheduled posts for a channel
```bash
buffer posts list --channel-id <channel-id>
```

### Check account
```bash
buffer account
buffer doctor   # diagnose setup issues
```

---

## Available operations

- **List Channels** — retrieve connected social media accounts and IDs
- **Create Post** — add to queue or schedule to a specific datetime
- **Edit Post** — update an existing scheduled post
- **Delete Post** — remove a scheduled post
- **List Posts** — view scheduled/queued posts per channel
- **Ideas** — create content ideas in Buffer's idea library
- **Dry Run** — validate post payload without calling the API

---

## Rate limits (Free plan)

- 100 requests per 15 minutes
- 100 requests per 24 hours
- 3,000 requests per 30 days
- 1 API key

For higher limits, upgrade to Essentials ($5/mo/channel) or Team ($10/mo/channel).

---

## Channels supported

Instagram, LinkedIn, YouTube, TikTok, X (Twitter), Facebook, Pinterest, Mastodon, Bluesky, Threads, Google Business Profile, Shopify

---

## Notes

- Free plan: maximum 3 channels — choose Instagram + LinkedIn + YouTube to start
- 10-post queue per channel on Free (resets as posts publish — not a monthly cap)
- If you need more than 3 channels, switch to Blotato (MCP native, $29/mo, unlimited channels)
- Buffer CLI generates the GraphQL request from the schema — use `buffer schema describe posts create` to inspect the full input shape
- Official skill auto-install: `buffer install claude` writes an up-to-date skill to `~/.claude/skills/buffer/SKILL.md`