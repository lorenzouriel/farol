{% test requires_cutoff_flag(model) %}
    select *
    from {{ model }}
    where janela_fechada is null
{% endtest %}
