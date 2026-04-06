from fastapi import FastAPI, HTTPException
from app.market_data_service import MarketDataService
from app.validations import InputValidator

app = FastAPI()
market_data_service = MarketDataService() 
input_validator = InputValidator()
market_data_service.init_db()

@app.get("/symbols/{symbol}/annual/{year}")
def get_annual_summary(symbol: str, year: int):
    try:
        symbol = symbol.strip()
        input_validator.validate_symbol(symbol)
        input_validator.validate_year(year)

        if not market_data_service.yearly_data_available(symbol, year):
            fetched_monthly_data = market_data_service.fetch_monthly_data(symbol)
            if not fetched_monthly_data:
                raise HTTPException(status_code=404, detail=f"No data found for {symbol}")
            market_data_service.store_monthly_data(symbol, fetched_monthly_data)

        return market_data_service.get_yearly_summary(symbol, year)
        
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except TypeError as te:
        raise HTTPException(status_code=404, detail="No data available in DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")