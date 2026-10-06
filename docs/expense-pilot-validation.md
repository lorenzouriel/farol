# Expense pilot validation

Verified during the 2026-10-05/06 implementation session. Counts below describe the explicit
pilot partitions, not full-source coverage or a current Docker health check.

| Resource | Raw records | Financial projection records |
|---|---:|---:|
| CGU organizations, superior 26000 / 2025 | 117 | 117 |
| CGU functional classification, function 12 / action 20RZ / 2025 | 2 | 2 |
| CGU amendment 202542900005 | 1 | 1 |
| SP Adamantina / January 2025 | 4,136 | 4,136 |
| SICONFI São Paulo / 2025 bimestre 1 | 3,006 | 91 expense cells |
| SICONFI São Paulo / RGF 2025 quadrimestre 1 Executivo | 301 | 10 rolling-12-month expense cells |
| SICONFI São Paulo / DCA 2025 | 3,197 | 286 annual expense cells |
| PI prefeitura 1473 annual totals | 17 years | 1 selected year |
| RS MDE indicators / 2025 | 476 | 476 |
| Contract 474056 commitments | 1 | 1 |
| Contract 474056 invoices | 5 | 5 |
| Câmara current deputies | 513 | Directory only |
| SP municipalities | 644 | Directory only |
| PI prefeituras | 224 | Directory only |
| PE jurisdictions | 1,817 | Directory only |
| Compras unit 153001 contracts | 26 | Directory only |

- Authenticated CGU extraction succeeded using the configured key.
- The first gold release `gold_rf849e1f6078f47ee` built 24 models and passed all four dbt tests.
- Superset published dashboard `/superset/dashboard/1/` with 12 chart queries executed successfully.
- A fresh SP snapshot retained 4,136 records; latest-batch selection prevents summing repeated snapshots.
- PE's ISO-8859-1 response was initially quarantined, then loaded after honoring the declared encoding.
- CEAP samples returned empty arrays and were quarantined; no zero-spending claim is made.
- The latest offline suite has 17 passing tests, including exact decimal handling, pagination loops,
  page caps, cache reuse, cross-origin pagination, legacy encoding, scope and financial grain checks.

After Docker became unavailable during continuation, the stack was rebuilt and the bounded pilot
reloaded. A fresh `airflow dags test despesas_v1 2026-10-06` completed successfully on 2026-10-06:
all three tasks (ingestion, dbt transformation/tests, dashboard publication) passed. Its published
release was `gold_r3d9cf2a679f14a15`, with dashboard `/superset/dashboard/1/`.
A subsequent PowerShell-wrapper ingestion replay and publication also passed. The latest release
is `gold_r57b8792b679145c8`, with [dashboard 2](http://127.0.0.1:18088/superset/dashboard/2/).
It passed all 24 model builds, four dbt tests, and 12 dashboard chart queries. Silver still contains
4,136 SP records and one CGU amendment after replay; current observations total 8,350.
All seven long-running Compose services were healthy at the final check.

The snapshot contains 35 saved response pages (5,783,135 original response-body bytes), including
repeated extraction snapshots. Only three pages have the newly added request-URL provenance fields;
older pages retain their raw-object references and hashes. These are pilot extraction counts, not
estimates of full upstream size. One earlier release remains `ready` and unpublished after the
PowerShell stderr handling interruption; it does not replace the latest published dashboard.

The current release and row counts are captured in [the live status snapshot](despesas-v1-status.json).

The checklist lists unimplemented capabilities separately. This is a partial v1 pilot, not all
42 capabilities. Runtime availability and the newest publication are reported by the status command.
