-- Annual source snapshots, not a sum across retrieval dates.
select * from {{ ref('fct_execucao_orgao') }}
