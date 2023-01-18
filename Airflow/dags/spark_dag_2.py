from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from pyspark.sql import SparkSession
from datetime import datetime, date
import pandas as pd
import os
from pyspark.sql import Row
    
default_args = {'owner': 'airflow','start_date': datetime(2023, 1, 1),}


with DAG(
    dag_id='spark_postgres_test',
    description='spark_test',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@once'
) as dag:
    path = os.getcwd()
    name = "spark_app_2.py"
    print(path)
    for root, dirs, files in os.walk(path):
        if name in files:
            app_path = (os.path.join(root, name))
            break

    spark_job = SparkSubmitOperator(task_id = "spark_job",
                                    application = app_path,
                                    conn_id = "spark_default",
                                    dag = dag)
    