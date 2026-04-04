from market_data_service import MarketDataService

market_data_service = MarketDataService() 

market_data_service.init_db()

def get_annual_summary(symbol: str, year: str):
    if not market_data_service.yearly_data_available(symbol, int(year)):
        fetched_monthly_data = market_data_service.fetch_monthly_data(symbol)
        market_data_service.store_monthly_data(symbol, fetched_monthly_data)

    summary = market_data_service.get_yearly_summary(symbol, int(year))
    print(f"Annual summary for {symbol} in {year}:{summary}")
    return summary

#get_annual_summary("AAPL", 2023)