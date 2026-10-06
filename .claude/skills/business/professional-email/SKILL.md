---
name: professional-email
description: >
  Drafts professional emails from loose context. Use when the user says
  "write an email to", "I need to send an email about", "how do I answer this",
  or "make an email for [client/person]".
---

# /professional-email - Professional Email

## Context to read

- **Business context:** `memory/company.md`
- **Tone of voice:** `memory/preferences.md`

## Flow

### Step 1 - Collect context

If the user did not provide enough information, ask:

1. "Who is the email for? (name, role, relationship with you)"
2. "What needs to be communicated or decided?"
3. "What tone do you want: direct, warm, formal, or firm?"

If the user gave loose context, extract what you can and proceed.

### Step 2 - Write the email

Rules:

- Subject line first.
- Human, clear, and specific.
- Tone proportional to the relationship (new client = more careful, old partner = more direct).
- No corporate filler.
- If it is a reply, reference the context in the first line.
- End with a clear next step.

Format:

```markdown
**Subject:** [subject]

Hi [Name],

[body]

[closing],
[User name, from memory/company.md]
```

### Step 3 - Present tone options when useful

If the situation is sensitive (collection, complaint, negotiation), provide 2 versions:

- **Softer**
- **More direct**

Let the user choose.
