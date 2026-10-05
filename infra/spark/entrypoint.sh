#!/usr/bin/env bash
set -euo pipefail

envsubst '${NESSIE_REF} ${S3_ACCESS_KEY} ${S3_SECRET_KEY} ${S3_ENDPOINT}' \
  < /opt/spark/conf/spark-defaults.conf.template > /opt/spark/conf/spark-defaults.conf

export SPARK_NO_DAEMONIZE=1
exec /opt/spark/sbin/start-connect-server.sh
