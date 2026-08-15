with source as (
    select *
    from read_parquet('s3://farol-raw/raw/despesas/**/*.parquet', union_by_name=true)
),

renamed as (
    select
        cast(nu_deputado_id as bigint) as id_deputado,
        cast(txt_fornecedor as varchar) as nome_fornecedor,
        cast(txt_cnpjcpf as varchar) as cnpj_cpf_fornecedor,
        cast(ide_documento as varchar) as num_documento,
        cast(vlr_liquido as decimal(12,2)) as valor_liquido,
        cast(dat_emissao as date) as data_documento,
        cast(num_ano as integer) as ano,
        cast(num_mes as integer) as mes,
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
