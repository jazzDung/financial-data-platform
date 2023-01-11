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
    current_time = datetime.datetime.now()
    start_date = str(current_time.year - 1) + '-' + str(current_time.month) + '-' + str(current_time.day)
    end_date = str(current_time.year) + '-' + str(current_time.month) + '-' + str(current_time.day)

    stock_history = stock_historical_data(symbol='AAA', start_date=start_date, end_date=end_date)
    stock_history['ticker'] = 'AAA'
    stock_history['timeStamp'] = stock_history['TradingDate'].astype(str) + " 00:00:00"
    stock_history.drop(stock_history.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            single_stock =  stock_historical_data(symbol=ticker, start_date=start_date, end_date=end_date)
            single_stock['timeStamp'] = single_stock['TradingDate'].astype(str) + " 00:00:00"
            single_stock['ticker'] = ticker
            stock_history = pd.concat([stock_history, single_stock])
        except Exception:
            pass

    stock_history = stock_history[['ticker', 'timeStamp', 'Open', 'High', 'Low', 'Close', 'Volume']]
    #Drop duplicates
    stock_history = stock_history[~stock_history.duplicated(subset=['ticker', 'timeStamp'], keep='first')]
    #Sort data
    stock_history = stock_history.sort_values(by=['ticker', 'timeStamp'])
    #Export to csv
    stock_history.to_csv('/opt/airflow/data/Stock History.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Stock History.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('stock_history', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='stock_history',
    description='Import to stock history table',
    start_date=pendulum.yesterday(),
    schedule_interval='@daily',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table stock_history cascade;
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