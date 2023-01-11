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
    all_stock_financial_health_rating = financial_health_rating('AAA')
    all_stock_financial_health_rating['ticker'] = 'AAA'
    all_stock_financial_health_rating = all_stock_financial_health_rating.set_index(['ticker'])
    all_stock_financial_health_rating.drop(all_stock_financial_health_rating.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            single_stock_financial_health_rating =  financial_health_rating(ticker)
            single_stock_financial_health_rating['ticker'] = ticker
            single_stock_financial_health_rating = single_stock_financial_health_rating.set_index(['ticker'])
            
            all_stock_financial_health_rating = pd.concat([all_stock_financial_health_rating, single_stock_financial_health_rating])
        except Exception: 
            pass    


    #Export to csv
    all_stock_financial_health_rating.to_csv('/opt/airflow/data/Financial Health Rating.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Financial Health Rating.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('financial_health_rating', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='financial_health_rating_v1',
    description='Import to Financial Health Rating table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 2-12/3 *',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table financial_health_rating cascade;
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