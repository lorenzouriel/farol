select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as entity_id,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    cast(json_extract_scalar(normalized_json, '$.period') as integer) as reference_period,
    json_extract_scalar(normalized_json, '$.statement') as statement_type,
    json_extract_scalar(normalized_json, '$.periodicity') as periodicity,
    json_extract_scalar(normalized_json, '$.label') as row_label,
    json_extract_scalar(normalized_json, '$.annex') as annex,
    json_extract_scalar(normalized_json, '$.account') as account_code,
    json_extract_scalar(normalized_json, '$.account_name') as account_name,
    json_extract_scalar(normalized_json, '$.column') as statement_column,
    json_extract_scalar(normalized_json, '$.basis') as measure_basis,
    cast(json_extract_scalar(normalized_json, '$.amount') as decimal(20,6)) as amount
from {{ ref('current_observation') }} where resource in ('siconfi_rreo','siconfi_rgf','siconfi_dca')
