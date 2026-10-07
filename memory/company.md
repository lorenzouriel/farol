# Company

> Central business memory. Claude reads this file before each answer.
> You can edit it at any time.

**Name:** Farol
**Business:** Open-source research project. Farol means "lighthouse" in Portuguese: each study lights up part of a country without claiming to describe all of it.
**What it does:** Open studies on countries, economies, and societies, with sources, methods, and findings you can inspect and build on.
**Profile:** Solopreneur / solo creator
**Serves clients:** No clients. Funded by supporters of the open-source project through Buy Me a Coffee.
**Team:** One person, no team.
**Tools:** Git/GitHub (public repository), Buy Me a Coffee
**Main deliverables:** Studies in the public repository (`studies/` on the `main` branch), each with a bounded question, sources, methodology, and a dated report (`ANALYSIS.md` + `ANALYSIS.html`)

## Additional context

- The study is the unit of work. Each one starts from a bounded question and can cover one country or compare several.
- The project starts with files and small scripts. New tools are added only when a real study needs them.
- Two branches. `main` is the public study repository (`README.md`, `AGENTS.md`, `studies/`, `template/`). `dev` is the workshop: content, promotion, the creator's routines, data analysis, research, and studies in progress under `projects/studies/`.
- When a study is finished on dev, only its folder is copied to `studies/` on main and added to the index. Dev is never merged into main.
