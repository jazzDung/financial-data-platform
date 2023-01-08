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
    cash_flow = financial_flow ('AAA', 'cashflow' ,'quarterly')
    cash_flow.reset_index(inplace=True)
    cash_flow = cash_flow.rename(columns = {'index':'switch'})
    cash_flow[['year','quarter']] = cash_flow.switch.str.split("-",expand=True)
    cash_flow = cash_flow.drop('switch', axis=1)
    cash_flow['quarter'] = cash_flow['quarter'].str[1:]
    cash_flow = cash_flow.set_index(['ticker','year','quarter'])
    cash_flow.drop(cash_flow.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            quarterly_cash_flow = financial_flow (ticker, 'cashflow' ,'quarterly')
            yearly_cash_flow = financial_flow (ticker, 'cashflow' ,'yearly')

            single_cash_flow = pd.concat([quarterly_cash_flow, yearly_cash_flow])
            single_cash_flow.reset_index(inplace=True)
            single_cash_flow = single_cash_flow.rename(columns = {'index':'switch'})
            single_cash_flow[['year','quarter']] = single_cash_flow.switch.str.split("-",expand=True)
            single_cash_flow = single_cash_flow.drop('switch', axis=1)
            single_cash_flow['quarter'] = single_cash_flow['quarter'].str[1:]
            single_cash_flow = single_cash_flow.set_index(['ticker','year','quarter'])
            cash_flow = pd.concat([cash_flow, single_cash_flow])
        except Exception: 
            pass    

    #Drop duplicates
    cash_flow = cash_flow[~cash_flow.index.duplicated(keep='first')]
    #Sort data
    cash_flow = cash_flow.sort_values(by=['year','quarter','ticker'], ascending=False)
    #Export to csv
    cash_flow.to_csv('/opt/airflow/data/Cash Flow.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Cash Flow.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('cash_flow', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='cash_flow_v1',
    description='Import to cash flow table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 1-12/3 *',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table cash_flow cascade;
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