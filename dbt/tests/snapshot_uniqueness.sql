select observation_id from {{ ref('current_observation') }}
group by observation_id having count(*) > 1
