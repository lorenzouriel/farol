-- Hierarchical statement cells must not be summed across account levels.
select * from {{ ref('fct_demonstrativo_fiscal') }}
