with source as (
    select *
    from read_parquet('s3://farol-raw/raw/parlamentares/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(IdentificacaoParlamentar.CodigoParlamentar as bigint) as codigo_parlamentar,
        cast(nome as varchar) as nome,
        cast(sigla_partido as varchar) as sigla_partido,
        cast(sigla_uf as varchar) as sigla_uf,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
