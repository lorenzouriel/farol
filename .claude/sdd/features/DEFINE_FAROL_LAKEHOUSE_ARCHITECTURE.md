# DEFINE: Farol Lakehouse Architecture

> A self-hosted, fully open-source medallion lakehouse that unifies ~15 fragmented Brazilian government data sources about parlamentares/candidatos into one queryable gold layer.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | FAROL_LAKEHOUSE_ARCHITECTURE |
| **Date** | 2026-08-05 |
| **Author** | define-agent |
| **Status** | ✅ Complete (Designed) |
| **Clarity Score** | 15/15 |

---

## Problem Statement

A parlamentar or candidato's activity, spending, campaign finance, declared assets, legal history, and public-money destinations are each published by a different Brazilian government system (Câmara, Senado, TSE, Portal da Transparência, TransfereGov, RFB, TCU, DataJud) that never cross-references the others — answering "what does this person's full record look like" today requires manually joining ~15 sources by hand. Farol needs a self-hosted, 100%-open-source lakehouse (raw → bronze → silver → gold) that ingests and cross-references those sources so any such question can be answered from a single queryable gold layer.

---

## Target Users

| User | Role | Pain Point |
|------|------|------------|
| Solo maintainer (current) | Builds and operates the lakehouse alone, part-time | Needs a stack with low day-to-day operational burden — no cluster scheduler, no managed-service babysitting, since there's no ops team |
| Future open-source contributors | Will join once the project is public | Need to be able to clone the repo and stand up the entire stack locally without specialized data-platform ops knowledge |

> Downstream consumers of the gold layer (journalists, researchers, an eventual agent/MCP layer) are the project's ultimate beneficiaries but are explicitly out of scope for this phase — this DEFINE covers the lakehouse up through gold, not a consumption layer. See Out of Scope.

---

## Goals

What success looks like (prioritized):

| Priority | Goal |
|----------|------|
| **MUST** | Ingest all ~15 sources from `docs/farolv1.md` into a raw layer, with `source_url`, `extracted_at`, `source_version` captured on every record |
| **MUST** | Resolve politician identity across Câmara, Senado, and TSE (whose `SQ_CANDIDATO` changes every election) via a CPF-keyed `dim_politico` + `politico_id_externo` bridge table |
| **MUST** | Gold-layer CEAP spending aggregates apply a rolling cutoff window that accounts for the 90-day reimbursement lag, never a raw sum |
| **MUST** | Legal/sanctions data carries `status_processual` and `instancia` as first-class fields from bronze onward; gold never emits an unqualified "N processos" count |
| **MUST** | 100% open-source tooling, self-hosted on a small cluster — no managed cloud data services (Databricks, Snowflake, BigQuery) |
| **SHOULD** | Full stack (MinIO + Postgres + Airflow + DuckDB/DuckLake) reproducible via `docker-compose up` in under 15 minutes for a new contributor on a clean machine |
| **SHOULD** | Airflow daily batch DAG completes end-to-end without manual intervention for at least 7 consecutive days |
| **SHOULD** | Ingestion (dlt) handles pagination, incremental state, and schema evolution declaratively rather than per-source bespoke logic |
| **COULD** | DuckLake's Iceberg-interop bridge documented as the migration path if multi-engine access is ever needed |
| **COULD** | Benchmark criteria documented for when the RFB CNPJ join would need the Spark escape hatch (Approach C from brainstorm) |

**Priority Guide:**
- **MUST** = MVP fails without this
- **SHOULD** = Important, but workaround exists
- **COULD** = Nice-to-have, cut first if needed

---

## Success Criteria

Measurable outcomes:

- [ ] 100% of the ~15 sources in `docs/farolv1.md` land in raw with `source_url`, `extracted_at`, and `source_version` populated on every record
- [ ] `dim_politico` + `politico_id_externo` correctly cross-reference CPF across Câmara, Senado, and TSE for 100% of a validation sample (current-legislature deputados and senadores)
- [ ] 0 CEAP spending aggregates published in gold without the 90-day cutoff window applied
- [ ] 0 unqualified legal/sanctions counts in gold (all carry `status_processual` + `instancia`)
- [ ] A new contributor can bring the full stack up via `docker-compose up` in under 15 minutes on a clean machine
- [ ] The Airflow daily batch DAG completes end-to-end without manual intervention for 7 consecutive days

---

## Acceptance Tests

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| AT-001 | Entity resolution happy path | A deputado exists in both Câmara's `/deputados` and TSE's candidatos bulk with a matching CPF | The silver-layer dbt models run | `dim_politico` contains exactly one row for that person, with one `politico_id_externo` bridge row per source system |
| AT-002 | Câmara pagination edge case | The Câmara API returns `dados: []` (not a 404) for a page beyond the last page of `/proposicoes` | The dlt ingestion resource paginates through the endpoint | Ingestion terminates cleanly without treating the empty page as an error, and no partial or corrupt raw records are written |
| AT-003 | CEAP 90-day lag window | A query requests "top CEAP spenders in the last 3 months" | The gold-layer model computes CEAP totals | The result applies the rolling cutoff window rather than presenting an understated raw sum as a final ranking |
| AT-004 | Legal-status qualification | A politician has a first-instance ruling recorded in DataJud | That record is surfaced in the gold layer | `status_processual` and `instancia` are present on the record, and it is never rolled into an unqualified "N processos" aggregate |
| AT-005 | New contributor bootstrap | A contributor clones the repo on a clean machine with Docker installed | They run `docker-compose up` per the infra setup | MinIO, Postgres, and Airflow are running and a first DuckDB query against a seeded/sample table succeeds, in under 15 minutes |

---

## Out of Scope

Explicitly NOT included in this feature:

- **Spark / distributed compute** — deferred unless the RFB CNPJ join (~20GB) is benchmarked and found too slow for DuckDB's out-of-core execution (documented escape hatch: brainstorm Approach C)
- **Iceberg + REST catalog (Polaris/Gravitino)** — DuckLake's Postgres catalog is used instead; Iceberg migration remains available via DuckLake's interop bridge if needed later
- **Streaming engines (Kafka/Flink/RisingWave)** — daily batch freshness is sufficient; none of the ~15 sources are live event streams
- **Dedicated data-quality platform (Soda/Great Expectations)** — dbt tests cover the v1 quality gates (CEAP cutoff, legal-status typing)
- **Agent/MCP consumption layer** — the doc's own later phase, once gold tables exist; not part of this architecture
- **Managed cloud data services** (Databricks, Snowflake, BigQuery, cloud-native warehouses) — violates the 100%-open-source, self-hosted constraint
- **Multi-region/HA MinIO or elastic cloud compute** — a single self-hosted small cluster is the target, not cloud autoscaling
- **BI/dashboard/frontend layer** — not addressed by this phase; gold tables are the deliverable
- **RFB CNPJ vínculos graph and TSE 2026 campaign/asset ingestion as day-one scope** — per the brainstorm's inherited build sequence, identity + CEAP + legislative activity land first; emendas, campaign finance, and the CNPJ graph are later phases of the same architecture, not excluded permanently

---

## Constraints

| Type | Constraint | Impact |
|------|------------|--------|
| Technical | 100% open-source tooling; no managed cloud data services | Limits engine/tool selection to self-hostable OSS: DuckDB/DuckLake, MinIO, Postgres, Airflow, dbt, dlt |
| Technical | Self-hosted small cluster, not elastic cloud compute | Architecture must not assume autoscaling; storage/compute sizing must fit a fixed, small set of machines |
| Resource | Solo maintainer today, open-source project in the future | Favors low-ops tooling and `docker-compose`-level reproducibility over operational sophistication |
| Timeline | 2026 is a general election year; the source doc frames Sept/Oct 2026 as the window where fresh data has maximum relevance, November+ as merely historical | Biases the build sequence toward identity resolution + CEAP + legislative activity first, matching the doc's own suggested phasing, so early value ships before the campaign season passes |
| Legal / Ethical | Donor CPFs must be masked at ingestion; non-public-agent family members appearing in asset declarations or corporate records must not be exposed; DataJud homonym risk must be guarded against | Privacy-masking and identity-disambiguation logic must be built into the pipeline (bronze/silver), not left to the presentation layer |

---

## Technical Context

> Essential context for Design phase — prevents misplaced files and missed infrastructure needs.

| Aspect | Value | Notes |
|--------|-------|-------|
| **Deployment Location** | Flat, function-based top-level layout: `ingestion/` (dlt sources), `transform/` (dbt project), `orchestration/` (Airflow DAGs), `infra/` (docker-compose, MinIO/Postgres/Airflow config), `docs/` (existing) | Confirmed by user; simplest structure for a new OSS contributor to navigate |
| **KB Domains** | `lakehouse` (table formats/catalogs — DuckLake, Iceberg-interop), `medallion` (bronze/silver/gold layer design), `modern-stack` (DuckDB patterns), `airflow` (DAG design, TaskFlow), `dbt` (model types, incremental strategies, testing), `data-modeling` (dimensional modeling, SCD for `dim_politico`), `data-quality` (dbt-testing patterns for the CEAP/legal-status gates), `sql-patterns` (cross-dialect SQL for DuckDB), `python` (dlt resource code) | Design phase should pull patterns from these domains directly |
| **IaC Impact** | New resources — greenfield repo, nothing exists yet. `docker-compose` is the provisioning mechanism (no Terraform in this repo) | MinIO, Postgres, Airflow, and DuckDB compute all need service definitions in `infra/` |

**Why This Matters:**

- **Location** → Design phase uses correct project structure, prevents misplaced files
- **KB Domains** → Design phase pulls correct patterns from `.claude/kb/`
- **IaC Impact** → Triggers infrastructure planning, avoids "works locally" failures

---

## Data Contract (if applicable)

### Source Inventory

| Source | Type | Volume | Freshness | Owner |
|--------|------|--------|-----------|-------|
| Câmara `/deputados`, `/proposicoes`, `/votacoes`, `/despesas` | REST (paginated, max 100/page) | Small, incremental | Daily | External (Câmara dos Deputados) |
| Câmara CEAP bulk (`Ano-{ano}.zip`, 2008–2026) | BULK, annual files | Few GB total | Daily (upstream updates daily) | External (Câmara dos Deputados) |
| Senado (parlamentares, matérias, votações) | REST/XML | Small | Daily | External (Senado Federal) |
| TSE Dados Abertos (candidatos, bens, prestação de contas) | BULK | Moderate, per-election, 2014–2026 | Daily | External (TSE) |
| TSE DivulgaCandContas (2026) | REST/Web | Moderate, growing through campaign season | Daily (near-real-time upstream) | External (TSE) |
| Portal da Transparência (emendas, sanções, SIAPE) | REST (API key) / BULK | Moderate; web download capped at 20k rows — bulk files required | Daily | External (CGU) |
| TransfereGov Transferências Especiais | REST — PostgREST (`campo=eq.valor` filters) | Moderate | Daily | External (Gestão) |
| RFB CNPJ | BULK | ~20GB, ~60M companies | Slower cadence (periodic upstream refresh) | External (Receita Federal) |

### Schema Contract

| Column | Type | Constraints | PII? |
|--------|------|-------------|------|
| `cpf` (politician, `dim_politico`) | VARCHAR | NOT NULL, UNIQUE | No — the politician's own CPF is public data for a public figure per the source doc's responsibility note |
| `nome_civil` / `nome_eleitoral` | VARCHAR | NOT NULL | No |
| `sq_candidato` | VARCHAR | Versioned by election (changes each cycle) | No |
| `source_url` | VARCHAR | NOT NULL, on every raw/bronze/gold record | No |
| `extracted_at` | TIMESTAMP | NOT NULL, on every raw/bronze/gold record | No |
| `source_version` | VARCHAR | NOT NULL, on every raw/bronze/gold record | No |
| `status_processual` / `instancia` (legal records) | VARCHAR | NOT NULL where a legal record exists | No |
| `cpf_doador` (campaign donor CPF) | VARCHAR | Masked/hashed at ingestion, never stored or exposed in plaintext | **Yes** — masking is a MUST constraint, not a later cleanup |
| Family members appearing in asset declarations or corporate records | — | Excluded from gold unless the person is independently a public agent | **Yes** |

### Freshness SLAs

| Layer | Target | Measurement |
|-------|--------|-------------|
| Raw / Staging | Within 24 hours of the daily Airflow run | Timestamp comparison (`extracted_at` vs. run time) |
| Bronze / Silver / Gold | Refreshed by completion of the same daily Airflow DAG | DAG completion time |

### Completeness Metrics

- 100% of the ~15 sources present in raw within each daily run window, or the failure is logged and surfaced (no silent partial loads)
- Zero null `cpf` in `dim_politico`'s primary key
- Zero unqualified legal-status aggregates and zero non-cutoff-windowed CEAP aggregates in gold (see Success Criteria)

### Lineage Requirements

- `source_url` / `extracted_at` / `source_version` propagate from raw through to every gold-layer fact — non-negotiable per the source doc
- Model-level lineage via the dbt DAG (`dbt docs generate`) is sufficient for v1; column-level lineage tooling (e.g., OpenLineage) is explicitly deferred

---

## Assumptions

Assumptions that if wrong could invalidate the design:

| ID | Assumption | If Wrong, Impact | Validated? |
|----|------------|------------------|------------|
| A-001 | DuckDB can execute the ~20GB RFB CNPJ join (~60M rows) via out-of-core processing without requiring a distributed engine | Would need to fall back to the Spark escape hatch (brainstorm Approach C) for that one job | [ ] |
| A-002 | None of the ~15 sources require sub-daily freshness even during the 2026 election season | Would need intraday Airflow scheduling specifically for TSE DivulgaCandContas / IDC feeds | [ ] |
| A-003 | The available self-hosted small cluster has enough disk/network capacity for MinIO + Postgres + Airflow + raw/bronze/silver/gold Parquet without elastic scaling | Would need to revisit storage sizing or introduce cloud object storage, breaking the self-hosted constraint | [ ] |
| A-004 | DuckLake (v0.3) is stable enough for this project's needs despite being a newer table format | Would need to fall back to plain DuckDB + Parquet without catalog/time-travel, or adopt Iceberg earlier than planned | [ ] |
| A-005 | The field-level inventory in `docs/farolv1.md` is accurate enough to design ingestion schemas against, despite several endpoints flagged `⚠︎` (not revalidated) | Schema decisions for those specific sources will need rework after the first exploratory pull confirms actual field shapes | [ ] |

**Note:** Validate critical assumptions before DESIGN phase. Unvalidated assumptions become risks.

---

## Clarity Score Breakdown

| Element | Score (0-3) | Notes |
|---------|-------------|-------|
| Problem | 3 | Specific, actionable, inherited from a fully validated BRAINSTORM session — names the fragmentation problem and the concrete unifying deliverable (gold layer) |
| Users | 3 | Two personas identified with concrete pain points (solo maintainer's ops burden, future contributor's local-setup friction); downstream consumers explicitly and correctly deferred as out of this phase's scope |
| Goals | 3 | Full MoSCoW breakdown, each goal traceable to a brainstorm decision or KB-grounded rationale |
| Success | 3 | Every criterion carries a number (100%, 0, 15 minutes, 7 consecutive days) — the two previously-fuzzy targets (bootstrap time, DAG stability window) were confirmed directly with the user rather than invented |
| Scope | 3 | Explicit, extensive Out of Scope list carried over from the brainstorm's YAGNI pass, plus constraints covering legal/ethical boundaries |
| **Total** | **15/15** | |

**Scoring Guide:**
- 0 = Missing entirely
- 1 = Vague or incomplete
- 2 = Clear but missing details
- 3 = Crystal clear, actionable

**Minimum to proceed: 12/15**

---

## Open Questions

None — ready for Design.

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-05 | define-agent | Initial version, derived from BRAINSTORM_FAROL_LAKEHOUSE_ARCHITECTURE.md plus two clarifying questions (project layout, success-metric targets) |

---

## Next Step

**Ready for:** `/build .claude/sdd/features/DESIGN_FAROL_LAKEHOUSE_ARCHITECTURE.md`
