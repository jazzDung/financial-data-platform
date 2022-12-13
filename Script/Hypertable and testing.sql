CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT create_hypertable('stock_history','time_stamp');
SELECT create_hypertable('stock_intraday_transaction','time_stamp');

-- select * from listing_companies limit 100;
-- select * from stock_history limit 100;
-- select * from income_statement limit 100;
-- select * from balance_sheet limit 100;
-- select * from cash_flow limit 100;
-- select * from financial_ratio limit 100;
-- select * from stock_intraday_transaction limit 100;


-- \copy listing_companies
--FROM '/home/hadoop/Project III/Danh sách công ty/Listing Companies.csv'
--DELIMITER ','
--CSV HEADER;

-- \copy stock_history
--FROM '/home/hadoop/Project III/Tổng hợp/Stock History.csv'
--DELIMITER ','
--CSV HEADER;

--\copy income_statement
--FROM '/home/hadoop/Project III/Tổng hợp/Income Statement.csv'
--DELIMITER ','
--CSV HEADER;

--\copy balance_sheet
--FROM '/home/hadoop/Project III/Tổng hợp/Balance Sheet.csv'
--DELIMITER ','
--CSV HEADER;

--\copy cash_flow
--FROM '/home/hadoop/Project III/Tổng hợp/Cash Flow.csv'
--DELIMITER ','
--CSV HEADER;

--\copy financial_ratio
--FROM '/home/hadoop/Project III/Tổng hợp/Financial Ratio.csv'
--DELIMITER ','
--CSV HEADER;

--\copy financial_ratio
--FROM '/home/hadoop/Project III/Tổng hợp/Financial Ratio.csv'
--DELIMITER ','
--CSV HEADER;
