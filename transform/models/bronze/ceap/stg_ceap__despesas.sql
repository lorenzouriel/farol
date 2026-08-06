with source as (
    select *
    from read_parquet('s3://farol-raw/raw/despesas/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(id_deputado as bigint) as id_deputado,
        cast(nome_fornecedor as varchar) as nome_fornecedor,
        cast(cnpj_cpf_fornecedor as varchar) as cnpj_cpf_fornecedor,
        cast(num_documento as varchar) as num_documento,
        cast(valor_liquido as decimal(12,2)) as valor_liquido,
        cast(data_documento as date) as data_documento,
        cast(ano as integer) as ano,
        cast(mes as integer) as mes,
        cast(num_ressarcimento as varchar) as num_ressarcimento,
        _source_url,
        cast(_extracted_at as timestamp) as _extracted_at,
        _source_version
    from source
),

deduped as (
    select
        *,
        row_number() over (
            partition by id_deputado, num_documento
            order by _extracted_at desc
        ) as row_num
    from renamed
)

select
    id_deputado,
    nome_fornecedor,
    cnpj_cpf_fornecedor,
    num_documento,
    valor_liquido,
    data_documento,
    ano,
    mes,
    num_ressarcimento,
    _source_url,
    _extracted_at,
    _source_version
from deduped
where row_num = 1
