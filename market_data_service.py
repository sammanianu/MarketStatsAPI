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
            print(f"HTTP Error: {response.status_code}")
            return None

        data = response.json()

        #print(data.keys())

        if "Error Message" in data:
            print("API Error:", data["Error Message"])
            return None

        time_series = data.get("Monthly Time Series")

        if not time_series:
            print("No monthly data found for symbol:", symbol)
            return None

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
            raise Exception("No valid monthly data to store.")

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