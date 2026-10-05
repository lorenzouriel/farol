#!/usr/bin/env bash
set -euo pipefail

superset db upgrade
superset fab create-admin --username admin --firstname Farol --lastname Local --email admin@localhost \
  --password "${SUPERSET_ADMIN_PASSWORD}" || true
superset init
(python /app/lakehouse/bootstrap.py || echo "Trino registration failed; rerun: docker compose exec superset python /app/lakehouse/bootstrap.py") &
exec gunicorn --bind 0.0.0.0:8088 --workers 1 --threads 4 --timeout 120 "superset.app:create_app()"
