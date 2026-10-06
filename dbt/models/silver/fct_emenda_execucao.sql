select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    json_extract_scalar(normalized_json, '$.amendment') as amendment_id,
    json_extract_scalar(normalized_json, '$.author') as author_name,
    json_extract_scalar(normalized_json, '$.locality') as locality,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.committed') as decimal(20,6)) as committed,
    cast(json_extract_scalar(normalized_json, '$.liquidated') as decimal(20,6)) as liquidated,
    cast(json_extract_scalar(normalized_json, '$.paid') as decimal(20,6)) as paid,
    cast(json_extract_scalar(normalized_json, '$.rp_registered') as decimal(20,6)) as rp_registered,
    cast(json_extract_scalar(normalized_json, '$.rp_cancelled') as decimal(20,6)) as rp_cancelled,
    cast(json_extract_scalar(normalized_json, '$.rp_paid') as decimal(20,6)) as rp_paid
from {{ ref('current_observation') }} where resource='cgu_emendas'
