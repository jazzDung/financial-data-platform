--drop table if exists listingCompanies cascade;
--drop table if exists stockHistory cascade;
--drop table if exists incomeStatement cascade;
--drop table if exists balanceSheet cascade;
--drop table if exists cashFlow cascade;
--drop table if exists financialRatio cascade;
--drop table if exists stockIntradayTransaction cascade;

--drop table if exists generalRating cascade;
--drop table if exists businessModelRating cascade;
--drop table if exists businessOperationRating cascade;
--drop table if exists financialHealthRating cascade;
--drop table if exists valuationRating cascade;
--drop table if exists industryFinancialHealth cascade;

--truncate table listingCompanies cascade;
--truncate table stockHistory cascade;
--truncate table incomeStatement cascade;
--truncate table balanceSheet cascade;
--truncate table cashFlow cascade;
--truncate table financialRatio cascade;
--truncate table stockIntradayTransaction cascade;

--truncate table generalRating cascade;
--truncate table businessModelRating cascade;
--truncate table businessOperationRating cascade;
--truncate table financialHealthRating cascade;
--truncate table valuationRating cascade;
--truncate table industryFinancialHealth cascade;

-- alter table generalRating add constraint fkListingCompaniesGeneralRating foreign key (ticker) references listingCompanies (ticker);
-- alter table businessModelRating add constraint fkListingCompaniesBusinessModelRating foreign key (ticker) references listingCompanies (ticker);
-- alter table businessOperationRating add constraint fkListingCompaniesBusinessOperationRating foreign key (ticker) references listingCompanies (ticker);
-- alter table financialHealthRating add constraint fkListingCompaniesFinancialHealthRating foreign key (ticker) references listingCompanies (ticker);
-- alter table valuationRating add constraint fkListingCompaniesValuationRating foreign key (ticker) references listingCompanies (ticker);
-- alter table industryFinancialHealth add constraint fkListingCompaniesIndustryFinancialHealth foreign key (ticker) references listingCompanies (ticker);



create table if not exists listingCompanies (
 	id serial,
 	ticker varchar(3) unique,
 	exchange varchar(5),
 	shortName varchar(256),
 	industryId double precision,
 	industryIdv2 integer,
 	industry varchar(256),
 	industryEn varchar(256),
 	establishedYear double precision,
 	noEmployees double precision,
 	noShareholders double precision,
 	foreignPercent double precision,
 	website varchar(256),
 	stockRating double precision,
 	deltaInWeek double precision,
 	deltaInMonth double precision,
 	deltaInYear double precision,
 	outstandingShare double precision,
 	issueShare double precision,
 	companyType varchar(2),
 	primary key (id)
 );
 
 
 
create table if not exists stockHistory (
 	ticker varchar(3),
 	timeStamp timestamp,
 	open double precision,
 	high double precision,
 	low double precision,
 	close double precision,
 	volume integer,
 	primary key (ticker, timeStamp),
 	foreign key (ticker) references listingCompanies (ticker)
 );

 
 
create table if not exists incomeStatement (
 	ticker varchar(3),
 	year integer,
 	quarter integer,
 	revenue integer,
 	yearRevenueGrowth double precision,
 	quarterRevenueGrowth double precision,
 	costOfGoodSold double precision,
 	grossProfit double precision,
 	operationExpense double precision,
 	operationProfit double precision,
 	yearOperationProfitGrowth double precision,
 	quarterOperationProfitGrowth double precision,
 	interestExpense double precision,
 	preTaxProfit integer,
 	postTaxProfit integer,
 	shareHolderIncome integer,
 	yearShareHolderIncomeGrowth double precision,
 	quarterShareHolderIncomeGrowth double precision,
 	investProfit double precision,
 	serviceProfit double precision,
 	otherProfit double precision,
 	provisionExpense double precision,
 	operationIncome double precision,
 	ebitda double precision,
 	primary key (ticker, year, quarter),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists balanceSheet (
 	ticker varchar(3),
 	year integer,
 	quarter integer,
 	shortAsset double precision,
 	cash integer,
 	shortInvest double precision,
 	shortReceivable double precision,
 	inventory double precision,
 	longAsset double precision,
 	fixedAsset double precision,
 	asset integer,
 	debt double precision,
 	shortDebt double precision,
 	longDebt double precision,
 	equity integer,
 	capital integer,
 	centralBankDeposit double precision,
 	otherBankDeposit double precision,
 	otherBankLoan double precision,
 	stockInvest double precision,
 	customerLoan double precision,
 	badLoan double precision,
 	provision double precision,
 	netCustomerLoan double precision,
 	otherAsset double precision,
 	otherBankCredit double precision,
 	oweOtherBank double precision,
 	oweCentralBank double precision,
 	valuablePaper double precision,
 	payableInterest double precision,
 	receivableInterest double precision,
 	deposit double precision,
 	otherDebt double precision,
 	fund double precision,
 	unDistributedIncome double precision,
 	minorShareHolderProfit double precision,
 	payable double precision,
 	primary key (ticker, year, quarter),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists cashFlow (
 	ticker varchar(3),
 	year integer,
 	quarter integer,
 	investCost integer,
 	fromInvest integer,
 	fromFinancial integer,
 	fromSale integer,
 	freeCashFlow double precision,
 	primary key (ticker, year, quarter),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists financialRatio (
 	ticker varchar(3),
 	year integer,
 	quarter integer,
 	priceToEarning double precision,
 	priceToBook double precision,
 	valueBeforeEbitda double precision,
 	dividend double precision,
 	roe double precision,
 	roa double precision,
 	daysReceivable double precision,
 	daysInventory double precision,
 	daysPayable double precision,
 	ebitOnInterest double precision,
 	earningPerShare double precision,
 	bookValuePerShare double precision,
 	interestMargin double precision,
 	nonInterestOnToi double precision,
 	badDebtPercentage double precision,
 	provisionOnBadDebt double precision,
 	costOfFinancing double precision,
 	equityOnTotalAsset double precision,
 	equityOnLoan double precision,
 	costToIncome double precision,
 	equityOnLiability double precision,
 	currentPayment double precision,
 	quickPayment double precision,
 	epsChange double precision,
 	ebitdaOnStock double precision,
 	grossProfitMargin double precision,
 	operatingProfitMargin double precision,
 	postTaxMargin double precision,
 	debtOnEquity double precision,
 	debtOnAsset double precision,
 	debtOnEbitda double precision,
 	shortOnLongDebt double precision,
 	assetOnEquity double precision,
 	capitalBalance double precision,
 	cashOnEquity double precision,
 	cashOnCapitalize double precision,
 	cashCirculation double precision,
 	revenueOnWorkCapital double precision,
 	capexOnFixedAsset double precision,
 	revenueOnAsset double precision,
 	postTaxOnPreTax double precision,
 	ebitOnRevenue double precision,
 	preTaxOnEbit double precision,
 	preProvisionOnToi double precision,
 	postTaxOnToi double precision,
 	loanOnEarnAsset double precision,
 	loanOnAsset double precision,
 	loanOnDeposit double precision,
 	depositOnEarnAsset double precision,
 	badDebtOnAsset double precision,
 	liquidityOnLiability double precision,
 	payableOnEquity double precision,
 	cancelDebt double precision,
 	ebitdaOnStockChange double precision,
 	bookValuePerShareChange double precision,
 	creditGrowth double precision,
 	primary key (ticker, year, quarter),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
 
create table if not exists stockIntradayTransaction (
 	id serial,
 	price double precision,
 	volume integer,
 	cp double precision,
 	rcp double precision,
 	a varchar(2),
 	ba double precision,
 	sa double precision,
 	hl varchar(256),
 	pcp double precision,
	timeStamp timestamp,
 	ticker varchar(3),
 	primary key (id, timeStamp),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists generalRating (
 	ticker varchar(3),
 	stockRating double precision,
 	valuation double precision,
 	financialHealth double precision,
 	businessModel double precision,
 	businessOperation double precision,
 	rsRating double precision,
 	taScore double precision,
 	highestPrice double precision,
 	lowestPrice double precision,
 	priceChange3m double precision,
 	priceChange1y double precision,
 	beta double precision,
 	alpha double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists businessModelRating (
 	ticker varchar(3),
 	businessModel double precision,
 	businessEfficiency double precision,
 	assetQuality double precision,
 	cashFlowQuality double precision,
 	bom double precision,
 	businessAdministration double precision,
 	productService double precision,
 	businessAdvantage double precision,
 	companyPosition double precision,
 	industry double precision,
 	operationRisk double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists businessOperationRating (
 	ticker varchar(3),
 	industryEn varchar(256),
 	loanGrowth double precision,
 	depositGrowth double precision,
 	netInterestIncomeGrowth double precision,
 	netInterestMargin double precision,
 	costToIncome double precision,
 	netIncomeToI double precision,
 	businessOperation double precision,
 	avgRoE double precision,
 	avgRoA double precision,
 	last5yearsNetProfitGrowth double precision,
 	last5yearsRevenueGrowth double precision,
 	last5yearsOperatingProfitGrowth double precision,
 	last5yearsEbItDaGrowth double precision,
 	last5yearsFcFfGrowth double precision,
 	lastYearGrossProfitMargin double precision,
 	lastYearOperatingProfitMargin double precision,
 	lastYearNetProfitMargin double precision,
 	tOiGrowth double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists financialHealthRating (
 	ticker varchar(3),
 	industryEn varchar(256),
 	loanDeposit double precision,
 	badLoanGrossLoan double precision,
 	badLoanAsset double precision,
 	provisionBadLoan double precision,
 	financialHealth double precision,
 	netDebtEquity double precision,
 	currentRatio double precision,
 	quickRatio double precision,
 	interestCoverage double precision,
 	netDebtEbItDa double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists valuationRating (
 	ticker varchar(3),
 	industryEn varchar(256),
 	valuation double precision,
 	pe double precision,
 	pb double precision,
 	ps double precision,
 	evebitda double precision,
 	dividendRate double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );
 
 
create table if not exists industryFinancialHealth (
 	ticker varchar(3),
 	industryEn double precision,
 	loanDeposit double precision,
 	badLoanGrossLoan double precision,
 	badLoanAsset double precision,
 	provisionBadLoan double precision,
 	financialHealth double precision,
 	netDebtEquity double precision,
 	currentRatio double precision,
 	quickRatio double precision,
 	interestCoverage double precision,
 	netDebtEbItDa double precision,
 	primary key (ticker),
 	foreign key (ticker) references listingCompanies (ticker)
 );