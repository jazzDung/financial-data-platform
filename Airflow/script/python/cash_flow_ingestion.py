import pandas as pd
from vnstock import *
from pathlib import Path

def data_to_csv():
    tickers = Path("/opt/airflow/data/ticker.txt").read_text().split("', '")

    cash_flow = financial_flow ('AAA', 'cashflow' ,'quarterly')
    cash_flow.reset_index(inplace=True)v
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
    cash_flow.to_csv('/opt/airflow/data/Cash Flow.csv', sep=',', encoding='utf-8')

def main():
    data_to_csv() 

if __name__ == '__main__':
    main()