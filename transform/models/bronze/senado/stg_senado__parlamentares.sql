with source as (
    select *
    from read_parquet('s3://farol-raw/raw/parlamentares/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(identificacao_parlamentar__codigo_parlamentar as bigint) as codigo_parlamentar,
        cast(identificacao_parlamentar__nome_parlamentar as varchar) as nome,
        cast(identificacao_parlamentar__sigla_partido_parlamentar as varchar) as sigla_partido,
        cast(identificacao_parlamentar__uf_parlamentar as varchar) as sigla_uf,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
