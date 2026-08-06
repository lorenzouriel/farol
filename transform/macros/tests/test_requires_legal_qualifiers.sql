{% test requires_legal_qualifiers(model) %}
    select *
    from {{ model }}
    where status_processual is null or instancia is null
{% endtest %}
