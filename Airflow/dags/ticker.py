from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from vnstock import *
import pendulum



default_args = {
    'owner': 'jazzdung',
    'retries':5,
    'retry_delay': timedelta(minutes=20)
}

def get_data():
    #Get the company list, which contain the tickers
    company_list = listing_companies()

    #Sort in alphabetical order
    tickers = company_list["ticker"].sort_values().values.tolist()

    #Remove weird ticker (Not 3 characters)
    tickers = list(filter(lambda item: len(item) == 3, tickers))
    
    #Make sure all ticker are uppercase
    [ticker.upper() for ticker in tickers]
            
    return tickers

def data_to_txt():
    #Get ticker list
    ticker = get_data()

    #Get the first 10 ticker for demo purpose
    ticker = str(ticker[:10])[1:-1]

    #Write to txt file
    with open("/opt/airflow/data/ticker/ticker.txt", "w+") as outfile:
        outfile.write(ticker)

    #Noti!
    print("Save ticker successfully!")

with DAG(
    dag_id='ticker_list',
    description='Get ticker list',
    start_date=pendulum.yesterday(),
    schedule_interval='0 9 * * *',
    catchup=True
) as dag:
    task1 = PythonOperator(
        task_id = 'ticker_to_txt',
        python_callable = data_to_txt
    )
    
    task1