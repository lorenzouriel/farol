-- Runs once, on first Postgres container start (docker-entrypoint-initdb.d).
-- Creates the two databases this stack needs on a single Postgres instance:
--   ducklake_catalog — DuckLake table-format metadata (snapshots, schema versions)
--   airflow           — Airflow's own metadata DB

CREATE DATABASE ducklake_catalog;
CREATE DATABASE airflow;
