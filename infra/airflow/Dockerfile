FROM apache/airflow:3.1.0-python3.11

USER airflow
RUN pip install --no-cache-dir \
        "pyspark[connect]==3.5.6" "pandas>=2.0,<3" "pyarrow>=15" "pyyaml>=6" "numpy>=1.26" \
        "trino[sqlalchemy]>=0.333" "great-expectations>=1.3,<2" "pytest>=8" \
    && python -m venv /opt/airflow/dbt-venv \
    && /opt/airflow/dbt-venv/bin/pip install --no-cache-dir "dbt-core>=1.10,<1.11" "dbt-trino>=1.9"

COPY --chown=airflow:root --chmod=0755 entrypoint.sh /opt/airflow/lakehouse-entrypoint.sh
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/opt/airflow/lakehouse-entrypoint.sh"]
