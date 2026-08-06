with source as (
    select *
    from read_parquet('s3://farol-raw/raw/processos/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(numero_processo as varchar) as numero_processo,
        cast(classe_processual as varchar) as classe_processual,
        cast(orgao_julgador as varchar) as orgao_julgador,
        coalesce(cast(status_processual as varchar), 'desconhecido') as status_processual,
        coalesce(cast(instancia as varchar), 'desconhecido') as instancia,
        cast(nome_parte as varchar) as nome_parte,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
