from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import timedelta
from sqlalchemy import create_engine
from pathlib import Path
from vnstock import *
import pandas as pd
import pendulum

default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=20)
}


def data_to_csv():

    #Get list of ticker
    tickers = Path("/opt/airflow/data/ticker.txt").read_text().split("', '")

    #Create blank dataframe with columns
    all_stock_industry_financial_health = industry_financial_health('AAA')
    all_stock_industry_financial_health['ticker'] = 'AAA'
    all_stock_industry_financial_health = all_stock_industry_financial_health.set_index(['ticker'])
    all_stock_industry_financial_health.drop(all_stock_industry_financial_health.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            single_stock_industry_financial_health =  industry_financial_health(ticker)
            single_stock_industry_financial_health['ticker'] = ticker
            single_stock_industry_financial_health = single_stock_industry_financial_health.set_index(['ticker'])
            
            all_stock_industry_financial_health = pd.concat([all_stock_industry_financial_health, single_stock_industry_financial_health])
        except Exception: 
            pass      


    #Export to csv
    all_stock_industry_financial_health.to_csv('/opt/airflow/data/Industry Financial Health.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Industry Financial Health.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to tabsle
    data.to_sql('industry_financial_health', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='industry_financial_health_v1',
    description='Import to Industry Financial Health table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 2-12/3 *',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table industry_financial_health cascade;
        """
    )

    task2 = PythonOperator(
        task_id = 'data_to_csv',
        python_callable = data_to_csv
    )

    task3 = PythonOperator(
        task_id = 'import_data',
        python_callable = csv_to_db
    )

    task1>>task2>>task3