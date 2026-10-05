"""Manual infrastructure smoke test; never fetches external source data."""
from datetime import datetime, timezone
from airflow.sdk import dag, task


@dag(schedule=None, start_date=datetime(2026, 1, 1, tzinfo=timezone.utc), catchup=False,
     tags=["farol", "infrastructure"])
def farol_local():
    @task(pool="spark")
    def verify_lakehouse():
        from farol.bootstrap import bootstrap
        bootstrap()
    verify_lakehouse()


farol_local()
