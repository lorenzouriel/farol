---
name: formats
description: >
  Document and file format toolkit. Routes to specialized sub-skills for Word documents,
  PDFs, PowerPoint presentations, and Excel spreadsheets. Trigger on: "create a doc",
  "edit docx", "fill PDF form", "create presentation", "make a spreadsheet", "pptx",
  "xlsx", "pdf", "word document", "slides", "export to PDF".
---

# Formats — Document & File Format Toolkit

Orchestrator for all document and file format tasks. Routes to the right sub-skill based on your request.

## Command Router

| Command | Sub-Skill | Trigger Phrases |
|---------|-----------|----------------|
| `/formats docx` | `docx/SKILL.md` | "create a doc", "edit word document", "tracked changes", "add comments to docx", ".docx" |
| `/formats pdf` | `pdf/SKILL.md` | "fill PDF form", "extract from PDF", "merge PDFs", "split PDF", "PDF to text", ".pdf" |
| `/formats pptx` | `pptx/SKILL.md` | "create presentation", "edit slides", "add speaker notes", "pptx", "PowerPoint" |
| `/formats xlsx` | `xlsx/SKILL.md` | "create spreadsheet", "edit Excel", "formula", "data analysis in Excel", ".xlsx", "spreadsheet" |
