import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cvxpy as cp
from sklearn.linear_model import LinearRegression
import json

with open("all_symbols/all_watchlist_symbols.json", "r") as f:
    all_watchlist_symbols = json.load(f)
    
# Define the end date as today
end_date = datetime.now().strftime('%Y-%m-%d')

# Function to fetch historical data for stocks
def fetch_historical_data(symbols):
    historical_data = {}
    for symbol in symbols:
        try:
            data = yf.download(symbol, period="max")
            if not data.empty:
                historical_data[symbol] = data
            else:
                print(f"No price data found for {symbol}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return historical_data

# Fetch historical data for the stock tickers
historical_data = fetch_historical_data(all_watchlist_symbols)

# Filter out stocks with no data
valid_symbols = [symbol for symbol, data in historical_data.items() if not data.empty]

# Align data by common dates
aligned_data = pd.concat([historical_data[symbol]['Close'].pct_change().dropna() for symbol in valid_symbols], axis=1, keys=valid_symbols).dropna()

# Calculate geometric mean return and covariance matrix
geometric_mean_returns = ((1 + aligned_data).prod() ** (1 / aligned_data.shape[0]) - 1).values  # Convert to NumPy array
cov_matrix = aligned_data.cov().values  # Convert to NumPy array

# Define the optimization problem using cvxpy
def optimize_allocation(expected_returns, cov_matrix, money_to_spend, max_weight=0.2, min_weight=0.01):
    num_assets = len(expected_returns)
    weights = cp.Variable(num_assets)
    
    # Objective function: maximize expected return
    objective = cp.Maximize(expected_returns @ weights)
    
    # Constraints: sum of weights equals 1, weights are non-negative, weights are less than or equal to max_weight, and weights are greater than or equal to min_weight
    constraints = [cp.sum(weights) == 1, weights >= min_weight, weights <= max_weight]
    
    # Define the problem
    problem = cp.Problem(objective, constraints)
    
    # Solve the problem
    problem.solve()
    
    # Get the optimal weights
    optimal_weights = weights.value
    
    # Adjust for the total money to spend
    adjusted_weights = {stock: weight * money_to_spend for stock, weight in zip(valid_symbols, optimal_weights)}
    
    return adjusted_weights

# Optimize allocation for personal account
optimal_weights_personal = optimize_allocation(geometric_mean_returns, cov_matrix, 1000.00)

# Print the optimal allocations
print("Optimal Allocation for Personal Account:")
for stock, amount in optimal_weights_personal.items():
    print(f"{stock}: ${amount:.2f}")

# Plot the historical data and trendlines for the top 5 stocks
top_5_stocks = sorted(optimal_weights_personal, key=optimal_weights_personal.get, reverse=True)[:5]
fig, axes = plt.subplots(5, 1, figsize=(14, 20), sharex=True)

# Generate distinct colors for each line plot
colors = plt.cm.get_cmap('tab10', 5)

for i, stock in enumerate(top_5_stocks):
    ax = axes[i]
    ax.plot(historical_data[stock].index, historical_data[stock]['Close'], label=stock, color=colors(i))
    
    # Add trend line
    x = np.arange(len(historical_data[stock]))
    y = historical_data[stock]['Close'].values
    model = LinearRegression().fit(x.reshape(-1, 1), y)
    trend = model.predict(x.reshape(-1, 1))
    ax.plot(historical_data[stock].index, trend, label=f'{stock} Trend', linestyle='--', color='red')
    
    ax.set_title(f'{stock} Price Over the Available Data Period')
    ax.set_ylabel('Price ($)')
    ax.legend()
    ax.grid(True)

plt.xlabel('Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()