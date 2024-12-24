import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

# Define the tickers of the stocks
tickers = ["BCO", "AOS", "DHR", "AVY", "CHE"]  # Add more tickers as needed

# Download historical data for the past year
end_date = pd.to_datetime('today').strftime('%Y-%m-%d') 
start_date = (pd.to_datetime('today') - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)

    if len(data) == 0:
        print(f"No data available for {ticker}")
        continue

    # Ensure both arrays have the same shape
    x = np.arange(len(data['Close']))
    y = data['Close'].values.ravel()  # Flatten y to make it 1-dimensional

    # Print shapes for debugging
    print(f"{ticker} - x shape: {x.shape}, y shape: {y.shape}")

    if len(x) != len(y):
        print(f"Data length mismatch for {ticker}")
        continue

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    regression_line = slope * x + intercept

    # Plot the data and the regression line
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, y, label=f'{ticker} Close Price')
    plt.plot(data.index, regression_line, label='Regression Line', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{ticker} Close Price and Regression Line')
    plt.legend()
    plt.show()