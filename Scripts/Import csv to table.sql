-- Run this in terminal, change file location


\copy listing_companies
FROM '/home/jazzdung/Project III/Formatted Data/Listing Companies.csv'
DELIMITER ','
CSV HEADER;

\copy stock_history
FROM '/home/jazzdung/Project III/Formatted Data/Stock History.csv'
DELIMITER ','
CSV HEADER;

\copy income_statement
FROM '/home/jazzdung/Project III/Formatted Data/Income Statement.csv'
DELIMITER ','
CSV HEADER;

\copy balance_sheet
FROM '/home/jazzdung/Project III/Formatted Data/Balance Sheet.csv'
DELIMITER ','
CSV HEADER;

\copy cash_flow
FROM '/home/jazzdung/Project III/Formatted Data/Cash Flow.csv'
DELIMITER ','
CSV HEADER;

\copy financial_ratio
FROM '/home/jazzdung/Project III/Formatted Data/Financial Ratio.csv'
DELIMITER ','
CSV HEADER;

\copy stock_intraday_transaction
FROM '/home/jazzdung/Project III/Formatted Data/Stock Intraday Transaction.csv'
DELIMITER ','
CSV HEADER;

\copy general_rating
FROM '/home/jazzdung/Project III/Formatted Data/General Rating.csv'
DELIMITER ','
CSV HEADER;

\copy business_model_rating
FROM '/home/jazzdung/Project III/Formatted Data/Business Model Rating.csv'
DELIMITER ','
CSV HEADER;

\copy business_operation_rating
FROM '/home/jazzdung/Project III/Formatted Data/Business Operation Rating.csv'
DELIMITER ','
CSV HEADER;

\copy financial_health_rating
FROM '/home/jazzdung/Project III/Formatted Data/Financial Health Rating.csv'
DELIMITER ','
CSV HEADER;

\copy valuation_rating
FROM '/home/jazzdung/Project III/Formatted Data/Valuation Rating.csv'
DELIMITER ','
CSV HEADER;

\copy industry_financial_health
FROM '/home/jazzdung/Project III/Formatted Data/Industry Financial Health.csv'
DELIMITER ','
CSV HEADER;
