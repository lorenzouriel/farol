{{
    config(
        materialized='incremental',
        unique_key=['id_deputado', 'ano_mes'],
        incremental_strategy='merge',
        tags=['daily', 'ceap']
    )
}}

with despesas as (
    select *
    from {{ ref('stg_ceap__despesas') }}
    {% if is_incremental() %}
    where _extracted_at > (select max(_extracted_at) from {{ this }})
    {% endif %}
),

cutoff as (
    select current_date - interval '90 days' as cutoff_date
)

select
    d.id_deputado,
    date_trunc('month', d.data_documento) as ano_mes,
    sum(d.valor_liquido) as total_gasto,
    (date_trunc('month', d.data_documento) < date_trunc('month', c.cutoff_date)) as janela_fechada,
    max(d._source_url) as source_url,
    max(d._extracted_at) as extracted_at,
    max(d._source_version) as source_version
from despesas d
cross join cutoff c
group by 1, 2, c.cutoff_date
