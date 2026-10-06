# resources/documents/ - general CompanyOS outputs

Folder for any output that is not pure marketing (does not fit in
`areas/marketing/`).

## What goes here

- **Analyses** from `/analyze-data` - executive summaries of CSV/XLSX/PDF
- **Emails** drafted by `/professional-email`
- **Miscellaneous reports** that are not ads reports
- **Documents** that skills generate and you need to send/print/attach

## Suggested structure

```
resources/documents/
|-- analyses/        reports from /analyze-data
|-- emails/          drafts from /professional-email
`-- other/           anything loose
```

Skills know where to save - you do not need to create subfolders
manually. If a skill asks where to save, it will suggest here.

## Why separate it from `areas/marketing/`?

`areas/marketing/` is the living history of marketing work - pieces,
campaigns, accumulated SEO.

`resources/documents/` is "one-off thing generated today" - a report you send to the
client and never look at again, an email draft you copy and paste into
Gmail.

The split matters for `/save` (commit) and for clarity when navigating
the folder.
