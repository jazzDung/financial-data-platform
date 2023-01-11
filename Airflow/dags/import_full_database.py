from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from sqlalchemy import create_engine
from vnstock import *
import pandas as pd
import pendulum

"""
Why is this needed?
Import data DAGs are limited to 10 ticker for best performance
So run this DAG when you need to get full data back on the database
"""


default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=20)
}

def csv_to_db():

    #Connect to postgresql database
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    # #Listing companies
    # listing_companies = pd.read_csv('/opt/airflow/data/backup/Listing Companies.csv')
    # listing_companies.to_sql('listing_companies', con=conn, if_exists='replace', index=True)

    #Cash flow
    cash_flow = pd.read_csv('/opt/airflow/data/backup/Cash Flow.csv')
    cash_flow.to_sql('cash_flow', con=conn, if_exists='replace', index=True)

    #Stock history
    stock_history = pd.read_csv('/opt/airflow/data/backup/Stock History.csv')
    stock_history.to_sql('stock_history', con=conn, if_exists='replace', index=True)

    #Income statement
    income_statement = pd.read_csv('/opt/airflow/data/backup/Income Statement.csv')
    income_statement.to_sql('income_statement', con=conn, if_exists='replace', index=True)

    #Balance sheet
    balance_sheet = pd.read_csv('/opt/airflow/data/backup/Balance Sheet.csv')
    balance_sheet.to_sql('balance_sheet', con=conn, if_exists='replace', index=True)

    #Financial ratio
    financial_ratio = pd.read_csv('/opt/airflow/data/backup/Financial Ratio.csv')
    financial_ratio.to_sql('financial_ratio', con=conn, if_exists='replace', index=True)

    #Stock intraday transaction
    stock_intraday_transaction = pd.read_csv('/opt/airflow/data/backup/Stock Intraday Transaction.csv')
    stock_intraday_transaction.to_sql('stock_intraday_transaction', con=conn, if_exists='replace', index=True)

    #General rating
    general_rating = pd.read_csv('/opt/airflow/data/backup/General Rating.csv')
    general_rating.to_sql('general_rating', con=conn, if_exists='replace', index=True)

    #Business model rating
    business_model_rating = pd.read_csv('/opt/airflow/data/backup/Business Model Rating.csv')
    business_model_rating.to_sql('business_model_rating', con=conn, if_exists='replace', index=True)

    #Business operation rating
    business_operation_rating = pd.read_csv('/opt/airflow/data/backup/Business Operation Rating.csv')
    business_operation_rating.to_sql('business_operation_rating', con=conn, if_exists='replace', index=True)

    #Financial health rating
    financial_health_rating = pd.read_csv('/opt/airflow/data/backup/Financial Health Rating.csv')
    financial_health_rating.to_sql('financial_health_rating', con=conn, if_exists='replace', index=True)

    #Valuation rating
    valuation_rating = pd.read_csv('/opt/airflow/data/backup/Valuation Rating.csv')
    valuation_rating.to_sql('valuation_rating', con=conn, if_exists='replace', index=True)

    #Industry financial rating
    industry_financial_health = pd.read_csv('/opt/airflow/data/backup/Industry Financial Health.csv')
    industry_financial_health.to_sql('industry_financial_health', con=conn, if_exists='replace', index=True)

    conn.close()

with DAG(
    dag_id='import_full_database',
    description='Import all data to database',
    start_date=pendulum.yesterday(),
    schedule_interval=None,
    catchup=True
) as dag:

    task1 = PythonOperator(
        task_id = 'import_data',
        python_callable = csv_to_db
    )

    task1