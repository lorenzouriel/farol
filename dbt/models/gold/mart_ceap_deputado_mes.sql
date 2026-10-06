select source, deputy_id, fiscal_year, reference_month,
       sum(gross) as gross, sum(deductions) as deductions, sum(reimbursed) as reimbursed,
       count(*) as source_rows, max(extracted_at) as extracted_at, max(run_id) as run_id
from {{ ref('fct_ceap_reembolso') }}
group by source, deputy_id, fiscal_year, reference_month
