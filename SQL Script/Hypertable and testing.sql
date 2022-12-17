-- add timescaledb to project
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- create hypertable from postgresql table
SELECT create_hypertable('stock_history','time_stamp', migrate_data => true);
SELECT create_hypertable('stock_intraday_transaction','time_stamp');

-- manual data compression
--ALTER TABLE stock_history SET (
--  timescaledb.compress,
--  timescaledb.compress_orderby = 'time_stamp DESC',
--  timescaledb.compress_segmentby = 'ticker'
--);
--
-- auto data compression
--SELECT add_compression_policy('stock_history', INTERVAL '2 weeks');
--SELECT add_compression_policy('stock_history', INTERVAL '0 day');
--
-- remove compression
--ALTER TABLE stock_history SET (timescaledb.compress=false);
--SELECT remove_compression_policy('stock_history');
--SELECT remove_compression_policy('stock_intraday_transaction');
--
-- verify compression
--SELECT * FROM timescaledb_information.compression_settings;
--
--SELECT 
--	pg_size_pretty(before_compression_total_bytes) as "before compression",
--  	pg_size_pretty(after_compression_total_bytes) as "after compression"
--  	FROM hypertable_compression_stats('stock_history');
--  
 
 
 