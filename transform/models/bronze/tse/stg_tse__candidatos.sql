with source as (
    select *
    from read_parquet('s3://farol-raw/raw/candidatos/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(sq_candidato as bigint) as sq_candidato,
        cast(nr_cpf_candidato as varchar) as cpf,
        cast(nm_candidato as varchar) as nome,
        cast(ds_cargo as varchar) as cargo,
        cast(ds_situacao_candidatura as varchar) as situacao,
        cast(ano_eleicao as integer) as ano_eleicao,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
)

select * from renamed
