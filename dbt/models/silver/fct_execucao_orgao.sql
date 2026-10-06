select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as entity_id,
    json_extract_scalar(normalized_json, '$.entity_name') as entity_name,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    json_extract_scalar(normalized_json, '$.superior') as superior_id,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.committed') as decimal(20,6)) as committed,
    cast(json_extract_scalar(normalized_json, '$.liquidated') as decimal(20,6)) as liquidated,
    cast(json_extract_scalar(normalized_json, '$.paid') as decimal(20,6)) as paid
from {{ ref('current_observation') }}
where resource = 'cgu_execucao_orgao'
