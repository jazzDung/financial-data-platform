from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import inspect
import pandas.io.sql as sqlio

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Full data on csv, just for demos

# full_indicator = pd.DataFrame

@app.before_first_request
def get_full_indicator():
    full_indicator = pd.read_csv("/app/data/full_indicator.csv")
    print("Get data successfully!")
    return full_indicator
full_indicator = get_full_indicator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ['POST'])
def submit():

    print(len(full_indicator))

    if request.method == 'POST':
        equation_name = request.form['equation_name']
        equation = request.form['equation']
        query = request.form['query']

        if equation != '':
            
            try:
                #Calulate equation to display
                result = equation_calculator(full_indicator, equation, equation_name)
                html_table = result.to_html(classes='data', header="true")

                #Write DAG
                dag_generator(full_indicator, equation, equation_name, '0 10 1 2-12/3 *')
                return render_template('success.html', message = 'Result of: ' + equation_name, tables=[html_table])
            except Exception: 
                return render_template('index.html', message = 'Invalid equation') 
        

        elif query != '':
            try:
                result = run_query(query)
                html_table = result.to_html(classes='data', header="true")

                return render_template('success.html', message = 'Result of: ' + query, tables=[html_table])
            except Exception: 
                return render_template('index.html', message = 'Invalid query')

        else:
            return render_template('index.html', message = 'Please enter an equation or query')

@app.route('/home', methods = ['POST'])
def home():
    if request.method == 'POST':
        return render_template('index.html')

def run_query(query):
    
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    # db = create_engine(conn_string)
    # conn = db.connect()

    # df.to_sql('test_table', con=conn, if_exists='replace', index=True)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True

    sql = query
    result = sqlio.read_sql_query(sql, conn)

    conn.close()
    return result

def equation_calculator(df, eq, name):

    #calculate equation, just to save result on 
    result = df.eval(eq)
    result = result.to_frame()
    result.rename(columns={0: 'result'}, inplace=True)
    result.head()
    
    #Write result to csv file (Just for now)
    result.to_csv('/app/data/generated/' + name + '.csv', sep=',', encoding='utf-8')

    return result[0:10]

def dag_generator(df, eq, name, period):

    #Imports and default arguments
    script = f"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from vnstock import *
import pendulum
from math import *
import pandas as pd
import numpy as np  

default_args = {{
'owner': 'jazzdung',
'retries':5,
'retry_delay': timedelta(minutes=20)
}}


full_indicator = pd.read_csv("/opt/airflow/data/full_indicator.csv")

def equation_calculator(df, eq, name):

    #calculate equation, just to save result on 
    result = df.eval(eq)
    result = result.to_frame()
    result.rename(columns={{0: 'result'}}, inplace=True)
    result.head()
    
    #Write result to csv file (Just for now)
    result.to_csv('/opt/airflow/data/' + {'name'} + '.csv', sep=',', encoding='utf-8')

    return result

with DAG(
    dag_id='{name}',
    description='{name}',
    start_date=pendulum.yesterday(),
    schedule_interval='{period}',
    catchup=True
) as dag:

    task1 = PythonOperator(
        task_id = 'equation_calculator',
        python_callable = equation_calculator,
        op_kwargs={{
            'df': 'full_indicator',
            'eq': '{eq}',
            'name': '{name}'
        }}
    )

    task1

"""

    #Write to py file
    with open("/app/dags/" + name + ".py", "w+") as dag:
        dag.write(script)

    return script

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')