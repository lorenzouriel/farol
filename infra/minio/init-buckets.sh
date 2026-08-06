#!/bin/sh
# Runs once via the minio-init container. Creates the private raw-layer bucket.
set -eu

mc alias set local "$MINIO_ENDPOINT" "$MINIO_ACCESS_KEY" "$MINIO_SECRET_KEY"

if ! mc ls "local/$FAROL_RAW_BUCKET" >/dev/null 2>&1; then
  mc mb "local/$FAROL_RAW_BUCKET"
fi

# No public-read policy — bucket stays private (see DESIGN Security Considerations).
mc anonymous set none "local/$FAROL_RAW_BUCKET"

echo "Bucket $FAROL_RAW_BUCKET ready."
