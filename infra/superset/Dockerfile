FROM apache/superset:5.0.0

USER root
RUN uv pip install --python /app/.venv/bin/python --no-cache "psycopg2-binary>=2.9" "trino[sqlalchemy]>=0.333" "requests>=2.31"
COPY superset_config.py /app/pythonpath/superset_config.py
COPY bootstrap.py /app/lakehouse/bootstrap.py
COPY --chmod=0755 entrypoint.sh /app/lakehouse/entrypoint.sh
USER superset

ENTRYPOINT ["/app/lakehouse/entrypoint.sh"]
