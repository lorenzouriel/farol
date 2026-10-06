# Farol

Farol is an open research repository for understanding countries through reproducible studies of their economies, institutions, industries, and societies.

Each study brings together a question, sources, methods, and findings that people and AI can inspect, challenge, reproduce, and extend. The name means **lighthouse** in Portuguese: a study illuminates part of a country without claiming to describe everything about it.

## The study is the unit of work

Start with a bounded question. A topic such as `porn-industry` can contain a study asking, “What can available evidence tell us about the industry's economic footprint in Brazil?” A study can cover one country or compare several.

Farol supports live research with AI: discovering sources, investigating discrepancies, running calculations, comparing countries, and revising conclusions. Findings are published as dated reports that remain readable without a running agent or service.

The repository starts with files and small scripts. Add tools only when an actual study needs them; there is no required application stack, database, orchestration service, or dashboard.

## Repository structure

```text
farol/
├── README.md
├── AGENTS.md
├── studies/
│   └── README.md                 # Index of actual studies
└── template/                     # Copy to start a study
    ├── README.md                 # Question, scope, status, reproduction
    ├── sources/
    │   └── sources.yaml          # References and provenance
    ├── data/
    │   └── README.md             # Input and derived data conventions
    ├── scripts/
    │   └── README.md             # Collection, analysis, report commands
    ├── docs/
    │   └── methodology.md        # Definitions, assumptions, limitations
    ├── ANALYSIS.md               # Editable findings and citations
    └── ANALYSIS.html             # Readable report snapshot
```

Use `studies/<study-slug>/` for a standalone study. When several studies share a topic, group them under `studies/<topic>/<study-slug>/`, for example `studies/porn-industry/brazil-economic-footprint/`. Use lowercase names separated by hyphens. Record countries in each study and the index; add country indexes when useful.

The structure is flexible. Qualitative studies may not need `data/` or `scripts/`. Keep only what the question requires.

## Start a study

1. Copy `template/` into a new directory under `studies/`.
2. Fill in its README: question, countries, period, scope, and status. Remove unused template sections and folders.
3. Record sources in `sources/sources.yaml`, including retrieval dates and coverage.
4. Document definitions and methods, then collect evidence and perform the analysis.
5. Write findings in `ANALYSIS.md`, linking claims to evidence and calculations.
6. Update `ANALYSIS.html` from the reviewed findings. Record the rendering method or manual update procedure in the study README.
7. Verify the report and add the study to the [study index](studies/README.md).

The template contains placeholders, not research results. No shared report generator or runtime is required. Each study documents its own dependencies and commands when needed.

## Research principles

- Support important factual claims with traceable evidence; prefer primary sources.
- Make quantitative findings traceable to inputs, transformations, and calculations.
- Distinguish observations, estimates, and interpretations. Explain uncertainty and conflicting evidence.
- State the period covered and the last verification date. A recent retrieval does not make old data current.
- Treat missing evidence and inconclusive results as valid outcomes.
- Store source material only when redistribution is permitted. Reference large or restricted datasets and document how to obtain them.

## Working with AI

Read [AGENTS.md](AGENTS.md) for the repository's research and editing conventions. A useful task might be:

> Refresh this study's sources, investigate the discrepancy between the two estimates, and show whether the conclusion changes.

An update should leave reviewable changes to sources, methods, calculations, and findings. AI output is a research aid, not evidence in itself. Keep Markdown and HTML consistent and explain material revisions in the study's change history.
