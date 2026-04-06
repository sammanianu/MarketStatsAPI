# Market Stats API

A FASTAPI service that povides annual market statistics for symbols for particular year

## Features

- Fetch monthly stock data from Alpha Vantage API.
- Store data in a local SQLite database.
- Return annual summary for a given stock symbol and year:
  - Highest monthly price
  - Lowest monthly price
  - Total annual trading volume
- Input validation for stock symbols and years.

## Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/sammanianu/MarketStatsAPI.git
   cd MarketStatsAPI
   ```

2. **Install dependencies**  
    ```bash
    pip install fastapi uvicorn requests
    ```

3. **Configure API key in `app/config.py`**
    ```python
    API_KEY = "your Alpha Vantage API key"
    You can claim a free API key here: https://www.alphavantage.co/support/#api-key
    ```

4. **Instruction for run using localhost**
   ```bash
   python -m uvicorn main:app --reload
   ```

5. **Access API docs**
   UI: http://127.0.0.1:8000/docs

## Usage

**Get annual summary:**
```bash
GET /symbols/{symbol}/annual/{year}
```

**Example Request:**
```bash
http://127.0.0.1:8000/symbols/IBM/annual/2021
```

**Example Response:**
```json
{
  "high": "152.84",
  "low": "114.56",
  "volume": "1350035200"
}
```

### Response Fields
- `high`: the highest price for symbol within year
- `low` : the lowest price for symbol within year
- `volume` : the sum of all monthly volumes for symbol for year

### Error Responses
- **400 Bad Request**: Invalid symbol or year formats.
- **404 Not Found**: Symbol not found or no data available.
- **500 Internam Server Error**: External API issue or server errors
- **502 Bad Gateway**: Alpha Vantage API connection issues.

