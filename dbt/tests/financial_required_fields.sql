select observation_id from {{ ref('fct_execucao_orgao') }}
where entity_id is null or fiscal_year is null or committed is null or liquidated is null or paid is null
union all
select observation_id from {{ ref('fct_execucao_municipal') }}
where amount is null or expense_stage not in ('committed','liquidated','paid','cancellation_unspecified')
union all
select observation_id from {{ ref('fct_demonstrativo_fiscal') }}
where amount is null or not (
    (statement_type='RREO' and annex='RREO-Anexo 01' and statement_column like 'DESPESAS %')
    or (statement_type='RGF' and annex='RGF-Anexo 01' and measure_basis='rolling_12_months')
    or (statement_type='DCA' and annex='DCA-Anexo I-D' and statement_column like 'Despesas %')
)
