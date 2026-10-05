# Local stack validation

Verified on 2026-10-05 using Docker Desktop (Linux engine 29.1.3).

- Compose configuration validates.
- Seven persistent services report healthy: SeaweedFS, Nessie, Spark Connect,
  Trino, PostgreSQL metadata, Airflow and Superset.
- One-shot storage initialization completed and created the warehouse bucket.
- `python -m farol.bootstrap` passed: Spark wrote a temporary Iceberg table and
  Trino read the expected row. The temporary table was dropped.
- Bronze, silver and gold namespaces exist.
- `dbt debug` passed; `dbt run` created `lake.gold.local_stack_check` (one synthetic row).
- Airflow discovered the paused, manually triggered `farol_local` DAG; import errors: none.
- Superset's `Farol` Trino connection is registered; repeated registration is idempotent.

Trino 476 with this Nessie catalog rejects view creation, so dbt uses table
materialization. The installed dbt 1.10 series emits a deprecation notice;
versions were retained to match the reference lab. No government-source ingestion
or expense data validation is implied by these infrastructure checks.
