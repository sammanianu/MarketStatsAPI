import sqlite3

DB_FILE = "market_data.db"

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