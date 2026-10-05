#!/usr/bin/env bash
set -euo pipefail

airflow db migrate
airflow pools set spark "${EXTRACT_POOL_SLOTS:-2}" "Concurrent extract tasks on Spark Connect"
exec airflow standalone
