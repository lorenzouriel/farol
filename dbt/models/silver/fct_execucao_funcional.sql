select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    json_extract_scalar(normalized_json, '$.function') as function_code,
    json_extract_scalar(normalized_json, '$.subfunction') as subfunction_code,
    json_extract_scalar(normalized_json, '$.program') as program_code,
    json_extract_scalar(normalized_json, '$.action') as action_code,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.committed') as decimal(20,6)) as committed,
    cast(json_extract_scalar(normalized_json, '$.liquidated') as decimal(20,6)) as liquidated,
    cast(json_extract_scalar(normalized_json, '$.paid') as decimal(20,6)) as paid
from {{ ref('current_observation') }} where resource='cgu_funcional'
