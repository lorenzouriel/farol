select count(*) as capability_count from {{ ref('mart_cobertura_fontes') }} having count(*) <> 42
