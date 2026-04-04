from market_data_service import MarketDataService

market_data_service = MarketDataService() 

market_data_service.init_db()

symbol = "AAPL"
year_int = 2023

if not market_data_service.yearly_data_available(symbol, year_int):
    fetched_monthly_data = market_data_service.fetch_monthly_data(symbol)
    #print(fetched_monthly_data)
    market_data_service.store_monthly_data(symbol, fetched_monthly_data)