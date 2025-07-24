import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.interpolate import make_interp_spline
from bs_model import implied_volatility

def smooth_plot(ax, strikes, ivs, color, label):
    if len(strikes) < 4:
        ax.plot(strikes, ivs, 'o-', color=color, label=label)
        return
    sorted_idx = np.argsort(strikes)
    x = np.array(strikes)[sorted_idx]
    y = np.array(ivs)[sorted_idx]
    x_new = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=min(3, len(x)-1))
    y_smooth = spline(x_new)
    ax.plot(x_new, y_smooth, color=color, linewidth=2.2, label=label)
    ax.scatter(x, y, color=color, s=30, alpha=0.6)

def analyze_volatility(ticker):
    print(f"=== Starting volatility analysis for {ticker} ===")
    data_source_ticker = ticker  # Ticker réellement utilisé pour les graphes

    # === Spot price ===
    try:
        spot_data = pd.read_csv("data/spot.csv")
    except:
        spot_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/demo_spot.csv"))
        print("⚠️ Using demo spot.csv")
        data_source_ticker = "AAPL (demo)"

    S = float(spot_data['spot'].iloc[0])
    today = pd.to_datetime(spot_data['date'].iloc[0])
    print(f"💰 Spot: {S:.2f}  📅 Date: {today.date()}")

    # === Dates & Constants ===
    r = 0.01
    expiration = "2025-09-20"
    expiration_date = datetime.strptime(expiration, "%Y-%m-%d")
    T = (expiration_date - today).days / 365.0
    if T <= 0:
        print("❌ Option expired.")
        return

    # === Chargement données ===
    try:
        df_calls = pd.read_csv(f"data/{ticker}_calls.csv")[['strike', 'lastPrice', 'impliedVolatility']]
        df_puts  = pd.read_csv(f"data/{ticker}_puts.csv")[['strike', 'lastPrice', 'impliedVolatility']]
    except:
        df_calls = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/demo_calls.csv"))[['strike', 'lastPrice', 'impliedVolatility']]
        df_puts  = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/demo_puts.csv"))[['strike', 'lastPrice', 'impliedVolatility']]
        print("⚠️ Using demo options data")
        data_source_ticker = "AAPL (demo)"

    # === Calcul des IVs ===
    df_calls['calculated IV'] = df_calls.apply(
        lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, r, 'call'), axis=1)
    df_puts['calculated IV'] = df_puts.apply(
        lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, r, 'put'), axis=1)

    # === Nettoyage des données aberrantes ===
    df_calls = df_calls[
        (df_calls['calculated IV'] > 0.01) & (df_calls['calculated IV'] < 2.0)
    ].sort_values('strike')

    df_puts = df_puts[
        (df_puts['calculated IV'] > 0.01) & (df_puts['calculated IV'] < 2.0)
    ].sort_values('strike')

    # === Création figure ===
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#f5f5f5')

    # === Style axes ===
    for ax in axs:
        ax.set_facecolor('#ffffff')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#999999')
        ax.spines['bottom'].set_color('#999999')
        ax.tick_params(colors='#333333')
        ax.title.set_color('#111111')
        ax.xaxis.label.set_color('#444444')
        ax.yaxis.label.set_color('#444444')

    # === Y-Limits unifiés ===
    y_min = 0
    y_max = max(
        df_calls['impliedVolatility'].max(),
        df_puts['impliedVolatility'].max(),
        df_calls['calculated IV'].max(),
        df_puts['calculated IV'].max()
    )
    axs[0].set_ylim(y_min, y_max)
    axs[1].set_ylim(y_min, y_max)

    # === Subplot 1: Calculées ===
    smooth_plot(axs[0], df_calls['strike'], df_calls['calculated IV'], '#2a9d8f', 'Calls (Calculated)')
    smooth_plot(axs[0], df_puts['strike'], df_puts['calculated IV'], '#e76f51', 'Puts (Calculated)')
    axs[0].axvline(S, color='black', linestyle='--', alpha=0.6, label=f'Spot: ${S:.2f}')
    axs[0].set_title(f"Implied Volatility (Computed by our model) - {data_source_ticker}", fontsize=14, fontweight='bold')
    axs[0].set_xlabel("Strike")
    axs[0].set_ylabel("Implied Volatility")
    axs[0].legend()

    # === Subplot 2: Yahoo ===
    smooth_plot(axs[1], df_calls['strike'], df_calls['impliedVolatility'], '#2a9d8f', 'Calls (Yahoo)')
    smooth_plot(axs[1], df_puts['strike'], df_puts['impliedVolatility'], '#e76f51', 'Puts (Yahoo)')
    axs[1].axvline(S, color='black', linestyle='--', alpha=0.6, label=f'Spot: ${S:.2f}')
    axs[1].set_title(f"Implied Volatility (Yahoo Finance) - {data_source_ticker}", fontsize=14, fontweight='bold')
    axs[1].set_xlabel("Strike")
    axs[1].set_ylabel("Implied Volatility")
    axs[1].legend()

    plt.tight_layout()
    plt.show()
    print(f"✅ Analysis done for {ticker}")

if __name__ == "__main__":
    analyze_volatility("AAPL")