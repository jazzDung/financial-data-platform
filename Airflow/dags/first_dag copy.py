from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pendulum


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag_v6',
    description='first demo dag',
    start_date=pendulum.yesterday(),
    # start_date=datetime(2022, 12, 6, 23),
    schedule_interval='@once'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo hello world, lmao yeet"
    )

    task2 = BashOperator(
        task_id='2nd_task',
        bash_command="will run after task1"
    )

    task3 = BashOperator(
        task_id='3rd_task',
        bash_command="will run after task1, run with task2"
    )

    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    # task1 >> task2
    # task1 >> task3

    task1 >> [task2, task3]