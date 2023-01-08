from vnstock import *

def get_data():
    company_list = listing_companies()
    tickers = company_list["ticker"].sort_values().values.tolist()
    for ticker in tickers:
        if len(ticker) > 3:
            tickers.remove(ticker)
            
    return tickers

def data_to_txt():
    ticker = get_data()
    ticker_full = str(ticker)
    ticker_10 = str(ticker[:10])
    with open("/opt/airflow/data/ticker.txt", "w+") as outfile:
        outfile.write(ticker_full)

    with open("/opt/airflow/data/ticker_10.txt", "w+") as outfile:
        outfile.write(ticker_10)

    print("Save ticker successfully!")

def main():
    data_to_txt() 

if __name__ == '__main__':
    main()