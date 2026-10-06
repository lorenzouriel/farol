select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as municipality,
    json_extract_scalar(normalized_json, '$.entity_name') as organization,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    cast(json_extract_scalar(normalized_json, '$.month') as integer) as reference_month,
    cast(json_extract_scalar(normalized_json, '$.date') as date) as event_date,
    json_extract_scalar(normalized_json, '$.document') as commitment_document,
    json_extract_scalar(normalized_json, '$.stage') as expense_stage,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.amount') as decimal(20,6)) as amount
from {{ ref('current_observation') }}
where resource = 'tce_sp_despesas'
