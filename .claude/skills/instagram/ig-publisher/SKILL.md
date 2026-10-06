---
name: instagram-publisher
description: >
  Publishes Instagram carousel posts from local images.
  Uploads images to imgBB (requires API key) for public hosting, creates Instagram
  media containers via the Graph API, and publishes the carousel.
  Supports 2-10 images per post and retrieves the real post permalink.
type: script
version: "1.0.0"
script:
  path: scripts/publish.js
  runtime: node
  invoke: "node --env-file=.env {skill_path}/scripts/publish.js --images \"{images}\" --caption \"{caption}\""
env:
  - INSTAGRAM_ACCESS_TOKEN
  - INSTAGRAM_USER_ID
  - IMGBB_API_KEY
categories: [social-media, publishing, instagram]
---

# Instagram Publisher

## When to use

Use the Instagram Publisher when you need to publish carousel posts directly to an Instagram Business account. This skill handles the full workflow: uploading images to imgBB (requires your own API key from https://api.imgbb.com/), creating Instagram media containers via the Graph API, and publishing the carousel. It supports 2-10 JPEG images per post.


## Instructions

### Workflow

1. List JPEG files in `squads/{squad}/output/images/` sorted by name.
   If no files found: stop and ask the user to add images before continuing.
2. Present the image list to the user with AskUserQuestion to confirm order.
3. Extract the caption from the content draft:
   - Use the hook slide text + CTA slide text
   - Max 2200 characters (Instagram limit)
4. Run the publish script:
   ```
   node --env-file=.env squads/{squad}/tools/publish.js \
     --images "<comma-separated-ordered-paths>" \
     --caption "<caption>"
   ```
   Add `--dry-run` to test the full flow without actually publishing.
5. On success: save the post URL and post ID to the step output file.
6. On failure: display the error and ask the user how to proceed.

### Constraints

- Images: JPEG only, 2-10 per carousel
- Caption: max 2200 characters
- Requires Instagram Business account (not Personal or Creator)
- Rate limit: 25 API-published posts per 24 hours

### Setup (first-time)

Copy `.env.example` to `.env` and fill in the two required variables:

```
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_USER_ID=
```

#### INSTAGRAM_ACCESS_TOKEN

Prerequisite: Instagram Business account connected to a Facebook Page, and an app created at [developers.facebook.com](https://developers.facebook.com/) (type: **Business**).

**To get a long-lived token (valid for 60 days):**

1. Open your app -> **Graph API Explorer**
2. In the top dropdown, select your app
3. Click **"Generate access token"**
4. Enable permissions:
   - `instagram_content_publish`
   - `instagram_basic`
   - `pages_read_engagement`
5. Click **"Generate access token"** and authorize - you will receive a short-lived token (1h)
6. Convert it to long-lived (60 days) with this GET:
   ```
   https://graph.facebook.com/oauth/access_token
     ?grant_type=fb_exchange_token
     &client_id={APP_ID}
     &client_secret={APP_SECRET}
     &fb_exchange_token={SHORT_TOKEN}
   ```
   _(APP_ID and APP_SECRET: your app -> Settings -> Basic)_
7. Copy `access_token` from the response and paste it into `.env`

> The token expires in 60 days. Repeat the process to renew.

#### INSTAGRAM_USER_ID

1. In Graph API Explorer (with the token above), make a GET request to:
   ```
   /me/accounts
   ```
2. Find your **Facebook Page** in the response and note the `id`
3. Make a GET request to:
   ```
   /{page-id}?fields=instagram_business_account
   ```
4. Copy the `id` inside `instagram_business_account` - this is your User ID

## Available operations

- **Publish Carousel** -- Upload images and publish a carousel post to Instagram
- **Dry Run** -- Test the full publishing flow without actually posting (use `--dry-run` flag)
- **Image Upload** -- Upload local JPEG images to imgBB (requires API key)
- **Status Check** -- Monitor media container processing status before publishing
