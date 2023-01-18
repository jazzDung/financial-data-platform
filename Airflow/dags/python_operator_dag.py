from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}


def greet(lmao, ti):
    first_name = ti.xcom_pull(task_ids='get_info', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_info', key='last_name')
    age = ti.xcom_pull(task_ids='get_info', key='age')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")


def get_info(ti):
    ti.xcom_push(key = 'first_name', value = 'Dung')
    ti.xcom_push(key = 'last_name', value = 'jazz')
    ti.xcom_push(key = 'age', value = 21)




with DAG(
    dag_id='python_operator_dag_v6',
    description='test dag using python operator',
    start_date=pendulum.yesterday(),
    # start_date=datetime(2022, 12, 6, 23),
    schedule_interval='@once'
) as dag:
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable = greet,
        op_kwargs={'lmao':'lmao'}
    )

    task2 = PythonOperator(
        task_id = 'get_info',
        python_callable = get_info
    )

    task2 >> task1