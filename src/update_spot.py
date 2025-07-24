# src/update_spot.py

import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import time

def update_spot_price(ticker='AAPL', path='../data/spot.csv'):
    print(f"Downloading stock prices for : {ticker}...")

    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')

        if data.empty:
            print("⚠️ First attempt failed (empty data). Waiting 5s and retrying...")
            time.sleep(5)
            data = stock.history(period='1d')

        if data.empty:
            raise ValueError("No data received from Yahoo Finance after retry.")

        last_price = data['Close'].iloc[-1]
        today = datetime.today().strftime('%Y-%m-%d')

        df = pd.DataFrame({
            'spot': [round(last_price, 2)],
            'date': [today]
        })

        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)

        print(f"✅ Spot saved : {last_price:.2f} ({today}) → {path}")

    except Exception as e:
        print(f"Error while downloading Spots : {e}")

# Direct Execution
if __name__ == "__main__":
    update_spot_price()