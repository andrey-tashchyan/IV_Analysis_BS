import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq



# === Black-Scholes formula ===
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma * np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# === Implied Volatility (numerical inversion) ===
def implied_volatility(market_price, S, K, T, r, option_type='call'):
    def f(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price

    try:
        return brentq(f, 0.001, 2.0, maxiter=100)
    except ValueError:
        return np.nan