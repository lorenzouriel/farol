# Farol infra

Self-hosted stack: MinIO (raw Parquet storage) + Postgres (DuckLake catalog
+ Airflow metadata) + Airflow (daily batch orchestration). DuckDB itself is
embedded — it runs inside the ingestion and dbt processes, not as a service.

## Bootstrap (target: under 15 minutes on a clean machine)

1. Install Docker and Docker Compose.
2. Copy the env template and fill in real secrets:

   ```bash
   cp infra/.env.example infra/.env
   ```

3. From `infra/`, bring up the stack:

   ```bash
   docker compose --env-file .env up -d
   ```

4. Wait for Airflow's UI at <http://localhost:8080> (default `standalone`
   admin credentials are printed in the `airflow` container logs on first
   boot: `docker compose logs airflow | grep password`).
5. Confirm MinIO's console at <http://localhost:9001> shows the `farol-raw`
   bucket (created automatically by `minio-init`).
6. Verify DuckDB can reach the DuckLake catalog:

   ```bash
   pip install duckdb
   python -c "
   import duckdb
   con = duckdb.connect()
   con.execute(\"INSTALL ducklake; LOAD ducklake;\")
   con.execute(
       \"ATTACH 'ducklake:postgres:dbname=ducklake_catalog host=localhost \"
       \"user=$POSTGRES_USER password=$POSTGRES_PASSWORD' AS lakehouse\"
   )
   print(con.execute('SHOW DATABASES').fetchall())
   "
   ```

If step 6 lists `lakehouse`, the stack is up — see `infra/README.md`'s
counterpart in `ingestion/` and `transform/` for how to run the first
ingestion + dbt build.

## Services

| Service | Purpose | Port |
|---------|---------|------|
| `minio` | S3-compatible object storage for raw Parquet | 9000 (API), 9001 (console) |
| `minio-init` | One-shot: creates the private `farol-raw` bucket, then exits | - |
| `postgres` | `ducklake_catalog` (table metadata) + `airflow` (Airflow metadata) databases | 5432 |
| `airflow` | `airflow standalone` — scheduler + webserver + triggerer in one process, `LocalExecutor` | 8080 |

## Teardown

```bash
docker compose down          # stop, keep volumes (data persists)
docker compose down -v       # stop and delete all data
```
