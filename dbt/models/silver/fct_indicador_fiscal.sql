select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as entity_id,
    json_extract_scalar(normalized_json, '$.entity_name') as entity_name,
    json_extract_scalar(normalized_json, '$.revision') as revision_id,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    json_extract_scalar(normalized_json, '$.indicator') as indicator,
    cast(json_extract_scalar(normalized_json, '$.numerator') as decimal(20,6)) as numerator,
    cast(json_extract_scalar(normalized_json, '$.denominator') as decimal(20,6)) as denominator,
    cast(json_extract_scalar(normalized_json, '$.percentage') as decimal(20,6)) as published_percentage
from {{ ref('current_observation') }} where resource = 'tce_rs_educacao'
