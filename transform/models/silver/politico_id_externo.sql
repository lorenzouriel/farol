{{
    config(
        materialized='table',
        tags=['daily', 'politico', 'identity']
    )
}}

with camara as (
    select
        'camara' as fonte,
        cast(id_deputado as varchar) as id_externo,
        cpf,
        _source_url as source_url,
        _extracted_at as extracted_at,
        _source_version as source_version
    from {{ ref('stg_camara__deputados') }}
    where cpf is not null
),

tse as (
    select
        'tse' as fonte,
        cast(sq_candidato as varchar) as id_externo,
        cpf,
        _source_url as source_url,
        _extracted_at as extracted_at,
        _source_version as source_version
    from {{ ref('stg_tse__candidatos') }}
    where cpf is not null
),

unioned as (
    select * from camara
    union all
    select * from tse
)

select
    md5(fonte || id_externo) as politico_id_externo_sk,
    cpf,
    fonte,
    id_externo,
    extracted_at as valid_from,
    cast('9999-12-31' as timestamp) as valid_to,
    true as is_current,
    source_url,
    extracted_at,
    source_version
from unioned
