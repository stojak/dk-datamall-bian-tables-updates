SELECT
    table_schema,
    table_name,
    last_update,
    row_count
FROM
    {{ source('meta','v_bian_tables_updates') }}
