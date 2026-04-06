from fastapi import HTTPException
from app.config import MAX_YEAR, MIN_YEAR

class InputValidator:

    def validate_year(self, year: int):
        if year < MIN_YEAR or year > MAX_YEAR:
            raise HTTPException(status_code=400, detail="Year must be in YYYY format.")
        
    
    def validate_symbol(self, symbol: str):
        if not symbol or not symbol.isalnum():
            raise HTTPException(status_code=400, detail="Invalid stock symbol.")