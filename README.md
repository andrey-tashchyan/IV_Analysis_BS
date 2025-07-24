
# 📈 Implied Volatility Analysis & Option Pricing Tool

This beta version Python-based project allows you to:

- Extract and visualize implied volatility curves (smile/skew)
- Compute implied volatilities using our Black-Scholes model
- Compare them to Yahoo Finance data for both calls and puts
- Fallback to demo data if live download fails
- Smooth and display clean volatility plots
- Automatically fetch and store the latest spot price

---

## 🔧 Features

| Feature                               | Description                                                     |
|---------------------------------------------------------------------------------------------------------|
| 🧠 Black-Scholes Pricing              | Compute vanilla option prices (calls/puts) analytically         |
| 🔍 Implied Volatility Extraction      | Solves for IV using Brent's root-finding method                 |
| 📊 Dual Plotting                      | Compares Yahoo IV vs. Black-Scholes IV for both puts and calls  |
| 🧪 Demo Data Fallback                 | Loads demo files if API fails (rate-limiting, invalid ticker, etc.)    |
| 💾 Spot Price Caching                 | Saves the latest spot in `data/spot.csv`                        |

---

## 📁 Project Structure

p1/
├── data/
│   ├── demo_calls.csv         # fallback call options data
│   ├── demo_puts.csv          # fallback put options data
│   ├── demo_spot.csv          # fallback spot price
│   └── spot.csv               # dynamically updated by script
|   |__ calls.csv              # dynamically created uploading live market data
|   |__ puts.csv               # dynamically created uploading live market data
|   |__ spot.csv               # dynamically created uploading live market data
|
│
├── src/
│   ├── main.py                # main program
│   ├── bs_model.py            # BS pricing & implied volatility solver
│   ├── vol_analysis.py        # plotting logic & smoothing
│   └── update_spot.py         # gets live spot price via yfinance
│
├── README.md
└── requirements.txt

---

## ▶️ Getting Started

### 1. Install dependencies

pip install -r requirements.txt

> 📌 It's recommended to use a virtual environment.

### 2. Run the main program

cd src
python main.py

You will be prompted to input a stock ticker (e.g., AAPL, TSLA).

---

## 📊 What You’ll See

- Two subplots:  
  - Left → Black-Scholes computed IVs  
  - Right → Yahoo Finance provided IVs  
- Calls and puts plotted separately (different colors)
- A dashed vertical line indicating the spot price  
- Smoothed spline curves when enough points are available

---

## 💾 Spot Price Management

The script update_spot.py fetches the current spot price using Yahoo Finance and stores it in data/spot.csv. If the request fails, it waits 5 seconds and retries once. If still unsuccessful, the program will use the fallback demo_spot.csv.

---

## 💡 Libraries Used

- pandas – Data handling
- numpy – Numerical computation
- matplotlib – Plotting
- scipy.optimize.brentq – Root solving for implied volatility
- scipy.interpolate.make_interp_spline – Smoothing IV curves
- yfinance – Spot price via Yahoo Finance
- curl_cffi – Robust Yahoo option chain scraping with Chrome impersonation

---

## ⚠️ Notes

- Only the nearest expiration is used for analysis.
- If API calls fail, the demo files will be used but the title will still show the input ticker and correct spot price.
- Greeks (Delta, Gamma, etc.) are not yet implemented.

---

## 🔁 Example Tickers to Try

AAPL   # Apple  
TSLA   # Tesla  
MSFT   # Microsoft  
GOOGL  # Alphabet  
^SPX   # S&P 500 Index

If no real-time data is available, the program will fall back to Apple demo data (24 July 2025).

---

## ✅ Output Sample

- Calls (🟢) and puts (🔴) IVs displayed
- Yahoo vs Calculated plotted side-by-side
- Smooth interpolation for aesthetic readability
- Spot price clearly marked on both graphs

---

## 📫 Contact
Andrey TASHCHYAN 
EPFL
andrey.tashchyan@epfl.ch

Feel free to fork, modify, or reach out for suggestions or improvements.

Happy pricing!
