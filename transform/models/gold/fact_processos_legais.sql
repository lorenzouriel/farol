{{
    config(
        materialized='table',
        tags=['daily', 'processos']
    )
}}

select
    numero_processo,
    nome_parte,
    classe_processual,
    orgao_julgador,
    status_processual,
    instancia,
    _source_url as source_url,
    _extracted_at as extracted_at,
    _source_version as source_version
from {{ ref('stg_datajud__processos') }}
