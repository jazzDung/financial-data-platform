from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from pyspark.sql import SparkSession
from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row
    
default_args = {'owner': 'airflow','start_date': datetime(2023, 1, 1),}


with DAG(
    dag_id='spark',
    description='spark_test',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily'
) as dag:

    spark_job = SparkSubmitOperator(task_id = "spark_job",
                                    application = "spark-app.py",
                                    conn_id = "spark_default",
                                    dag = dag)