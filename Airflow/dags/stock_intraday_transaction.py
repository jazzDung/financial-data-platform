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
    'retries': 5,
    'retry_delay': timedelta(minutes=20)
}


def data_to_csv():

    #Get list of ticker
    tickers = Path("/opt/airflow/data/ticker.txt").read_text().split("', '")

    #Create blank dataframe with columns
    today_stock_data = stock_intraday_data(symbol='ACB', page_num=0, page_size=5000)
    today_stock_data['timeStamp'] = datetime.datetime.today().strftime('%Y-%m-%d') + " " + today_stock_data['time'].astype(str)
    today_stock_data['ticker'] = 'ACB'
    today_stock_data = today_stock_data.drop(['time'], axis =1 )
    today_stock_data.drop(today_stock_data.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            single_stock_data =  stock_intraday_data(symbol=ticker, page_num=0, page_size=1000)
            single_stock_data['timeStamp'] = datetime.datetime.today().strftime('%Y-%m-%d') + " " + single_stock_data['time'].astype(str)
            single_stock_data['ticker'] = ticker
            single_stock_data = single_stock_data.drop(['time'], axis =1 )
            today_stock_data = pd.concat([today_stock_data, single_stock_data])
        except Exception: 
            pass    

    #Create new index columns, since 2 identical transaction can occur
    today_stock_data = today_stock_data.reset_index(drop=True)
    today_stock_data.index = range(0, len(today_stock_data))

    #Export to csv
    today_stock_data.to_csv('/opt/airflow/data/Stock Intraday Transaction.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Stock Intraday Transaction.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('stock_intraday_transaction', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='stock_intraday_transaction',
    description='Import to Stock Intraday Transaction table',
    start_date=pendulum.yesterday(),
    schedule_interval='@daily',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table stock_intraday_transaction cascade;
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