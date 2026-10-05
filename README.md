# Farol local lakehouse

Based on `lab-lakehouse-oss`: SeaweedFS 3.97 (S3), Nessie 0.104.2,
Iceberg 1.9.2, Spark Connect 3.5.6, Trino 476, Airflow 3.1.0,
PostgreSQL 17 metadata, dbt and Superset 5.0.0. Versions match the reference.

```mermaid
flowchart LR
  A[Airflow] --> S[Spark Connect]
  S --> N[Nessie catalog]
  S --> O[SeaweedFS / Iceberg files]
  D[dbt] --> T[Trino]
  T --> N
  T --> O
  U[Superset] --> T
  A --> P[PostgreSQL metadata]
  U --> P
```

The Compose project, network, images and volumes are separate from the reference lab.
Its synthetic source databases and business models are excluded. External API ingestion
is not implemented by this infrastructure setup. API keys stay in the existing `.env`
and are not passed to services until a source integration needs them.

## Start on Windows

Start Docker Desktop with Linux containers. Allow about 10 GB RAM for Docker
(service limits total approximately 7.5 GiB, plus build/runtime overhead).
Run these commands from this repository in PowerShell:

```powershell
# Keep your existing .env. Only copy the example for a new checkout without one.
if (!(Test-Path .env)) { Copy-Item .env.example .env }
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 600
docker compose exec airflow python -m farol.bootstrap
docker compose exec airflow /opt/airflow/dbt-venv/bin/dbt debug --project-dir /opt/lakehouse/dbt --profiles-dir /opt/lakehouse/dbt
docker compose exec airflow /opt/airflow/dbt-venv/bin/dbt run --project-dir /opt/lakehouse/dbt --profiles-dir /opt/lakehouse/dbt
```

The bootstrap creates bronze/silver/gold namespaces and writes a temporary Iceberg
table through Spark, reads it through Trino, then drops it. dbt creates the synthetic
`lake.gold.local_stack_check` table. Models materialize as tables because Trino's
Nessie connector does not support creating views. Neither command ingests government data.
The same smoke check is available as the manually triggered `farol_local` Airflow DAG.

| Service | Local address | Access |
|---|---|---|
| Airflow | http://127.0.0.1:18081 | Local SimpleAuth all-admin mode |
| Superset | http://127.0.0.1:18088 | admin / `SUPERSET_ADMIN_PASSWORD` (default admin) |
| Trino | http://127.0.0.1:18080 | User farol; no password |
| Nessie | http://127.0.0.1:29120/api/v2 | Catalog API |
| S3 | http://127.0.0.1:18333 | Credentials in `.env.example` / Compose defaults |
| Spark Connect | sc://127.0.0.1:25002 | Spark client |

Superset automatically registers the `Farol` Trino connection using `trino://farol@trino:8080/lake`.
After dbt runs, add the `gold.local_stack_check` dataset to verify SQL connectivity.
No expense dashboards or production authentication are configured. Services bind to
loopback; these development defaults are intended only for your local machine.

Host ports can be changed in `.env`; containers use internal service names and ports.
Keep infrastructure passwords URL-safe because metadata connection URIs embed them.
The reference's dbt environment and Great Expectations tooling are installed in Airflow;
business models and quality rules still need to be implemented for Farol.

```powershell
docker compose ps
docker compose logs --tail 100
docker compose down  # stops Farol, keeps persisted data
```

Avoid `down -v` unless you intend to erase Farol's persisted storage and metadata.
Optional host Python development: `uv sync` (Python 3.11+); Docker provides the Python
runtime needed for the commands above. The API audit scripts remain in `scripts/`.
