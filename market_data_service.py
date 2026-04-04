import sqlite3
from urllib import response
import requests

DB_FILE = "market_data.db"
API_URL = "https://www.alphavantage.co/query"
API_KEY = "EGYL8S6JD25WYKVR"

class MarketDataService:

    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        return conn
    
    def init_db(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS monthly_data (
                symbol TEXT NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                volume INTEGER NOT NULL,
                UNIQUE(symbol, year, month)
            )
            """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_monthly_data(self, symbol: str):

        response = requests.get(
            API_URL,
            params={"function": "TIME_SERIES_MONTHLY", "symbol": symbol, "apikey": API_KEY},
            timeout=10,
        )

        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            return None

        data = response.json()

        return data