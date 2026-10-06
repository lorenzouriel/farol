select observation_id, source, partition_key, run_id, raw_object_key, extracted_at,
    json_extract_scalar(normalized_json, '$.entity') as deputy_id,
    cast(json_extract_scalar(normalized_json, '$.year') as integer) as fiscal_year,
    cast(json_extract_scalar(normalized_json, '$.month') as integer) as reference_month,
    json_extract_scalar(normalized_json, '$.document') as document_id,
    json_extract_scalar(normalized_json, '$.category') as expense_category,
    cast(json_extract_scalar(normalized_json, '$.gross') as decimal(20,6)) as gross,
    cast(json_extract_scalar(normalized_json, '$.deductions') as decimal(20,6)) as deductions,
    cast(json_extract_scalar(normalized_json, '$.reimbursed') as decimal(20,6)) as reimbursed
from {{ ref('current_observation') }} where resource = 'camara_despesas'
