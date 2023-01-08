from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=20)
}

with DAG(
    dag_id='import_data_from_python_script',
    description='Import to test table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 1-12/3 *',
    catchup=True
) as dag:

    task1 = BashOperator(
        task_id='data_to_csv',
        bash_command='python /opt/airflow/script/python/cash_flow_ingestion.py'
    )

    task2 = BashOperator(
        task_id='data_to_db',
        bash_command='python /opt/airflow/script/python/cash_flow_to_db.py'
    )

    task1>>task2