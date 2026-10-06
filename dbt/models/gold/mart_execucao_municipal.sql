-- Cancellations are a separate source event; no inferred netting against commitments.
select source, municipality, organization, fiscal_year, reference_month,
       expense_stage, measure_basis, sum(amount) as amount,
       count(*) as source_rows, max(extracted_at) as extracted_at,
       max(run_id) as run_id, max(partition_key) as partition_key
from {{ ref('fct_execucao_municipal') }}
group by source, municipality, organization, fiscal_year, reference_month, expense_stage, measure_basis
