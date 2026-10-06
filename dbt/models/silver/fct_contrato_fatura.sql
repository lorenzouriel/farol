select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as contract_id,
    json_extract_scalar(normalized_json, '$.document') as invoice_id,
    cast(json_extract_scalar(normalized_json, '$.date') as date) as issued_at,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    json_extract_scalar(normalized_json, '$.cancelled') as source_cancelled,
    json_extract_scalar(normalized_json, '$.status') as source_status,
    cast(json_extract_scalar(normalized_json, '$.gross') as decimal(20,6)) as invoice_gross,
    cast(json_extract_scalar(normalized_json, '$.net') as decimal(20,6)) as invoice_net
from {{ ref('current_observation') }} where resource='compras_faturas'
