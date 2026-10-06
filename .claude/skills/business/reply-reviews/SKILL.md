---
name: reply-reviews
description: >
  Writes short, human replies to Google Business Profile reviews. Keeps the pattern:
  client name, varied thank-you, concrete phrase about the product/service, optional emoji.
  Use when the user asks to answer Google reviews.
---

# /reply-reviews - Google Review Replies

## Context

- **Tone of voice:** `memory/preferences.md`
- **Business context:** `memory/company.md`

## Reply pattern

Replies are **short** (1 to 2 sentences), **personal**, and **concrete**.

Rules:

1. Mention the client's first name when it is clear.
2. Vary the thank-you. Do not repeat the same opening.
3. Pull something specific from the review or business.
4. Optional emoji only if it matches the brand tone.
5. Follow `memory/preferences.md`.

Avoid generic phrases like "your feedback is very important to us" or "we are always available".

## Flow

### Step 1 - Extract reviews

The user may paste text, a screenshot, or a review list. Extract:

- Name
- Rating
- Review text
- Context clue

If it is an image, read and transcribe the data before replying.

### Step 2 - Write the reply

For each review, write **one reply** following the pattern.

For 3-star or lower reviews, stop and align with the user before replying.

### Step 3 - Output

List each reply below its review, ready to paste into GMB:

```markdown
**[Name] - [rating]**
> [review]

-> [reply]
```

If the user asks to keep a record, save in `areas/marketing/google-reviews/YYYY-MM-DD-replies.md` with review + published reply.

## Rules

- Do not promise anything the company does not control.
- Do not ask the client to contact by DM/phone unless the user asks.
- Do not use the client's full name in the public reply.
- Do not mention competitors.
- For negative reviews: acknowledge, do not defend, and only offer a private channel if the user authorizes it.
