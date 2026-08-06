# DESIGN: Farol Lakehouse Architecture

> Technical design for a self-hosted, open-source medallion lakehouse (MinIO + DuckLake + dlt + dbt + Airflow) that unifies Câmara, Senado, TSE, CEAP, and DataJud data for the Farol project's first buildable vertical slice.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | FAROL_LAKEHOUSE_ARCHITECTURE |
| **Date** | 2026-08-05 |
| **Author** | design-agent |
| **DEFINE** | [DEFINE_FAROL_LAKEHOUSE_ARCHITECTURE.md](./DEFINE_FAROL_LAKEHOUSE_ARCHITECTURE.md) |
| **Status** | ✅ Complete (Built) |

---

## Architecture Overview

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                     FAROL LAKEHOUSE — SYSTEM OVERVIEW                     │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  [Câmara REST] [Senado REST/XML] [TSE Bulk] [CEAP Bulk] [DataJud REST]  │
│        │              │              │           │            │         │
│        └──────────────┴──────┬───────┴───────────┴────────────┘         │
│                               ▼                                          │
│              [dlt ingestion — one Airflow task per source]              │
│         stamps source_url / extracted_at / source_version on every row  │
│                               │                                          │
│                               ▼                                          │
│              [Raw: MinIO — Parquet, source-shaped, per source]          │
│                               │                                          │
│                               ▼   dbt build (DuckDB + ducklake extension)│
│           [Bronze: DuckLake tables — typed, deduplicated per source]    │
│                               │                                          │
│                               ▼   dbt                                    │
│      [Silver: dim_politico (CPF-keyed) + politico_id_externo bridge]    │
│                               │                                          │
│                               ▼   dbt, quality-gated (halt_on_failure)   │
│        [Gold: fact_ceap_gastos (90-day cutoff), fact_processos_legais   │
│                (status_processual/instancia always present)]            │
│                               │                                          │
│                               ▼                                          │
│              (future phase — out of scope: agent/MCP layer)             │
│                                                                           │
│  Catalog: Postgres (DuckLake metadata)     Orchestration: Airflow daily  │
└───────────────────────────────────────────────────────────────────────────┘
```

This design covers the vertical slice implied by the DEFINE's MUST goals and constraints: identity resolution across **Câmara, Senado, and TSE** (required by the DEFINE's success criteria), **CEAP** spending (the 90-day cutoff MUST goal), and **DataJud** legal records (the status-qualification MUST goal). RFB CNPJ, TransfereGov/emendas, DivulgaCandContas, and Portal da Transparência sanções are explicitly deferred per the DEFINE's Out of Scope — this architecture is built so they slot in as additional `ingestion/sources/*.py` modules without structural change.

---

## Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| MinIO | Self-hosted, S3-compatible object storage for raw Parquet and DuckLake data files | MinIO (Docker container) |
| Postgres | DuckLake metadata catalog + Airflow metadata DB (two databases, one instance) | PostgreSQL 16 (Docker container) |
| dlt ingestion | Pulls Câmara, Senado, TSE, CEAP, and DataJud into raw Parquet on MinIO, stamping provenance on every record | Python, `dlt` (`filesystem` destination) |
| DuckDB + DuckLake | Query/transform engine; the `ducklake` extension attaches the Postgres catalog over MinIO Parquet, giving ACID + snapshot time travel | DuckDB 1.2+, `ducklake` extension 0.3 |
| dbt | Bronze → Silver → Gold transforms; dbt tests enforce the CEAP-cutoff and legal-status quality gates | dbt Core + `dbt-duckdb` adapter |
| Airflow | Daily batch orchestration: one dynamically-mapped task per ingestion source, then `dbt build` | Apache Airflow 3.0, standalone mode / LocalExecutor |

---

## Key Decisions

### Decision 1: DuckLake (Postgres catalog) over Iceberg + REST catalog

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-08-05 |

**Context:** The lakehouse needs an open table format with ACID transactions and time travel (to satisfy the DEFINE's non-negotiable provenance requirement), self-hostable on a small cluster by a solo maintainer, sized for data volumes that top out around ~20GB (RFB CNPJ, deferred) with everything else in single-digit GB.

**Choice:** DuckLake 0.3, with Postgres as the metadata backend and Parquet files on MinIO as the data layer, queried via DuckDB.

**Rationale:** KB guidance (`lakehouse/quick-reference.md`) is explicit: *"Single-node analytics (<500GB): DuckLake 0.3 or DuckDB + Parquet"* and *"Dev/CI/CD testing: DuckLake (zero infra, fast, Iceberg interop)"*. DuckLake gives snapshot-based time travel and multi-table ACID transactions with one extra Postgres container — no separate REST catalog service to run.

**Alternatives Rejected:**
1. Iceberg v3 + Apache Polaris/Gravitino — rejected because it adds a REST catalog service plus Spark/Trino compute, more operational surface than a solo maintainer needs at this data volume (per brainstorm Approach B).
2. Delta Lake — rejected because its tooling is Spark-native; DuckDB's Delta read support is present but DuckLake's DuckDB-first design and Postgres-catalog simplicity fit the constraint better.

**Consequences:**
- DuckLake is a newer format (0.3, Sep 2025) with a smaller ecosystem than Iceberg — accepted risk, tracked as DEFINE assumption A-004.
- An Iceberg-interop bridge (`COPY FROM DATABASE ducklake_catalog TO iceberg_catalog`) remains available if multi-engine (Spark/Trino) access is ever needed — no rewrite required, just a metadata-level copy.

---

### Decision 2: dlt (data load tool) as the sole ingestion framework

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-08-05 |

**Context:** Five heterogeneous source shapes need to land in raw: paginated REST (Câmara, Senado), bulk file downloads (TSE, CEAP), and a rate-limited REST API (DataJud) — each with its own pagination, retry, and schema-drift behavior.

**Choice:** Every source is a `dlt.source` with one `dlt.resource` per logical entity, writing Parquet to MinIO via dlt's `filesystem` destination.

**Rationale:** dlt handles pagination state, retries, and schema evolution declaratively, which scales across ~15 eventual sources far better than bespoke per-source scripts. It's a single Python dependency with no extra service to run, which matters for the `docker-compose up`-in-15-minutes success criterion.

**Alternatives Rejected:**
1. Airbyte (self-hosted) — rejected: its own database, scheduler, and UI is heavier ops than a solo maintainer needs, and almost none of these Brazilian gov sources have existing connectors so most would be custom anyway.
2. Custom `requests` + `pyarrow` scripts — rejected: re-implements pagination, retry, and schema-drift handling per source, ~15 times over.

**Consequences:**
- dlt's `filesystem` destination lands source-shaped Parquet in raw; DuckLake tables aren't created until dbt's bronze layer reads that Parquet — this keeps dlt simple (no DuckLake-specific destination adapter needed, since dlt has no native DuckLake integration yet) and keeps raw genuinely raw.
- Provenance stamping (`source_url`, `extracted_at`, `source_version`) happens inside dlt resources, not as a later cleanup step — see `ingestion/common/provenance.py` in the File Manifest.

---

### Decision 3: CPF-keyed `dim_politico` + explicit `politico_id_externo` bridge table

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-08-05 |

**Context:** The same politician appears as Câmara's numeric `id`, Senado's `CodigoParlamentar`, and TSE's `SQ_CANDIDATO` (which changes every election cycle). The DEFINE's success criteria require 100% correct cross-referencing across all three systems.

**Choice:** `dim_politico` uses `cpf` as the stable natural key (surfaced via a generated `politico_sk` surrogate key per the KB's star-schema pattern), with a separate `politico_id_externo` bridge table (`fonte`, `id_externo`, `cpf`, `valid_from`, `valid_to`) rather than one "smart" unified ID.

**Rationale:** CPF is the only key stable across all three source systems (per `docs/farolv1.md` section 1). The DEFINE and brainstorm both explicitly rejected inventing a clever unified ID — the bridge table keeps every source-to-CPF mapping explicit, auditable, and correctable when a match turns out wrong (which the source doc warns will happen).

**Alternatives Rejected:**
1. A single synthetic cross-system ID computed from fuzzy name matching — rejected: unauditable, and the source doc explicitly warns against this exact shortcut.
2. Storing external IDs as columns directly on `dim_politico` (one column per source) — rejected: doesn't scale as more sources are added (RFB CNPJ, Portal da Transparência), and loses the `valid_from`/`valid_to` versioning TSE's `SQ_CANDIDATO` needs.

**Consequences:**
- Every new source added later (RFB, TransfereGov, etc.) plugs into the same bridge table pattern instead of requiring a `dim_politico` schema change.
- Entity-resolution bugs are correctable by fixing bridge rows, not by re-deriving `dim_politico` from scratch.

---

### Decision 4: Airflow 3.0 with dynamic task mapping, one task per source

| Attribute | Value |
|-----------|-------|
| **Status** | Accepted |
| **Date** | 2026-08-05 |

**Context:** Daily batch freshness is confirmed sufficient (DEFINE discovery Q3); the DAG needs to run five independent ingestion sources followed by a single `dbt build`.

**Choice:** One Airflow DAG (`farol_daily_batch`), using TaskFlow's `.expand()` to dynamically map one `run_source` task per entry in `SOURCES`, followed by a single `dbt_build` task.

**Rationale:** KB airflow pitfalls are explicit: *"Monolithic tasks (ETL in one) → One task per logical step"*. Dynamic mapping means a new source is added by appending to a list, not writing a new task; a single source's failure (e.g., DataJud rate-limiting) doesn't block the other four from loading.

**Alternatives Rejected:**
1. One monolithic `run_all_sources` task — rejected per the KB pitfall above; a single slow/failing source would block or delay everything.
2. Dagster — rejected in the brainstorm phase already (not revisited here): Airflow's larger community and this repo's existing `airflow-specialist` agent tooling make it the lower-friction choice for a solo maintainer.

**Consequences:**
- Failed sources retry independently (`retries=2, retry_delay=5min` per KB pitfall guidance) without re-running sources that already succeeded that day.
- `dbt_build` only runs after all five ingestion tasks complete — a slow bulk download (TSE, CEAP) sets the floor for when transforms start.

---

## File Manifest

| # | File | Action | Purpose | Agent | Dependencies |
|---|------|--------|---------|-------|---------------|
| 1 | `infra/docker-compose.yml` | Create | MinIO + Postgres + Airflow (standalone) service definitions | (general) | None |
| 2 | `infra/.env.example` | Create | Documents required secrets/env vars (MinIO keys, Postgres creds, DataJud API key) | (general) | None |
| 3 | `infra/postgres/init-catalogs.sql` | Create | Creates the `ducklake_catalog` and `airflow` databases on first container start | (general) | 1 |
| 4 | `infra/minio/init-buckets.sh` | Create | Creates the private `farol-raw` bucket on first container start | (general) | 1 |
| 5 | `infra/README.md` | Create | Bootstrap instructions targeting the confirmed 15-minute `docker-compose up` success criterion | (general) | 1, 2, 3, 4 |
| 6 | `ingestion/common/provenance.py` | Create | `source_url`/`extracted_at`/`source_version` stamping shared by every source | @python-developer | None |
| 7 | `ingestion/common/privacy.py` | Create | CPF-masking transformer interface, ready for future donor-CPF sources (TSE prestação de contas, Portal da Transparência) | @python-developer | None |
| 8 | `ingestion/sources/camara.py` | Create | dlt source: `deputados` + `proposicoes`; handles the `dados: []` pagination trap | @python-developer | 6 |
| 9 | `ingestion/sources/senado.py` | Create | dlt source: `parlamentares` | @python-developer | 6 |
| 10 | `ingestion/sources/tse_bulk.py` | Create | dlt source: `candidatos` bulk files (2014–2026) | @python-developer | 6 |
| 11 | `ingestion/sources/ceap.py` | Create | dlt source: CEAP annual bulk files | @python-developer | 6 |
| 12 | `ingestion/sources/datajud.py` | Create | dlt source: `processos`, capturing `status_processual`/`instancia` at the source | @python-developer | 6 |
| 13 | `ingestion/pipeline.py` | Create | Wires all five sources to the `filesystem` (MinIO) destination | @lakehouse-architect | 8, 9, 10, 11, 12 |
| 14 | `ingestion/config.yaml` | Create | Per-source base URLs, page sizes, bulk-file years | (general) | None |
| 15 | `transform/dbt_project.yml` | Create | dbt project configuration | @dbt-specialist | None |
| 16 | `transform/profiles.yml` (example) | Create | `dbt-duckdb` adapter: attaches the DuckLake Postgres catalog and MinIO S3 settings | @lakehouse-architect | None |
| 17 | `transform/models/bronze/camara/stg_camara__deputados.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 18 | `transform/models/bronze/camara/stg_camara__proposicoes.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 19 | `transform/models/bronze/senado/stg_senado__parlamentares.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 20 | `transform/models/bronze/tse/stg_tse__candidatos.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 21 | `transform/models/bronze/ceap/stg_ceap__despesas.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 22 | `transform/models/bronze/datajud/stg_datajud__processos.sql` | Create | Typed, deduplicated bronze model | @dbt-specialist | 13 |
| 23 | `transform/models/silver/dim_politico.sql` | Create | CPF-keyed identity dimension | @schema-designer | 17, 19, 20 |
| 24 | `transform/models/silver/politico_id_externo.sql` | Create | Bridge table: `fonte`, `id_externo`, `cpf`, `valid_from`, `valid_to` | @schema-designer | 17, 19, 20 |
| 25 | `transform/models/gold/fact_ceap_gastos.sql` | Create | CEAP spending aggregate, 90-day cutoff window applied | @dbt-specialist | 21, 23 |
| 26 | `transform/models/gold/fact_processos_legais.sql` | Create | Legal facts; always carries `status_processual`/`instancia` | @dbt-specialist | 22, 23 |
| 27 | `transform/macros/tests/test_requires_cutoff_flag.sql` | Create | Custom generic test: fails if a CEAP gold row is missing the cutoff qualifier | @data-quality-analyst | 25 |
| 28 | `transform/macros/tests/test_requires_legal_qualifiers.sql` | Create | Custom generic test: fails if a legal gold row is missing `status_processual`/`instancia` | @data-quality-analyst | 26 |
| 29 | `transform/models/silver/schema.yml` | Create | Contracts: `cpf` not_null + unique on `dim_politico`; provenance columns not_null on every model | @data-contracts-engineer | 23, 24 |
| 30 | `transform/models/gold/schema.yml` | Create | Applies the two custom generic tests at `severity: error` (halt_on_failure) | @data-contracts-engineer | 25, 26, 27, 28 |
| 31 | `orchestration/dags/farol_daily_batch.py` | Create | TaskFlow DAG: dynamically-mapped per-source ingestion → `dbt build` | @airflow-specialist | 13, 15 |
| 32 | `tests/ingestion/test_provenance.py` | Create | Unit test: every record carries `source_url`/`extracted_at`/`source_version` | @test-generator | 6 |
| 33 | `tests/ingestion/test_camara_pagination.py` | Create | AT-002: `dados: []` terminates cleanly, no corrupt records written | @test-generator | 8 |
| 34 | `tests/transform/ceap_cutoff.yml` (dbt unit test) | Create | AT-003: cutoff window applied against static fixture rows | @test-generator | 25 |

**Total Files:** 34

---

## Agent Assignment Rationale

> Agents discovered from `.claude/agents/` — Build phase invokes matched specialists.

| Agent | Files Assigned | Why This Agent |
|-------|-----------------|-----------------|
| @python-developer | 6, 7, 8, 9, 10, 11, 12 | `kb_domains: [python, pydantic, testing]` — dlt sources are plain Python with dataclasses/type hints, exactly this agent's specialization |
| @lakehouse-architect | 13, 16 | `kb_domains: [lakehouse, spark, data-modeling]` — DuckLake catalog attachment and the MinIO/S3 destination wiring are table-format/catalog concerns, not general Python or dbt modeling |
| @dbt-specialist | 15, 17, 18, 19, 20, 21, 22, 25, 26 | `kb_domains: [dbt, data-quality, sql-patterns]` — model development and project config is this agent's core purpose |
| @schema-designer | 23, 24 | Dimensional modeling / SCD specialist — `dim_politico` and its bridge table are exactly the grain-and-key decisions this agent owns, escalated from @dbt-specialist per its own `stop_conditions` |
| @data-quality-analyst | 27, 28 | `kb_domains: [data-quality, dbt, data-modeling]` — custom dbt generic tests enforcing the CEAP-cutoff and legal-status MUST goals |
| @data-contracts-engineer | 29, 30 | `kb_domains: [data-quality, data-modeling]` — schema.yml contracts (not_null/unique constraints, test severity) are schema-governance, not model-writing |
| @airflow-specialist | 31 | `kb_domains: [airflow, sql-patterns, data-quality]` — DAG implementation with TaskFlow and dynamic task mapping |
| @test-generator | 32, 33, 34 | Test automation specialist — pytest unit tests and the dbt fixture-based unit test |
| (general) | 1, 2, 3, 4, 5, 14 | No infrastructure/Docker specialist exists in this repo's agent roster (the `terraform`/`ci-cd-specialist` agents target cloud IaC and Azure DevOps, not local `docker-compose`); plain YAML/shell/Markdown handled directly |

**Agent Discovery:**
- Scanned: `.claude/agents/**/*.md`
- Matched by: file type, purpose keywords, path patterns, KB domains declared in each agent's frontmatter

---

## Code Patterns

### Pattern 1: dlt source with provenance stamping and pagination-trap handling

```python
# ingestion/common/provenance.py
"""Provenance injection shared by every dlt source — MUST-goal per DEFINE."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator

SOURCE_VERSION = "1.0.0"  # bump when a source's extraction logic changes


@dataclass(frozen=True)
class ProvenanceContext:
    source_url: str
    source_version: str = SOURCE_VERSION


def with_provenance(
    records: Iterator[dict[str, Any]], ctx: ProvenanceContext
) -> Iterator[dict[str, Any]]:
    """Stamp every record with source_url/extracted_at/source_version before it leaves ingestion."""
    extracted_at = datetime.now(timezone.utc).isoformat()
    for record in records:
        yield {
            **record,
            "_source_url": ctx.source_url,
            "_extracted_at": extracted_at,
            "_source_version": ctx.source_version,
        }
```

```python
# ingestion/sources/camara.py
"""Câmara dos Deputados REST source — deputados + proposições.

Handles the known pagination trap: /api/v2 returns `dados: []` (not a 404)
once you page past the last result — see docs/farolv1.md section 2.
"""
import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
PAGE_SIZE = 100  # API max


@dlt.source
def camara_source():
    return [deputados(), proposicoes()]


@dlt.resource(name="deputados", write_disposition="merge", primary_key="id")
def deputados():
    url = f"{BASE_URL}/deputados"
    ctx = ProvenanceContext(source_url=url)
    page = 1
    while True:
        resp = requests.get(url, params={"pagina": page, "itens": PAGE_SIZE}, timeout=30)
        resp.raise_for_status()
        dados = resp.json()["dados"]
        if not dados:  # empty page == end of results, not an error
            break
        yield from with_provenance(iter(dados), ctx)
        page += 1


@dlt.resource(name="proposicoes", write_disposition="append", primary_key="id")
def proposicoes(ano: int = dlt.config.value):
    url = f"{BASE_URL}/proposicoes"
    ctx = ProvenanceContext(source_url=url)
    page = 1
    while True:
        resp = requests.get(
            url, params={"ano": ano, "pagina": page, "itens": PAGE_SIZE}, timeout=30
        )
        resp.raise_for_status()
        dados = resp.json()["dados"]
        if not dados:
            break
        yield from with_provenance(iter(dados), ctx)
        page += 1
```

```python
# ingestion/pipeline.py
"""Entry point: runs every source, lands raw Parquet in MinIO."""
import dlt

from ingestion.sources.camara import camara_source
from ingestion.sources.ceap import ceap_source
from ingestion.sources.datajud import datajud_source
from ingestion.sources.senado import senado_source
from ingestion.sources.tse_bulk import tse_bulk_source

SOURCES = {
    "camara": camara_source,
    "senado": senado_source,
    "tse_bulk": tse_bulk_source,
    "ceap": ceap_source,
    "datajud": datajud_source,
}


def run_single_source(source_name: str) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=f"farol_raw_{source_name}",
        destination=dlt.destinations.filesystem(bucket_url="s3://farol-raw"),
        dataset_name="raw",
        loader_file_format="parquet",
    )
    info = pipeline.run(SOURCES[source_name]())
    print(info)  # dlt LoadInfo — surfaced to Airflow task logs for observability
```

### Pattern 2: dbt gold model applying the CEAP cutoff window, with an enforcing test

```sql
-- transform/models/gold/fact_ceap_gastos.sql
{{
    config(
        materialized='incremental',
        unique_key=['id_deputado', 'ano_mes'],
        incremental_strategy='merge',
        tags=['daily', 'ceap']
    )
}}

-- CEAP has a 90-day reimbursement submission lag (docs/farolv1.md section 3) —
-- any month inside that window is flagged, never summed as if final.
with despesas as (
    select *
    from {{ ref('stg_ceap__despesas') }}
    {% if is_incremental() %}
    where _extracted_at > (select max(_extracted_at) from {{ this }})
    {% endif %}
),

cutoff as (
    select current_date - interval '90 days' as cutoff_date
)

select
    d.id_deputado,
    date_trunc('month', d.data_documento) as ano_mes,
    sum(d.valor_liquido) as total_gasto,
    (date_trunc('month', d.data_documento) < date_trunc('month', c.cutoff_date)) as janela_fechada,
    max(d._source_url) as source_url,
    max(d._extracted_at) as extracted_at,
    max(d._source_version) as source_version
from despesas d
cross join cutoff c
group by 1, 2, c.cutoff_date
```

```sql
-- transform/macros/tests/test_requires_cutoff_flag.sql
-- Fails if any row in a CEAP-derived gold model is missing the janela_fechada qualifier.
{% test requires_cutoff_flag(model) %}
    select *
    from {{ model }}
    where janela_fechada is null
{% endtest %}
```

```yaml
# transform/models/gold/schema.yml (excerpt)
models:
  - name: fact_ceap_gastos
    tests:
      - requires_cutoff_flag:
          severity: error   # halt_on_failure — this is a MUST goal, not advisory
  - name: fact_processos_legais
    columns:
      - name: status_processual
        tests: [not_null]
      - name: instancia
        tests: [not_null]
    tests:
      - requires_legal_qualifiers:
          severity: error
```

### Pattern 3: Airflow 3.0 DAG with dynamic task mapping

```python
# orchestration/dags/farol_daily_batch.py
"""Daily batch: dlt ingestion (dynamic per source) -> dbt build.

One task per source via dynamic task mapping so a single source's failure
doesn't block the others (KB pitfall: one task per logical step, not one
monolithic ETL task).
"""
from datetime import datetime, timedelta

from airflow.sdk import dag, task

SOURCES = ["camara", "senado", "tse_bulk", "ceap", "datajud"]


@dag(
    dag_id="farol_daily_batch",
    schedule="@daily",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["farol", "daily"],
)
def farol_daily_batch():
    @task
    def run_source(source_name: str) -> str:
        from ingestion.pipeline import run_single_source

        run_single_source(source_name)
        return source_name

    @task
    def dbt_build() -> None:
        import subprocess

        subprocess.run(["dbt", "build", "--project-dir", "transform"], check=True)

    ingested = run_source.expand(source_name=SOURCES)
    ingested >> dbt_build()


farol_daily_batch()
```

### Pattern 4: Configuration structure

```yaml
# ingestion/config.yaml
sources:
  camara:
    base_url: "https://dadosabertos.camara.leg.br/api/v2"
    page_size: 100
  senado:
    base_url: "https://legis.senado.leg.br/dadosabertos"
  tse_bulk:
    base_url: "https://dadosabertos.tse.jus.br"
    election_years: [2018, 2022, 2026]
  ceap:
    base_url: "https://www.camara.leg.br/cotas"
    years: [2023, 2024, 2025, 2026]
  datajud:
    base_url: "https://api-publica.datajud.cnj.jus.br"
    api_key_env: "DATAJUD_API_KEY"

destination:
  raw_bucket: "s3://farol-raw"
  minio_endpoint_env: "MINIO_ENDPOINT"

orchestration:
  schedule: "@daily"
  retries: 2
  retry_delay_minutes: 5
```

```yaml
# transform/profiles.yml (example — not committed with real credentials)
farol:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ':memory:'
      extensions:
        - httpfs
        - ducklake
      attach:
        - path: "ducklake:postgres:dbname=ducklake_catalog host={{ env_var('POSTGRES_HOST') }} user={{ env_var('POSTGRES_USER') }} password={{ env_var('POSTGRES_PASSWORD') }}"
          alias: lakehouse
      settings:
        s3_endpoint: "{{ env_var('MINIO_ENDPOINT') }}"
        s3_access_key_id: "{{ env_var('MINIO_ACCESS_KEY') }}"
        s3_secret_access_key: "{{ env_var('MINIO_SECRET_KEY') }}"
        s3_use_ssl: false
        s3_url_style: path
      schema: lakehouse
```

---

## Data Flow

```text
1. Airflow triggers farol_daily_batch on the @daily schedule
   │
   ▼
2. Five ingestion tasks run in parallel (dynamic task mapping): each dlt
   source pulls from its API/bulk endpoint, stamps source_url/extracted_at/
   source_version, and writes Parquet to s3://farol-raw/{source}/{resource}/
   │
   ▼
3. dbt_build runs: bronze models read raw Parquet via read_parquet() and
   materialize typed, deduplicated DuckLake tables (first point the DuckLake
   Postgres catalog is touched)
   │
   ▼
4. Silver models resolve identity: dim_politico (CPF-keyed) and
   politico_id_externo (bridge table) are built from bronze Câmara/Senado/TSE
   │
   ▼
5. Gold models aggregate: fact_ceap_gastos applies the 90-day cutoff window,
   fact_processos_legais always carries status_processual/instancia
   │
   ▼
6. dbt tests run as part of `dbt build`; MUST-goal tests (cutoff flag, legal
   qualifiers, cpf not_null/unique) are severity:error and halt the pipeline
   on failure
```

---

## Integration Points

| External System | Integration Type | Authentication |
|------------------|-------------------|-----------------|
| Câmara dadosabertos API | REST | None required (public) |
| Senado dadosabertos API | REST/XML | None required (public) |
| TSE Dados Abertos (bulk) | HTTP file download | None required (public) |
| CEAP bulk (Câmara) | HTTP file download (ZIP) | None required (public) |
| DataJud (CNJ) | REST | API key (public but rate-limited, per `docs/farolv1.md`'s 🔑 marker) |
| MinIO | S3-compatible API | Access key / secret key |
| Postgres (DuckLake catalog + Airflow metadata) | SQL (libpq) | User / password |

---

## Testing Strategy

| Test Type | Scope | Files | Tools | Coverage Goal |
|-----------|-------|-------|-------|-----------------|
| Unit | Provenance stamping, pagination-trap handling | `tests/ingestion/test_provenance.py`, `tests/ingestion/test_camara_pagination.py` | pytest | 100% of `ingestion/common/` and the Câmara pagination branch |
| Unit (dbt) | CEAP cutoff window, legal-status qualifiers | `tests/transform/ceap_cutoff.yml`, `transform/macros/tests/*.sql` | dbt unit tests (`dbt test --select test_type:unit`) | All MUST-goal quality gates |
| Integration | Full `docker-compose up` → seeded query round-trip | `infra/README.md` (manual + scripted check) | docker-compose, DuckDB CLI | Validates AT-005 (15-minute bootstrap) |
| E2E | One full daily DAG run against real sources | Manual (Airflow UI) | Airflow | Happy path across all five sources |

### Acceptance Test Coverage

| DEFINE Acceptance Test | Covered By |
|--------------------------|------------|
| AT-001 (entity resolution happy path) | `transform/models/silver/dim_politico.sql` + `schema.yml` unique/not_null tests on `cpf` |
| AT-002 (Câmara pagination edge case) | `tests/ingestion/test_camara_pagination.py`, Pattern 1's `deputados()`/`proposicoes()` loop termination |
| AT-003 (CEAP 90-day lag window) | `fact_ceap_gastos.sql` + `test_requires_cutoff_flag.sql`, `tests/transform/ceap_cutoff.yml` |
| AT-004 (legal-status qualification) | `fact_processos_legais.sql` + `test_requires_legal_qualifiers.sql` |
| AT-005 (new contributor bootstrap) | `infra/docker-compose.yml` + `infra/README.md`, manually timed against the 15-minute target |

---

## Error Handling

| Error Type | Handling Strategy | Retry? |
|------------|---------------------|--------|
| REST 5xx/timeout (Câmara, Senado, DataJud) | dlt's built-in HTTP retry/backoff | Yes |
| Câmara `dados: []` end-of-pagination | Treated as a normal loop-termination signal, not an error | No — not a failure |
| Bulk file download failure/partial ZIP (TSE, CEAP) | Size/checksum verification before Parquet conversion; re-download on mismatch | Yes |
| dlt schema drift (new column from source) | dlt schema contract set to `evolve` for additive changes | No — logged, not retried |
| dlt schema drift (breaking type change) | dlt schema contract set to `freeze`; pipeline run fails loudly rather than silently coercing | No — alert, requires a code change |
| dbt test failure, MUST-goal gate (cutoff flag, legal qualifiers, `cpf` not_null/unique) | `severity: error`, blocks `dbt_build` and therefore the DAG | No — blocks, not retried automatically |
| dbt test failure, non-MUST gate | `severity: warn`, logged but does not block | No |
| Airflow task failure (any) | `retries=2, retry_delay=5min` per KB pitfall guidance | Yes |
| MinIO/Postgres transiently unavailable | dlt/dbt fail fast; Airflow's task-level retry absorbs short outages | Yes |

---

## Configuration

| Config Key | Type | Default | Description |
|------------|------|---------|--------------|
| `MINIO_ENDPOINT` | string | `http://minio:9000` | MinIO S3-compatible endpoint |
| `MINIO_ACCESS_KEY` / `MINIO_SECRET_KEY` | string | — (required, no default) | MinIO credentials |
| `POSTGRES_HOST` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | string | — (required, no default) | DuckLake catalog + Airflow metadata DB |
| `DATAJUD_API_KEY` | string | — (required, no default) | DataJud REST API key; stored as an Airflow Connection, not a plain env var, in orchestration |
| `FAROL_RAW_BUCKET` | string | `s3://farol-raw` | Raw-layer landing bucket |
| `SOURCE_VERSION` | string | `1.0.0` | Bumped manually per source when extraction logic changes; propagates into every record's `_source_version` |
| `AIRFLOW__CORE__EXECUTOR` | string | `LocalExecutor` | Matches the self-hosted small-cluster, no-autoscaling constraint |

---

## Security Considerations

- Donor CPF and other third-party PII must be masked/hashed before landing in bronze — `ingestion/common/privacy.py` establishes the transformer interface now so the sources that actually carry donor CPF (TSE prestação de contas, Portal da Transparência — both deferred) plug into it without a later architectural change.
- All secrets (MinIO keys, Postgres password, DataJud API key) are supplied via `.env` (gitignored) locally and Airflow Connections/Variables in orchestration — never hardcoded in DAGs, dbt profiles, or committed config.
- MinIO's `farol-raw` bucket is created private by default (`infra/minio/init-buckets.sh`); no public-read policy.
- The "a homonym isn't the same person, a first-instance ruling isn't a conviction" MUST goal is enforced structurally by `test_requires_legal_qualifiers.sql` at `severity: error`, not left as a documentation-only warning that a future contributor could miss.

---

## Observability

| Aspect | Implementation |
|--------|------------------|
| Logging | dlt's `LoadInfo` (rows loaded, load ID, schema version) printed per source run, captured in Airflow task logs |
| Metrics | dbt's `run_results.json`, parsed after every `dbt build` into a `quality.audit_log` table (adapted from the KB medallion data-quality-gates pattern) tracking pass/fail per test per run |
| Tracing | Airflow's native per-task logging and retry history in its UI; DAG tagged `farol`/`daily` for filtering |

---

## Pipeline Architecture (if applicable)

### DAG Diagram

```text
[Câmara REST] ──┐
[Senado REST]  ──┤
[TSE Bulk]     ──┼──extract(dlt)──▶ [Raw: MinIO Parquet + provenance] ──stage(dbt)──▶ [Bronze: DuckLake]
[CEAP Bulk]    ──┤                                                                         │
[DataJud REST] ──┘                                                                         ▼ model(dbt)
                                                                          [Silver: dim_politico + bridge]
                                                                                            │
                                                                                            ▼ aggregate(dbt)
                                                                    [Gold: fact_ceap_gastos, fact_processos_legais]
                                                                                            │
                                                                                            ▼
                                                                [Quality Gate: dbt tests, severity:error halts]
```

### Partition Strategy

| Table | Partition Key | Granularity | Rationale |
|-------|-----------------|--------------|-------------|
| `stg_ceap__despesas` | `ano` | Yearly | Matches CEAP's native annual ZIP file layout; avoids re-parsing untouched years |
| `stg_camara__proposicoes` | `ano` | Yearly | Câmara publishes proposições bulk files annually |
| `stg_datajud__processos` | `ano_ajuizamento` | Yearly | Matches DataJud's typical case-year segmentation |
| `fact_ceap_gastos` | `ano_mes` | Monthly | Aligns with the 90-day cutoff window, which is month-granular |

### Incremental Strategy

| Model | Strategy | Key Column | Lookback |
|-------|----------|-------------|-----------|
| `dim_politico` | merge | `cpf` | N/A — full dimension, low volume |
| `politico_id_externo` | merge | (`fonte`, `id_externo`) | N/A |
| `stg_ceap__despesas` | merge | (`id_deputado`, `num_ressarcimento`) | 90 days (reimbursement lag) |
| `fact_ceap_gastos` | merge | (`id_deputado`, `ano_mes`) | 90 days |
| `stg_datajud__processos` | append | N/A | N/A |

### Schema Evolution Plan

| Change Type | Handling | Rollback |
|-------------|-----------|-----------|
| New column | dlt schema contract `evolve` adds it at raw automatically; dbt bronze models pick it up on next `dbt run` with `on_schema_change='append_new_columns'` | Drop column |
| Type change | dlt schema contract `freeze` fails the load loudly rather than silently coercing; requires a source-module code change | Revert type in the dlt resource |
| Column removal | Deprecate in `schema.yml` contract first, remove from the bronze model after a documented grace period | Re-add column, backfill from raw Parquet (still present due to snapshot retention) |

### Data Quality Gates

| Gate | Tool | Threshold | Action on Failure |
|------|------|-----------|----------------------|
| `dim_politico.cpf` not null / unique | dbt test (`not_null` + `unique`) | 0 violations | Block pipeline (`severity: error`) |
| `fact_ceap_gastos.janela_fechada` not null | dbt custom generic test (`requires_cutoff_flag`) | 0 violations | Block pipeline (`severity: error`) |
| `fact_processos_legais.status_processual`/`instancia` not null | dbt custom generic test (`requires_legal_qualifiers`) | 0 violations | Block pipeline (`severity: error`) |
| Bronze row-count vs. previous run | dbt `row_count_ratio` test (KB `dbt/patterns/generic-tests.md`) | 90–110% of prior run | Alert + continue (`severity: warn`) |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-05 | design-agent | Initial version, derived from DEFINE_FAROL_LAKEHOUSE_ARCHITECTURE.md |

---

## Next Step

**Ready for:** `/ship .claude/sdd/features/DEFINE_FAROL_LAKEHOUSE_ARCHITECTURE.md`
