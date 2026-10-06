-- No payment measure: an invoice is not evidence of payment.
select * from {{ ref('fct_contrato_fatura') }}
