with batches as (
    select *, row_number() over (
        partition by resource, partition_key order by extracted_at desc, run_id desc
    ) as recency
    from {{ source('bronze', 'complete_batch') }}
)
select o.*, concat(o.run_id, ':', cast(o.row_ordinal as varchar)) as observation_id
from {{ source('bronze', 'expense_observation') }} o
join batches b on o.run_id = b.run_id and b.recency = 1
where o.normalized_json is not null
