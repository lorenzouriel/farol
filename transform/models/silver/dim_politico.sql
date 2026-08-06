{{
    config(
        materialized='table',
        tags=['daily', 'politico', 'identity']
    )
}}

with camara as (
    select
        cpf,
        nome_civil,
        nome_eleitoral,
        sigla_partido,
        sigla_uf,
        _source_url as source_url,
        _extracted_at as extracted_at,
        _source_version as source_version
    from {{ ref('stg_camara__deputados') }}
    where cpf is not null
),

tse_only as (
    select
        t.cpf,
        t.nome as nome_civil,
        t.nome as nome_eleitoral,
        null as sigla_partido,
        null as sigla_uf,
        t._source_url as source_url,
        t._extracted_at as extracted_at,
        t._source_version as source_version
    from {{ ref('stg_tse__candidatos') }} t
    left join camara c on c.cpf = t.cpf
    where t.cpf is not null
      and c.cpf is null
),

unioned as (
    select * from camara
    union all
    select * from tse_only
),

deduped as (
    select
        *,
        row_number() over (partition by cpf order by extracted_at desc) as row_num
    from unioned
)

select
    md5(cpf) as politico_sk,
    cpf,
    nome_civil,
    nome_eleitoral,
    sigla_partido,
    sigla_uf,
    source_url,
    extracted_at,
    source_version
from deduped
where row_num = 1
