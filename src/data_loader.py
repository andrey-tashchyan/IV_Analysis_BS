import pandas as pd
import os
from datetime import datetime
from curl_cffi import requests
import shutil

def download_data(ticker_symbol="AAPL"):
    print("=== Téléchargement via curl_cffi ===")

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    url = f"https://query2.finance.yahoo.com/v7/finance/options/{ticker_symbol}"
    session = requests.Session(impersonate="chrome")

    try:
        response = session.get(url)
        data = response.json()
        if 'optionChain' not in data or not data['optionChain']['result']:
            raise ValueError("Pas de données d'options valides")
    except Exception as e:
        print(f"❌ Error while downloading {ticker_symbol} : {e}")
        print("📂 Using demo data instead...")
        try:
            shutil.copy("../data/demo_calls.csv", "data/calls.csv")
            shutil.copy("../data/demo_puts.csv", "data/puts.csv")
            shutil.copy("../data/demo_spot.csv", "data/spot.csv")
            print("✅ Demo data successfully downloaded.")
            return True
        except Exception as e2:
            print(f"❌ Error while downloading demo data : {e2}")
            return False

    try:
        chain = data['optionChain']['result'][0]
        expiration_timestamp = chain['expirationDates'][0]
        options = chain['options'][0]
    except Exception as e:
        print(f"❌ Error parsing data : {e}")
        return False

    calls = pd.DataFrame(options['calls'])[['strike', 'lastPrice', 'impliedVolatility', 'volume']]
    puts  = pd.DataFrame(options['puts'])[['strike', 'lastPrice', 'impliedVolatility', 'volume']]

    calls.to_csv(os.path.join(output_dir, "calls.csv"), index=False)
    puts.to_csv(os.path.join(output_dir, "puts.csv"), index=False)

    expiration_date = datetime.fromtimestamp(expiration_timestamp).strftime("%Y-%m-%d")
    spot = float(chain['quote']['regularMarketPrice'])
    today = datetime.today().strftime("%Y-%m-%d")

    pd.DataFrame({'spot': [spot], 'date': [today]}).to_csv(
        os.path.join(output_dir, "spot.csv"), index=False
    )

    print(f"✅ Data downloaded for {ticker_symbol} (exp: {expiration_date})")
    return True