select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as contract_id,
    json_extract_scalar(normalized_json, '$.document') as commitment_id,
    json_extract_scalar(normalized_json, '$.document_number') as commitment_number,
    cast(json_extract_scalar(normalized_json, '$.date') as date) as issued_at,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.committed') as decimal(20,6)) as committed,
    cast(json_extract_scalar(normalized_json, '$.liquidated') as decimal(20,6)) as liquidated,
    cast(json_extract_scalar(normalized_json, '$.paid') as decimal(20,6)) as paid,
    cast(json_extract_scalar(normalized_json, '$.rp_registered') as decimal(20,6)) as rp_registered,
    cast(json_extract_scalar(normalized_json, '$.rp_paid') as decimal(20,6)) as rp_paid
from {{ ref('current_observation') }} where resource='compras_empenhos'
