with source as (
    select *
    from read_parquet('s3://farol-raw/raw/deputados/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(id as bigint) as id_deputado,
        cast(nome as varchar) as nome_civil,
        cast(nome_eleitoral as varchar) as nome_eleitoral,
        cast(cpf as varchar) as cpf,
        cast(sigla_partido as varchar) as sigla_partido,
        cast(sigla_uf as varchar) as sigla_uf,
        cast(id_legislatura as bigint) as id_legislatura,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
