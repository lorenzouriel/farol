# Working in Farol

## Purpose and scope

Farol is a repository of research about countries. The deliverable is a study with traceable evidence, explicit methods, and readable findings. Read the root README and the target study's README, source registry, methodology, and analysis before changing an existing study.

Keep changes within the requested study or repository task. Preserve unrelated work. Use existing local skills when relevant to the task; their presence does not make every workflow mandatory.

## Structure

- Start new studies by copying `template/` into `studies/<study-slug>/` or `studies/<topic>/<study-slug>/`.
- Frame each study around a bounded question and state countries, time period, inclusion criteria, and exclusions.
- Keep study-specific code, dependencies, data, and documentation together. Remove unused template sections and folders.
- Maintain `studies/README.md` when studies are added or their scope or status changes.
- Introduce shared tools only after concrete reuse warrants them. Do not add a backend, database, scheduler, or frontend framework unless the task requires it.

## Evidence and analytical integrity

- Never invent sources, citations, observations, or results. Label placeholders and unverified claims.
- Prefer primary evidence. Read the relevant source before citing it; record its URL, publisher, publication date when known, retrieval date, coverage, and limitations in `sources/sources.yaml`.
- Use stable source IDs and direct links in reports. Cite specific pages, tables, or series when available.
- Distinguish source publication, retrieval, and observation dates. Verify time-sensitive claims when refreshing a study.
- Separate observed facts, estimates, assumptions, and interpretation. Explain disagreements between sources and avoid unsupported causal claims.
- Document units, currencies, price years, denominators, definitions, and cross-country comparability where relevant.
- Treat missing values as missing, not zero. Explain exclusions, imputation, sampling bias, and uncertainty.
- AI-generated prose and summaries are not independent evidence. Trace their claims back to inspected sources.

## Data and reproducibility

- Keep original inputs separate from derived outputs. Document provenance and transformations; do not silently overwrite source snapshots.
- Store only material that can be redistributed. For restricted or large inputs, record retrieval instructions and access limitations instead. Never commit credentials or private personal data.
- Document actual commands, working directory, runtime versions, dependencies, and input/output paths in the study README when code is used.
- Prefer small scripts with explicit inputs and outputs. Record seeds when randomness affects results.
- Check calculations and relevant data assumptions, such as units, missingness, duplicate keys, totals, and joins. Add tests where they protect substantive analytical logic; do not introduce a test framework for prose-only changes.

## Reports and updates

- Use `ANALYSIS.md` as the editable findings and `ANALYSIS.html` as the corresponding readable snapshot. Document the study's generation or manual synchronization procedure.
- Reports must state status, period covered, last verification date, methods, citations, and limitations. Inconclusive findings are acceptable.
- Prefer HTML that opens locally without a service. Keep assets local when feasible and avoid hidden live data dependencies.
- Never present a template or unverified draft as completed research. Use `planned`, `in-progress`, or `reviewed`; mark a study reviewed only after evidence, calculations, and report checks are actually complete.
- On refresh, record what evidence changed and whether conclusions changed in the study README. Update both report formats and the verification date only to reflect checks actually performed.
- Before finishing, check links and consistency between evidence, calculations, and prose. When changing report presentation, inspect the HTML in a browser if available and report any unperformed checks.
- Summarize changes, validation performed, and remaining evidence gaps. Do not claim to have run commands or reviewed sources that you did not inspect.
