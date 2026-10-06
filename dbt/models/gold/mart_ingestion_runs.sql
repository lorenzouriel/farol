select * from {{ source('bronze', 'ingestion_runs') }}
