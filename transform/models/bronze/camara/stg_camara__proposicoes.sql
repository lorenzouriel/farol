with source as (
    select *
    from read_parquet('s3://farol-raw/raw/proposicoes/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(id as bigint) as id_proposicao,
        cast(sigla_tipo as varchar) as sigla_tipo,
        cast(numero as integer) as numero,
        cast(ano as integer) as ano,
        cast(ementa as varchar) as ementa,
        cast(data_apresentacao as timestamp) as data_apresentacao,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
