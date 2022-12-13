from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pendulum


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_operator_dag_v1',
    description='test dag using postgres operator',
    start_date=pendulum.yesterday(),
    # start_date=datetime(2022, 12, 6, 23),
    schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'financial_database',
        sql = """
            create table if not exists dag_demo_table (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )
    task1