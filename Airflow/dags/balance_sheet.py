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
    balance_sheet = financial_flow ('AAA', 'balancesheet' ,'quarterly')
    balance_sheet.reset_index(inplace=True)
    balance_sheet = balance_sheet.rename(columns = {'index':'switch'})
    balance_sheet[['year','quarter']] = balance_sheet.switch.str.split("-",expand=True)
    balance_sheet = balance_sheet.drop('switch', axis=1)
    balance_sheet['quarter'] = balance_sheet['quarter'].str[1:]
    balance_sheet = balance_sheet.set_index(['ticker','year','quarter'])
    balance_sheet.drop(balance_sheet.index, inplace=True)

    #Get data for each ticker and append to the dataframe
    for ticker in tickers:
        try:
            quarterly_balance_sheet = financial_flow (ticker, 'balancesheet' ,'quarterly')
            yearly_balance_sheet = financial_flow (ticker, 'balancesheet' ,'yearly')

            single_balance_sheet = pd.concat([quarterly_balance_sheet, yearly_balance_sheet])
            single_balance_sheet.reset_index(inplace=True)
            single_balance_sheet = single_balance_sheet.rename(columns = {'index':'switch'})
            single_balance_sheet[['year','quarter']] = single_balance_sheet.switch.str.split("-",expand=True)
            single_balance_sheet = single_balance_sheet.drop('switch', axis=1)
            single_balance_sheet['quarter'] = single_balance_sheet['quarter'].str[1:]
            single_balance_sheet = single_balance_sheet.set_index(['ticker','year','quarter'])
            balance_sheet = pd.concat([balance_sheet, single_balance_sheet])
        except Exception: 
            pass    

    #Drop duplicates
    balance_sheet = balance_sheet[~balance_sheet.index.duplicated(keep='first')]
    #Sort data
    balance_sheet = balance_sheet.sort_values(by=['year','quarter','ticker'], ascending=False)
    balance_sheet.reset_index(inplace=True)
    #Export to csv
    balance_sheet.to_csv('/opt/airflow/data/Balance Sheet.csv', sep=',', encoding='utf-8')


def csv_to_db():

    #Csv to dataframe
    data = pd.read_csv('/opt/airflow/data/Balance Sheet.csv')

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    #Import dataframe to table
    data.to_sql('balance_sheet', con=conn, if_exists='replace', index=True)
    conn.close()


with DAG(
    dag_id='balance_sheet',
    description='Import to balance sheet table',
    start_date=pendulum.yesterday(),
    schedule_interval='0 10 1 2-12/3 *',
    catchup=True
) as dag:

    #Truncate table to avoid duplicates
    task1 = PostgresOperator(
        task_id = 'truncate_table',
        postgres_conn_id = 'financial_database',
        sql = """
            TRUNCATE table balance_sheet cascade;
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