# Expense lakehouse: operating the bounded v1 pilot

The running pipeline is a **partial implementation of the v1 plan**. All 42 catalog capabilities
are tracked; only explicitly configured, validated partitions can contribute financial records.
`pilot_loaded` means that configured scope passed its contract, not that an entire source is complete.

## Start and run

From the repository root in PowerShell, with Docker Desktop Linux containers running:

```powershell
docker compose up -d --build --wait --wait-timeout 600
.\scripts\despesas.ps1 -Action test
.\scripts\despesas.ps1 -Action run
.\scripts\despesas.ps1 -Action status
```

Do not overwrite the existing `.env`. `TRANSPARENCIA_API_KEY` is used for CGU requests.
The other configured API keys are not required for this expense pilot.

Open Superset at http://127.0.0.1:18088 (admin and the configured `SUPERSET_ADMIN_PASSWORD`).
Open the newest published **Farol despesas v1 — bounded pilot** dashboard. Its coverage table
is authoritative for which capabilities were loaded. Chart titles describe non-additive financial
semantics; each table has a 1,000-row display limit, which is not an ingestion limit.

Airflow: http://127.0.0.1:18081. `despesas_v1` is a manual DAG with ingestion, transformation
and dashboard tasks. `max_active_runs=1` plus a PostgreSQL advisory lock serialize conflicting
operations. The test runner can execute it explicitly:

```powershell
docker compose exec -T airflow airflow dags test despesas_v1 2026-10-05
```

## Currently configured coverage

| Resource | Scope and behavior |
|---|---|
| CGU organizations | 2025, superior organization 26000; complete pagination to empty page |
| CGU functional classification | 2025, education function 12, action 20RZ; separate program/classification rows |
| CGU amendments | Amendment 202542900005, year 2025; restos a pagar kept separately |
| TCE-SP | Adamantina, January 2025; preserves all source rows and separate cancellation events |
| SICONFI | São Paulo 3550308 / 2025: RREO bimestre 1 expense cells (annex 01), RGF Executivo quadrimestre 1 personnel-expense rolling-12-month totals (annex 01), DCA annual expense columns (annex I-D) |
| TCE-PI | Prefeitura 1473, 2025 annual totals; upstream years retained raw, selected year filtered explicitly |
| TCE-RS | 2025 published MDE indicators; original three-decimal values preserved |
| Compras | Unit 153001 directory, contract 474056 commitments and invoices; linked historical commitment may precede 2025 |
| Câmara | Current deputy directory; deputy 204379 January 2025 CEAP is quarantined if the response is empty |
| TCE-PE | Jurisdiction directory decoded using upstream ISO-8859-1; expense route remains disabled pending contract validation |
| TCE-RN / TCE-CE | Expense resources explicitly blocked; see config reasons |

The source catalog has 42 query capabilities; the implementation does not equate each capability
to a table. Unimplemented adapters appear as `contract_pending`, not successful or zero-valued.
CGU detail/documents, cards, travel, historical COVID, beneficiary queries, related-item queries,
remaining SICONFI support queries and TCE capabilities still need verified adapters and mappings.
No automated supplier crosswalk, nationwide backfill, or complete v1 release is claimed.

## Storage and financial meaning

- `s3://warehouse/raw/<source>/<resource>/<run-id>/<request-hash>/<page>-<uuid>.json.gz`
  contains immutable original response bodies. Objects contain no credentials in their names.
  HTTP error bodies are retained, and may include upstream messages; do not publish raw objects.
- `lake.bronze.expense_observation` holds source records, normalized projections and raw-object
  lineage. JSON decimals are decoded as Decimal; raw JSON numbers may be serialized as strings
  in the record projection, while the original bytes remain available in S3.
- `lake.bronze.complete_batch` marks only contract-validated, complete partition snapshots.
  `lake.silver.current_observation` selects the latest such batch per resource/partition.
- Silver facts keep CGU totals, SP movements, fiscal cells, ratios, amendments and invoices separate.
  Monetary columns use DECIMAL(20,6), preserving source precision. There is no global “total spent”.
- Cancellation stage is `cancellation_unspecified`, not automatically netted from commitments.
  An invoice is never converted into a payment. Fiscal hierarchy rows and percentages are non-additive.
- No CPF, personal contact details or supplier identity is projected into the implemented gold marts.
  Raw responses retain source records and are only available to trusted local operators.

## Operations and publication

`farol_ops` is a separate PostgreSQL database, migrated idempotently even with existing Docker volumes.
It contains ingestion runs, per-page hashes/byte sizes, quality results, completed checkpoints and
publication state. It is separate from Airflow's own metadata database.

Financial batches that are empty, out-of-scope, malformed, duplicated at a declared natural grain,
or incomplete at a page cap are quarantined. These batches do not replace the latest good financial
snapshot. Empty CEAP does not mean a deputy spent nothing. Lookup arrays may legitimately be empty.
SP has no reliable unique transaction ID in the observed payload: identical-looking source rows are
retained using snapshot row ordinals, not deduplicated by date/payee/amount.

Each dbt publication builds a unique `lake.gold_r<release-id>` schema and runs quality checks.
Only a successful build becomes `ready`. Superset creates a new dashboard and queries every chart
before making it visible; then publication becomes `published`. A failed release does not overwrite
the previous dashboard or gold tables. Shared silver tables may change during a failed build;
published dashboards query immutable gold tables only.

Dashboard registration failures can leave unpublished draft dashboards/datasets. They do not replace
the prior published release. Retry the ready release with:

```powershell
docker compose exec -T superset python -m farol.expenses.dashboard
```

## Recovery, replay and expansion

```powershell
# Resume transiently failed/running runs using durable successful pages.
.\scripts\despesas.ps1 -Action ingest -Resource tce_sp_despesas -Resume

# Fetch a fresh complete snapshot after fixing a quarantined source contract.
.\scripts\despesas.ps1 -Action ingest -Resource tce_pe_unidades

# Build and publish from the latest good batches, without external requests.
.\scripts\despesas.ps1 -Action publish
```

Resume requires the same configuration hash. HTTP errors are refetched; successful saved pages are
checksum-verified and reused. Quarantined runs require a fresh run after investigation, because a
successful HTTP response can still contain invalid data. Ingestion exits 2 for partial coverage;
infrastructure failures stop publication. The DAG intentionally allows healthy-source publication
with visible partial coverage; a successful DAG does not certify every source.

Edit `conf/despesas.yml` to change approved year/entity allowlists or enable a verified adapter.
Do not expand to all years or municipalities without measuring pages, source quotas and disk use.
HTTP calls have time/size/page caps, bounded retries, same-origin pagination, and per-resource pacing.
Long Retry-After values stop the batch instead of bypassing the server's requested delay.

Run tests after contract changes. Add fixture coverage and a bounded live check for each new financial
mapping. Retention, raw deletion, orphan-file removal, snapshot expiration, scheduled refresh and
daily live smoke jobs are not enabled. Volumes persist across normal container restarts; deleting
Docker volumes or resetting Docker Desktop can destroy local data. Keep external backups if needed.
