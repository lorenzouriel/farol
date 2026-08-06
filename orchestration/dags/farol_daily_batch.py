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

        subprocess.run(
            [
                "dbt",
                "build",
                "--project-dir",
                "transform",
                "--profiles-dir",
                "transform",
            ],
            check=True,
        )

    ingested = run_source.expand(source_name=SOURCES)
    ingested >> dbt_build()


farol_daily_batch()
