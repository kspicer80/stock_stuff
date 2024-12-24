print("Script is starting ...")
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
from indicator_functions import *

def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def make_recommendation(df):
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger_bands(df)
    df = calculate_stochastic(df)
    df = calculate_atr(df)
    
    recommendation = "Hold"
    
    macd = df['MACD'].iloc[-1]
    macd_signal = df['MACD_Signal'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    close = df['Close'].iloc[-1]
    lower_band = df['LowerBand'].iloc[-1]
    upper_band = df['UpperBand'].iloc[-1]
    slowk = df['SlowK'].iloc[-1]
    slowd = df['SlowD'].iloc[-1]
    atr = df['ATR'].iloc[-1]
    atr_mean = df['ATR'].mean()

    # Debugging statements
    print(f"MACD: {macd}, MACD Signal: {macd_signal}, RSI: {rsi}")
    print(f"Close: {close}, Lower Band: {lower_band}, Upper Band: {upper_band}")
    print(f"SlowK: {slowk}, SlowD: {slowd}, ATR: {atr}, ATR Mean: {atr_mean}")

    close_value = close.values[0]  # Extract the scalar value from the Series

    if macd > macd_signal and rsi < 70:
        recommendation = "Buy"
    elif macd < macd_signal and rsi > 30:
        recommendation = "Sell"

    # Incorporate Bollinger Bands
    if close_value < lower_band:
        recommendation = "Buy"
    elif close_value > upper_band:
        recommendation = "Sell"

    # Incorporate Stochastic Oscillator
    if slowk < 20 and slowd < 20:
        recommendation = "Buy"
    elif slowk > 80 and slowd > 80:
        recommendation = "Sell"

    # Incorporate ATR for volatility check (optional)
    if atr > atr_mean:
        recommendation += " (High Volatility)"

    return recommendation

def main():
    tickers = ["BCO", "AOS", "DHR", "AVY", "CHE", "XLK"]  # List of ticker symbols
    start_date = '2024-01-01'
    end_date = '2024-12-19'

    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, start_date, end_date)
        recommendation = make_recommendation(stock_data)
        print(f"Recommendation for {ticker}: {recommendation}")

if __name__ == "__main__":
    main()