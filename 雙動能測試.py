import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the ticker symbols
tickers = ["GLD", "QQQ", "TLT", "VOO"]

# Fetch historical data
data = yf.download(tickers, start="2008-01-01")['Close']

# Calculate the average rate of return
def get_average_rate_of_return(prices):
    month1 = (prices / prices.shift(21) - 1) * 100
    month3 = (prices / prices.shift(63) - 1) * 100
    month6 = (prices / prices.shift(126) - 1) * 100
    return month1 * 0.5 + month3 * 0.3 + month6 * 0.2

returns = data.apply(get_average_rate_of_return)

# Determine the best asset to invest in each month
monthly_returns = returns.resample('M').last()

# Ensure we have no NaN values in best_assets
best_assets = monthly_returns.idxmax(axis=1).dropna()
print(best_assets)

# Simulate the investment
initial_investment = 10000
investment_values = pd.Series(index=monthly_returns.index, dtype=float)
investment_values.iloc[0] = initial_investment

for i in range(1, len(best_assets)):
    current_asset = best_assets.iloc[i]
    date = monthly_returns.index[i]
    previous_date = monthly_returns.index[i-1]
    
    if current_asset in data.columns and date in data.index and previous_date in data.index:
        current_price = data[current_asset].loc[date]
        previous_price = data[current_asset].loc[previous_date]
        investment_values.iloc[i] = investment_values.iloc[i-1] * (current_price / previous_price)
    else:
        investment_values.iloc[i] = investment_values.iloc[i-1]  # Carry forward the previous value if date not found

# Fill initial NaN and calculate cumulative returns
investment_values.fillna(method='ffill', inplace=True)

# Plot the total return
plt.figure(figsize=(12, 6))
plt.plot(investment_values, label='Total Return', color='green')
plt.title('Total Return of Investment Strategy')
plt.xlabel('Date')
plt.ylabel('Total Return ($)')
plt.legend()
plt.grid(True)
plt.show()