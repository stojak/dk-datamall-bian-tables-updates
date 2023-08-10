SELECT
    id,
    customer_id,
    order_id,
    order_line_id,
    name,
    title,
    created,
    pool_before_transaction,
    total_price,
    subsidization,
    phone_number,
    comment,
    log_type,
    sap,
    supplier,
    invoice,
    contract_id
FROM {{ ref('webtool_work_transactionlog') }}
