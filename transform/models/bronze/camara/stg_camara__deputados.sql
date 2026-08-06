with source as (
    select *
    from read_parquet('s3://farol-raw/raw/deputados/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(id as bigint) as id_deputado,
        cast(nome as varchar) as nome_civil,
        cast(ultimoStatus.nomeEleitoral as varchar) as nome_eleitoral,
        cast(cpf as varchar) as cpf,
        cast(siglaPartido as varchar) as sigla_partido,
        cast(siglaUf as varchar) as sigla_uf,
        cast(idLegislatura as bigint) as id_legislatura,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
