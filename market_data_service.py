import sqlite3
from unittest import result
from urllib import response
from fastapi import HTTPException
import requests
from typing import Dict

DB_FILE = "market_data.db"
API_URL = "https://www.alphavantage.co/query"
API_KEY = "EGYL8S6JD25WYKVR"

class MarketDataService:

    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
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

        print(f"Fetching data for {symbol}.")

        response = requests.get(
            API_URL,
            params={"function": "TIME_SERIES_MONTHLY", "symbol": symbol, "apikey": API_KEY},
            timeout=10,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to fetch data from external API: {response.status_code}",
            )

        data = response.json()

        if "Error Message" in data:
            raise HTTPException(status_code=404, detail="Symbol not found in external API.")

        time_series = data.get("Monthly Time Series")

        if not time_series:
            raise HTTPException(
                status_code=502,
                detail="External API returned unexpected data format.",
            )

        return time_series
    
    def store_monthly_data(self, symbol: str, time_series: Dict[str, dict]):
        conn = self.get_db_connection()
        rows = []
        for date_str, values in time_series.items():
            try:
                year, month, _ = date_str.split("-")
                rows.append(
                    (
                        symbol,
                        int(year),
                        int(month),
                        values["2. high"],
                        values["3. low"],
                        int(values["5. volume"]),
                    )
                )
            except Exception:
                continue

        if not rows:
            conn.close()
            raise HTTPException(status_code=502, detail="No valid monthly data to store.")

        conn.executemany(
            """
            INSERT OR IGNORE INTO monthly_data
            (symbol, year, month, high, low, volume)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        conn.close()

    def yearly_data_available(self, symbol: str, year: int):
        conn = self.get_db_connection()
        cursor = conn.execute(
            "SELECT COUNT(1) AS count FROM monthly_data WHERE symbol = ? AND year = ?",
            (symbol, year),
        )

        row = cursor.fetchone()
        conn.close()
        count = row[0]

        if count > 0:
            print(f"Data exists for {symbol} in {year}.")
            return True
        else:
            return False
        
    def get_yearly_summary (self, symbol: str, year: int):
        conn = self.get_db_connection()
        cursor = conn.execute(
            """
            SELECT
                MAX(high) AS high,
                MIN(low) AS low,
                SUM(volume) AS volume
            FROM monthly_data
            WHERE symbol = ? AND year = ?
            """,
            (symbol, year),
        )
        result = cursor.fetchone()
        conn.close()

        if result["high"] is None or result["low"] is None or result["volume"] is None:
            raise HTTPException(
                status_code=404,
                detail=f"No monthly data available for {symbol} in {year}.",
            )

        return {
            "high": f"{result['high']}",
            "low": f"{result['low']}",
            "volume": str(result["volume"]),
        }