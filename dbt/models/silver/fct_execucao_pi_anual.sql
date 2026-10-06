select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as entity_id,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.committed') as decimal(20,6)) as committed,
    cast(json_extract_scalar(normalized_json, '$.liquidated') as decimal(20,6)) as liquidated,
    cast(json_extract_scalar(normalized_json, '$.paid') as decimal(20,6)) as paid
from {{ ref('current_observation') }} where resource = 'tce_pi_totais'
