with a as (
    select run_id, expense_stage, sum(amount) as total
    from {{ ref('fct_execucao_municipal') }} group by run_id, expense_stage
), b as (
    select run_id, expense_stage, sum(amount) as total
    from {{ ref('mart_execucao_municipal') }} group by run_id, expense_stage
)
select coalesce(a.run_id,b.run_id) as run_id from a full outer join b
on a.run_id=b.run_id and a.expense_stage=b.expense_stage
where a.total is distinct from b.total
