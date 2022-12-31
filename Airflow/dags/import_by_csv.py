from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
from vnstock import *
import pandas as pd
import pendulum
import psycopg2
import psycopg2.extras as extras
from sqlalchemy import create_engine


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

def get_ticker_list():
    company_list = listing_companies()
    tickers = company_list["ticker"].sort_values().values.tolist()
    for ticker in tickers:
        if len(ticker) > 3:
            tickers.remove(ticker)
    return tickers[:10]

def get_cash_flow():
    tickers = get_ticker_list()

    cash_flow = financial_flow ('AAA', 'cashflow' ,'quarterly')
    cash_flow.reset_index(inplace=True)
    cash_flow = cash_flow.rename(columns = {'index':'switch'})
    cash_flow[['year','quarter']] = cash_flow.switch.str.split("-",expand=True)
    cash_flow = cash_flow.drop('switch', axis=1)
    cash_flow['quarter'] = cash_flow['quarter'].str[1:]
    cash_flow = cash_flow.set_index(['ticker','year','quarter'])
    cash_flow.drop(cash_flow.index, inplace=True)

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


    cash_flow = cash_flow[~cash_flow.index.duplicated(keep='first')]
    cash_flow = cash_flow.sort_values(by=['year','quarter','ticker'], ascending=False)
    cash_flow.to_csv('/opt/airflow/data/cash_flow.csv', sep=',', encoding='utf-8')

def import_data():
    data = pd.read_csv('/opt/airflow/data/cash_flow.csv')
    
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    data.to_sql('test_table', con=conn, if_exists='replace', index=True)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True

    conn.close()


with DAG(
    dag_id='import_through_csv_v1',
    description='create new table and import data',
    start_date=pendulum.yesterday(),
    # start_date=datetime(2022, 12, 6, 23),
    schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'financial_database',
        sql = """
            CREATE TABLE IF NOT EXISTS test_table (
                ticker varchar(3),
                year integer,
                quarter integer,
                invest_cost integer,
                from_invest integer,
                from_financial integer,
                from_sale integer,
                free_cash_flow double precision,
                PRIMARY KEY (ticker, year, quarter),
                FOREIGN KEY (ticker) REFERENCES listing_companies (ticker)
            );
        """
    )

    task2 = PythonOperator(
        task_id = 'get_cash_flow_data',
        python_callable = get_cash_flow
    )

    task3 = PythonOperator(
        task_id = 'import_cash_flow_data',
        python_callable = import_data
    )

    task1 >> task2 >> task3