
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from vnstock import *
import pendulum
from math import *
import pandas as pd
import numpy as np  

default_args = {
'owner': 'jazzdung',
'retries':5,
'retry_delay': timedelta(minutes=20)
}


full_indicator = pd.read_csv("/opt/airflow/data/full_indicator.csv")

def equation_calculator(df, eq, name):

    #calculate equation, just to save result on 
    result = df.eval(eq)
    result = result.to_frame()
    result.rename(columns={0: 'result'}, inplace=True)
    result.head()
    
    #Write result to csv file (Just for now)
    result.to_csv('/opt/airflow/data/' + name + '.csv', sep=',', encoding='utf-8')

    return result

with DAG(
    dag_id='demo_equation',
    description='demo_equation',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 2-12/3 *',
    catchup=True
) as dag:

    task1 = PythonOperator(
        task_id = 'equation_calculator',
        python_callable = equation_calculator,
        op_kwargs={
            'df': 'full_indicator',
            'eq': 'fromFinancial + fromSale + fromInvest',
            'name': 'demo_equation'
        }
    )

    task1

