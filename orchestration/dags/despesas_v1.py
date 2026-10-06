"""Manual bounded ingestion and quality-gated publication; schedules remain paused."""
from datetime import datetime, timezone
from airflow.sdk import dag, task


@dag(schedule=None,start_date=datetime(2026,1,1,tzinfo=timezone.utc),catchup=False,
     max_active_runs=1,tags=['farol','despesas','pilot'])
def despesas_v1():
    @task(pool='spark')
    def ingest():
        from farol.expenses.pipeline import run
        # Source failures are recorded and displayed; healthy partitions can publish.
        complete = run(resume=True)
        return {'all_configured_resources_complete':complete}

    @task(pool='spark')
    def transform(_coverage):
        from farol.expenses.publish import build_release
        return build_release()

    @task
    def dashboard(release):
        from farol.expenses.dashboard import publish_dashboard
        return publish_dashboard(release)

    dashboard(transform(ingest()))


despesas_v1()
