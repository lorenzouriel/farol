select * from {{ source('bronze', 'capability_registry') }}
