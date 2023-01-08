import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Truncate table to avoid data duplication
def truncate_table():
    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()
    cursor = conn.cursor()

    sql1 = '''TRUNCATE table test_table cascade;'''
    cursor.execute(sql1)

    conn.commit()
    conn.close()

def csv_to_db():
    data = pd.read_csv('/opt/airflow/data/Cash Flow.csv')

    conn_string = 'postgresql://postgres:02092001@172.17.0.1:5432/financialDataPlatform'
    db = create_engine(conn_string)
    conn = db.connect()

    data.to_sql('test_table', con=conn, if_exists='replace', index=True)
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True

    conn.close()


def main():
    truncate_table()
    csv_to_db() 

if __name__ == '__main__':
    main()