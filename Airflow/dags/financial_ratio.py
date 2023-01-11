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
    all_financial_ratio = financial_ratio('AAA', 'quarterly', True)
    all_financial_ratio = all_financial_ratio.set_index(['ticker','year','quarter'])
    all_financial_ratio.drop(all_financial_ratio.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            quarterly_financial_ratio = financial_ratio(ticker, 'quarterly', True)
            yearly_financial_ratio = financial_ratio (ticker, 'yearly', True)

            single_financial_ratio = pd.concat([quarterly_financial_ratio, yearly_financial_ratio])
            single_financial_ratio = single_financial_ratio.set_index(['ticker','year','quarter'])
            all_financial_ratio = pd.concat([all_financial_ratio, single_financial_ratio])
        except Exception: 
            pass    

    #Drop duplicates
    all_financial_ratio = all_financial_ratio[~all_financial_ratio.index.duplicated(keep='first')]
    #Sort data
    all_financial_ratio = all_financial_ratio.sort_values(by=['year','quarter','ticker'], ascending=False)
    all_financial_ratio.reset_index(inplace=True)
    #Export to csv
    all_financial_ratio.to_csv('/opt/airflow/data/Financial Ratio.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Financial Ratio.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('financial_ratio', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='financial_ratio',
    description='Import to financial ratio table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 2-12/3 *',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table financial_ratio cascade;
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