from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pendulum


default_args = {
    'owner': 'vu',
    'retries':5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='postgres_quarterly_dag',
    description='',
    start_date=pendulum.yesterday(),
    # start_date=datetime(2022, 12, 6, 23),
    schedule_interval='@once'
) as dag:
    task1 = BashOperator(
        task_id='Start',
        bash_command="Starting Calculation"
    )
    task2 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'postgres_default',
        sql = ["""
            CREATE TABLE IF NOT EXISTS quarterly_statistics as (
                SELECT
                    i.ticker, i.year, i.quarter, i.revenue, i.cost_of_good_sold, i.gross_profit, i.operation_expense, i.operation_income, i.interest_expense, i.pre_tax_profit, i.post_tax_profit, i.ebitda, 
                    b.short_asset, b.long_asset, b.debt, b.equity, b.short_invest, b.short_receivable, b.inventory, b.fixed_asset, b.asset, b.un_distributed_income,
                    c.invest_cost, c.from_invest, c.from_financial, c.from_sale, c.free_cash_flow 
                FROM income_statement i
                JOIN balance_sheet b
                    ON i.ticker= b.ticker
                    AND i.year = b.year
                    AND i.quarter = b.quarter
                JOIN cash_flow c
                    ON i.ticker= c.ticker
                    AND i.year = c.year
                    AND i.quarter = c.quarter
                    );
        """,
        """ALTER TABLE quarterly_statistics ADD CONSTRAINT quarterly_statistics_pk PRIMARY KEY (ticker, year, quarter);"""]
    )
    task1 >> task2