# BRAINSTORM: Farol Lakehouse Architecture

> Exploratory session to clarify intent and approach before requirements capture

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | FAROL_LAKEHOUSE_ARCHITECTURE |
| **Date** | 2026-08-05 |
| **Author** | brainstorm-agent |
| **Status** | ✅ Complete (Defined) |

---

## Initial Idea

**Raw Input:** Source document `docs/farolv1.md` — a scoping doc for Farol, a project that answers any question about a Brazilian parlamentar/candidato (proposals, votes, spending, campaign funding, declared assets, legal history, public-money destinations) by unifying ~15 government data sources (Câmara, Senado, TSE, Portal da Transparência, TransfereGov, RFB, TCU, DataJud, etc.) that currently don't cross-reference each other. User follow-up: "Let's think about the architecture first, needs to be all Open Source tools. I'm planning in a Data Lakehouse (raw, bronze, silver, gold)."

**Context Gathered:**
- No existing code in the repo yet — this is a greenfield project (`docs/` currently holds only `catalog.md` and `farolv1.md`).
- `docs/farolv1.md` already contains a strong, source-verified inventory of APIs/bulk files per domain (identity, legislative activity, mandate spending, emendas, campaign finance, legal/sanctions, corporate ties) plus known data traps (CEAP 90-day lag, `dados: []` pagination on Câmara API, DataJud homonym risk, CNPJ bulk ~20GB, 20k-row web-download cap on Portal da Transparência).
- The doc's own suggested build sequence (dim_politico + ID bridge → CEAP → proposições/votações → emendas → TSE campaign/assets → RFB CNPJ graph → agent/MCP layer) maps cleanly onto medallion layering and was used to sequence the YAGNI cuts below.
- Repo's KB (`.claude/kb/_index.yaml`) has direct domain coverage for this decision: `lakehouse` (table formats/catalogs), `medallion` (bronze/silver/gold), `modern-stack` (DuckDB/Polars/SQLMesh), `airflow`, `dbt`, `data-modeling`, `data-quality`, `sql-patterns`, `python`.

**Technical Context Observed (for Define):**

| Aspect | Observation | Implication |
|--------|-------------|-------------|
| Likely Location | New repo, no `src/` yet | Greenfield — Define/Design will need to establish project structure from scratch |
| Relevant KB Domains | `lakehouse`, `medallion`, `modern-stack`, `airflow`, `dbt`, `data-modeling`, `data-quality`, `sql-patterns`, `python` | These ground the Design phase's code patterns |
| IaC Patterns | None yet (no `terraform/` or deploy tooling) | Self-hosted small cluster deployment (MinIO, Postgres, Airflow) will need provisioning decided in Design |

---

## Discovery Questions & Answers

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Where will this lakehouse run day-to-day? | Self-hosted small cluster (a handful of machines you control, not elastic cloud) | Rules out managed cloud services (Databricks/Snowflake/BigQuery); favors tools that don't require a compute cluster to be useful (DuckDB-class engines run fine on one node within the cluster) |
| 2 | Who's building and running this? | Solo now, open source project in the future | Prioritizes low day-to-day ops overhead now, and a stack a future contributor can `docker-compose up` easily — ruled out anything requiring specialized ops knowledge to bootstrap |
| 3 | How fresh does ingested data need to be? | Daily batch (confirmed as sufficient for v1 even during election season) | Eliminates streaming engines (Kafka/Flink/RisingWave) entirely — none of the ~15 sources are live event streams anyway |
| 4 | What pulls the ~15 heterogeneous sources (paginated REST, PostgREST, bulk ZIP/CSV) into raw? | dlt (data load tool) — open source, Python-native | Fixes the ingestion layer: declarative pagination/incremental-state/schema-evolution handling instead of ~15 bespoke scripts or a heavyweight connector platform (Airbyte) |
| 5 | Any sample data available yet (API responses, bulk files, ground truth)? | Nothing yet, starting fresh | Design/Build must budget an exploratory first pull per source before schema decisions are finalized; no shortcuts from existing fixtures |

**Minimum Questions:** 3 (5 asked)

---

## Sample Data Inventory

| Type | Location | Count | Notes |
|------|----------|-------|-------|
| Input files | N/A | 0 | No sample pulls exist yet — first build task per source is an exploratory API/bulk-file pull to ground the raw-layer schema |
| Output examples | N/A | 0 | Gold-layer schema (e.g. `dim_politico` shape) will be drafted in Design, validated against real pulls in Build |
| Ground truth | N/A | 0 | None available; `docs/farolv1.md` itself functions as the closest thing to ground truth (a source-verified inventory of fields per API) |
| Related code | N/A | 0 | Greenfield repo — no existing ingestion or transform code to reuse |

**How samples will be used:**

- Once pulled, exploratory samples from each of the ~15 sources will ground dlt resource schemas (pagination shape, field types, nullability)
- The doc's noted quirks (Câmara's `dados: []` on out-of-range pages, CEAP's own file layout/dictionary, TSE's per-election `SQ_CANDIDATO`) should be re-verified against a live pull before being encoded as ingestion logic, since the doc itself flags several endpoints as `⚠︎ não revalidado`

---

## Approaches Explored

### Approach A: DuckDB/DuckLake lean stack ⭐ Recommended

**Description:** MinIO (self-hosted, S3-compatible) for object storage; DuckLake (Postgres metadata catalog + Parquet files in MinIO, snapshot-based time travel) as the table format; dlt for ingestion into raw; dbt for bronze → silver → gold transforms; Airflow for daily batch orchestration. All compute runs as single-process DuckDB — the small cluster hosts MinIO, Postgres, and Airflow, not a distributed compute grid.

**Pros:**
- Directly matches KB guidance: *"Single-node analytics (<500GB): DuckLake 0.3 or DuckDB + Parquet"* — total data volume here (largest single dataset ~20GB RFB CNPJ bulk, everything else single-digit GB) sits well inside that envelope
- Low enough operational surface for a solo maintainer today, and realistic for a future open-source contributor to stand up locally (`docker-compose up`, no REST catalog service, no cluster scheduler)
- DuckLake's snapshot time-travel satisfies the doc's own non-negotiable requirement — every claim shown must carry `source_url`, `extracted_at`, `source_version`

**Cons:**
- DuckLake is a newer format (0.3) — smaller ecosystem and fewer battle scars than Iceberg
- The RFB CNPJ join (~20GB, ~60M companies) needs to be written for out-of-core execution rather than assuming it fits in memory; unproven until benchmarked

**Why Recommended:** Confidence 0.85 (KB pattern match — `.claude/kb/lakehouse/quick-reference.md` "When to Use What" table — no codebase precedent since this is greenfield). Matches confirmed constraints exactly: modest data volume, daily batch freshness, solo-now/OSS-later maintenance model. Chosen approach carries an explicit escape hatch (Approach C) if the one heavy join doesn't hold up.

---

### Approach B: Iceberg + Trino/Spark, standard distributed lakehouse

**Description:** Iceberg v3 tables with a REST catalog (Apache Polaris or Gravitino), Trino or Spark for compute across the small cluster, dbt for transforms, Airflow for orchestration.

**Pros:**
- The "textbook" 2026 open-source greenfield lakehouse per KB (`lakehouse/quick-reference.md`: *"Greenfield lakehouse → Iceberg v3 + Polaris or Gravitino"*)
- Broadest engine compatibility (Spark, Flink, Trino, DuckDB, Snowflake all read Iceberg) and higher portfolio/resume value

**Cons:**
- Real operational weight for a solo maintainer: a REST catalog service plus Trino or Spark on top of everything Approach A already needs
- Solves for a scale the confirmed data volumes don't require yet

**Why not recommended:** Violates YAGNI against the confirmed constraints (modest volume, daily batch, solo ops) — this is scale-driven architecture for a project that isn't at that scale.

---

### Approach C: Hybrid — DuckLake by default, Spark only for the CNPJ graph join

**Description:** Identical to Approach A for ingestion and all transforms, except the section-7 differentiator (`político → sócio → CNPJ → contrato público`, the ~20GB RFB join) runs as a dedicated Spark job writing back into the same Parquet layer.

**Pros:**
- Keeps day-to-day operations lean while giving the one genuinely heavy join a distributed engine instead of hoping DuckDB's out-of-core mode holds up

**Cons:**
- Two compute paradigms to maintain instead of one — premature until Approach A is actually tested and found wanting on that specific join

**Why not recommended (yet):** Held in reserve, not built. Revisit only if Approach A's CNPJ join is benchmarked and proves too slow or memory-hungry in practice.

---

## Data Engineering Context (if applicable)

### Source Systems

| Source | Type | Volume Estimate | Current Freshness |
|--------|------|-----------------|-------------------|
| Câmara `/deputados`, `/proposicoes`, `/votacoes` etc. | REST (paginated, max 100/page) | Small, incremental | Daily |
| Câmara CEAP bulk (`Ano-{ano}.zip`) | BULK, annual files since 2008 | Few GB total | Updated daily upstream, pulled daily |
| Senado (parlamentares, matérias, votações) | REST/XML | Small | Daily |
| TSE Dados Abertos (candidatos, bens, prestação de contas) | BULK | Moderate, per-election | Daily during 2026 election window |
| TSE DivulgaCandContas (2026) | REST/Web | Moderate, growing through campaign season | Near-real-time upstream; pulled daily |
| Portal da Transparência (emendas, sanções, SIAPE) | REST (API key) / BULK | Moderate; web download capped at 20k rows — bulk files must be used | Daily |
| TransfereGov Transferências Especiais | REST — PostgREST (`campo=eq.valor` filters) | Moderate | Daily |
| RFB CNPJ | BULK | ~20GB, ~60M companies | Static/periodic upstream; pulled on a slower cadence |

### Data Flow Sketch

```text
[Câmara/Senado REST] ─┐
[TSE/CEAP/RFB Bulk]  ─┼─▶ [dlt ingestion] ─▶ [Raw: MinIO/Parquet
[TransfereGov PostgREST] ┘                     + source_url/extracted_at/source_version]
                                                        │
                                                        ▼
                                        [dbt: Bronze — typed, deduplicated per source]
                                                        │
                                                        ▼
                                [dbt: Silver — entity resolution: dim_politico (CPF-keyed)
                                 + politico_id_externo bridge table]
                                                        │
                                                        ▼
                          [dbt: Gold — query-ready tables, quality-gated aggregates
                           (CEAP cutoff window, status_processual/instancia typed)]
                                                        │
                                                        ▼
                                    [Future phase: Agent/MCP consumption layer]

Orchestration: Airflow, daily batch, running alongside MinIO + Postgres on the
self-hosted small cluster. DuckDB is the compute engine at every transform stage.
```

### Key Data Questions Explored

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | What's the expected data volume? | Largest single dataset ~20GB (RFB CNPJ); rest single-digit GB or small paginated pulls | Confirms <500GB envelope → DuckDB/DuckLake is the right-sized engine per KB guidance |
| 2 | What freshness SLA is needed? | Daily batch, even during election season | Eliminates streaming engines; Airflow daily DAGs are sufficient |
| 3 | Who consumes the output? | Not yet defined (deferred to `/define`) — doc frames it as eventually an agent/MCP layer over gold tables | Gold layer must be query-ready and stable, but the consumption layer itself is explicitly out of this brainstorm's scope |

---

## Selected Approach

| Attribute | Value |
|-----------|-------|
| **Chosen** | Approach A — DuckDB/DuckLake lean stack |
| **User Confirmation** | 2026-08-05, confirmed explicitly after all three approaches were presented |
| **Reasoning** | Matches confirmed constraints (modest data volume, daily batch freshness, solo-now/OSS-later maintenance) and KB sizing guidance exactly; carries an explicit, documented escape hatch (Approach C) if the CNPJ join doesn't hold up under DuckDB |

---

## Key Decisions Made

| # | Decision | Rationale | Alternative Rejected |
|---|----------|-----------|----------------------|
| 1 | DuckLake (Postgres catalog + Parquet on MinIO) over Iceberg + REST catalog | KB: <500GB → DuckLake/DuckDB; simpler ops for a solo maintainer and future OSS contributor | Iceberg v3 + Polaris/Gravitino (Approach B) |
| 2 | dlt for ingestion across all ~15 heterogeneous sources | Declarative pagination/incremental-state/schema-evolution handling vs. ~15 bespoke scripts or a heavyweight connector platform | Airbyte (too heavy to self-host solo); custom Python scripts (too much boilerplate per source) |
| 3 | Airflow for daily batch orchestration | Matches confirmed daily-batch freshness; no streaming requirement anywhere in the source list | Kafka/Flink/RisingWave (no live event streams exist among the sources) |
| 4 | `source_url` / `extracted_at` / `source_version` captured at the dlt/raw layer, not bolted on later | Doc treats provenance as non-negotiable ("um número sem procedência é indistinguível de desinformação") | Adding provenance only at the presentation layer |
| 5 | `status_processual` / `instancia` typed as first-class columns starting in bronze | Doc's own warning: a first-instance ruling isn't a conviction, a homonym isn't the same person — this must be a dbt contract, not a UI fix | Leaving legal-status nuance to be handled ad hoc at query time |
| 6 | Gold-layer spending aggregates require an explicit rolling cutoff window | CEAP's 90-day reimbursement lag means a raw SUM silently understates the last ~3 months | Publishing an unqualified "who spent most" ranking |

---

## Features Removed (YAGNI)

| Feature Suggested | Reason Removed | Can Add Later? |
|-------------------|----------------|----------------|
| Spark / distributed compute | Untested assumption that DuckDB can't handle the ~20GB RFB CNPJ join; no evidence yet that it's needed | Yes — Approach C is the documented path back in if benchmarks show DuckDB struggling |
| Iceberg + REST catalog (Polaris/Gravitino) | More ops than a solo maintainer needs; DuckLake's Postgres catalog is simpler and has an Iceberg-interop bridge already | Yes — DuckLake → Iceberg migration path exists if multi-engine access becomes necessary |
| Streaming engine (Kafka/Flink/RisingWave) | Confirmed daily batch is sufficient; no source in the doc is a live event stream | Yes, but no signal it will ever be needed given the source list |
| Dedicated data-quality platform (Soda/Great Expectations) | dbt tests cover the two confirmed v1 quality gates (CEAP cutoff, legal-status typing); a standalone DQ platform is more infra than justified yet | Yes, if quality-gate complexity grows beyond what dbt tests express well |
| Agent/MCP consumption layer | Explicitly the doc's own later phase (step 7 of its suggested sequence) — this brainstorm scoped the lakehouse only, up through gold | Yes — natural next phase once gold tables exist |

---

## Incremental Validations

| Section | Presented | User Feedback | Adjusted? |
|---------|-----------|---------------|-----------|
| End-to-end layering (MinIO/DuckLake/dlt/dbt/Airflow, raw provenance capture) | ✅ | "Yes!" — confirmed as presented | No |
| Quality-gate placement (CEAP cutoff in gold, legal-status typing from bronze) + full YAGNI cut list | ✅ | "All good" — confirmed as presented | No |

**Minimum Validations:** 2 (2 completed)

---

## Suggested Requirements for /define

Based on this brainstorm session, the following should be captured in the DEFINE phase:

### Problem Statement (Draft)
Build a self-hosted, fully open-source data lakehouse (raw → bronze → silver → gold) that ingests and cross-references ~15 fragmented Brazilian government data sources about parlamentares/candidatos, so that questions spanning mandate activity, spending, emendas, campaign finance, legal history, and corporate ties can be answered from one queryable gold layer.

### Target Users (Draft)
| User | Pain Point |
|------|------------|
| Solo maintainer (now) | Needs a stack operable alone, with low day-to-day ops burden |
| Future open-source contributors | Need to be able to stand up the full stack locally without specialized ops knowledge |
| Eventual downstream consumers (journalists, researchers, agent/MCP layer — out of this phase's scope) | Need a stable, query-ready gold layer with provenance on every fact |

### Success Criteria (Draft)
- [ ] All ~15 sources from `docs/farolv1.md` land in raw with `source_url`, `extracted_at`, `source_version` captured per record
- [ ] `dim_politico` (CPF-keyed) + `politico_id_externo` bridge table correctly resolve identity across Câmara, Senado, and TSE (which changes `SQ_CANDIDATO` every election)
- [ ] Gold-layer spending aggregates apply the CEAP 90-day cutoff window rather than a raw sum
- [ ] Legal/sanctions data never surfaces an unqualified count without `status_processual`/`instancia`
- [ ] Full stack (MinIO + Postgres + Airflow + DuckDB) is reproducible via `docker-compose up` for a new contributor
- [ ] Daily Airflow batch runs end-to-end without manual intervention

### Constraints Identified
- 100% open-source tooling — no managed cloud data services (Databricks, Snowflake, BigQuery)
- Self-hosted small cluster, not elastic cloud compute
- Solo maintainer today; must remain approachable for future open-source contributors
- Daily batch freshness only (no streaming requirement)
- Sensitive-data handling per the doc's own responsibility section: mask donor CPFs, exclude non-public-agent family members, guard against DataJud homonyms

### Out of Scope (Confirmed)
- Spark / distributed compute (deferred — Approach C escape hatch if the RFB CNPJ join needs it)
- Iceberg + REST catalog (deferred — DuckLake's Iceberg-interop bridge is the migration path if needed)
- Streaming engines (Kafka/Flink/RisingWave)
- Dedicated data-quality platform (Soda/Great Expectations) — dbt tests suffice for v1 gates
- Agent/MCP consumption layer (next phase, once gold tables exist)

---

## Session Summary

| Metric | Value |
|--------|-------|
| Questions Asked | 5 |
| Approaches Explored | 3 |
| Features Removed (YAGNI) | 5 |
| Validations Completed | 2 |
| Duration | Single session, 2026-08-05 |

---

## Next Step

**Ready for:** `/define .claude/sdd/features/BRAINSTORM_FAROL_LAKEHOUSE_ARCHITECTURE.md`
