import datetime

from pathlib import PurePath
from pendulum import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook
from airflow.utils.task_group import TaskGroup


def task_fail_slack_alert(context):
    slack_msg = f"""
            :spock-hand: dag_failed
            *dag*: {context.get('task_instance').dag_id}
            *task*: {context.get('task_instance').task_id}
            *hostname*: {context.get('task_instance').hostname}
            *execution_time*: {context.get('execution_date')}
            *logs*: {context.get('task_instance').log_url}
            """
    hook = SlackWebhookHook(slack_webhook_conn_id="slack_datamall")
    return hook.send_text(text=slack_msg)


env = {'SF_ACCOUNT': '{{ conn.snowflake_datamall.extra_dejson.account }}.{{ conn.snowflake_datamall.extra_dejson.region }}',
       'SF_DATABASE': '{{ conn.snowflake_datamall.extra_dejson.database }}',
       'SF_ROLE': '{{ conn.snowflake_datamall.extra_dejson.role }}',
       'SF_USER': '{{ conn.snowflake_datamall.login }}',
       'SF_PASSWORD': '{{ conn.snowflake_datamall.password }}',
       'SF_WAREHOUSE': '{{ conn.snowflake_datamall.extra_dejson.warehouse }}',
       'SF_SCHEMA': '{{ conn.snowflake_datamall.schema }}',
       'DAG_PATH': PurePath(__file__).parent,
       'DAG_FOLDER': PurePath(__file__).parent.name
       }

args = {
    'retries': 1,
    'owner': 'datadk',
    'on_failure_callback': task_fail_slack_alert
    }

with DAG(
    "webtool",
    start_date=datetime(2023, 7, 24),
    description="DAG (triggered by import_webtool DAG) loads Webtool tables: from base to work and work - finance schemas.",
    catchup=False,
    default_args=args,
    schedule_interval=None,
    tags=["datamall"]
) as dag:
    
    with TaskGroup(group_id='run_dbt') as RunDBT:
        
        run_dbt_datamall_work = BashOperator(
            task_id='run_dbt_datamall_work',
            bash_command="rm -rf /tmp/$DAG_FOLDER;\
                          cp -r $DAG_PATH /tmp/$DAG_FOLDER;\
                          $DBT_VENV_PATH_1_5/bin/dbt run --select snowflake_datamall_work.* --project-dir /tmp/$DAG_FOLDER/dbt --profiles-dir /tmp/$DAG_FOLDER/dbt",
            env=env,
            append_env=True,
            dag=dag,
            )

        run_dbt_datamall_finance = BashOperator(
            task_id='run_dbt_datamall_finance',
            bash_command="rm -rf /tmp/$DAG_FOLDER;\
                          cp -r $DAG_PATH /tmp/$DAG_FOLDER;\
                          $DBT_VENV_PATH_1_5/bin/dbt run --select snowflake_datamall_finance.* --project-dir /tmp/$DAG_FOLDER/dbt --profiles-dir /tmp/$DAG_FOLDER/dbt",
            env=env,
            append_env=True,
            dag=dag,
            )
        
        run_dbt_datamall_work >> run_dbt_datamall_finance

        RunDBT
