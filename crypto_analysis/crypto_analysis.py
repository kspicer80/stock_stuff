import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Define the cryptocurrencies
cryptos = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'USDT-USD', 'SOL-USD', 'BNB-USD', 'DOGE-USD', 'USDC-USD', 'ADA-USD', 'TRX-USD', "IBIT", "ETHA"]


# Find the oldest date for each cryptocurrency
oldest_dates = {}
for crypto in cryptos:
    try:
        data = yf.download(crypto, period='max')
        oldest_dates[crypto] = data.index.min()
    except Exception as e:
        print(f"Failed to download data for {crypto}: {e}")

# Remove cryptocurrencies that failed to download
cryptos = [crypto for crypto in cryptos if crypto in oldest_dates]

# Find the overall oldest date
overall_oldest_date = min(oldest_dates.values()).strftime('%Y-%m-%d')

# Fetch the data from the overall oldest date to today
data = yf.download(cryptos, start=overall_oldest_date, end=datetime.today().strftime('%Y-%m-%d'))['Close']

# Calculate the correlation matrix
correlation_matrix = data.corr()

# Find the most highly correlated pairs
correlation_pairs = correlation_matrix.unstack()
sorted_pairs = correlation_pairs.sort_values(kind="quicksort", ascending=False)
high_corr_pairs = sorted_pairs[(sorted_pairs < 1) & (sorted_pairs > 0.8)]

# Print the most highly correlated pairs
print("Most highly correlated pairs:")
print(high_corr_pairs)

# Plot the heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='inferno')
plt.title('Cryptocurrency Correlation Matrix')
plt.show()