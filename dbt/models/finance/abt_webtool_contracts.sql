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
FROM {{ ref('webtool_work_contracts') }}
