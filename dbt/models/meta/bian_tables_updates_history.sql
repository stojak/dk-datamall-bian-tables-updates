SELECT
    table_schema,
    table_name,
    table_update,
    row_count
FROM
    {{ source('meta','bian_tables_updates_history') }}
