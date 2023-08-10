SELECT
    id,
    user_id,
    start_date,
    end_date,
    months,
    contract_type,
    sim_count,
    sim_price,
    created,
    active,
    pool_amount,
    comment
FROM
    {{ source('base','import_webtool_base_contracts') }}
