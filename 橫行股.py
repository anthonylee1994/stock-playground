import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Fetch S&P 500 tickers
sp500_url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
sp500 = pd.read_csv(sp500_url)
tickers = sp500['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers]

def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1mo', interval='1d')
        return ticker, data
    except Exception:
        return ticker, None

# Fetch data for all tickers
data_dict = {ticker: fetch_data(ticker)[1] for ticker in tickers}

# Calculate average volume and slope of closing prices over the last 12 months
avg_volumes = {}
slopes = {}
for ticker, data in data_dict.items():
    if data is not None and not data.empty:
        avg_volumes[ticker] = data['Volume'].mean()
        # Calculate the slope of the closing prices
        x = np.arange(len(data))
        y = data['Close'].values
        slope, _, _, _, _ = linregress(x, y)
        slopes[ticker] = slope

# Filter stocks by high volume and positive but low slope
filtered_stocks = {ticker: (avg_volumes[ticker], slopes[ticker]) for ticker in avg_volumes if slopes[ticker] > 0}
sorted_stocks = sorted(filtered_stocks.items(), key=lambda x: (-x[1][0], x[1][1]))[:10]

# Print the results
print("Top 10 stocks with the highest volume and rising slowly:")
for ticker, (volume, slope) in sorted_stocks:
    print(f"{ticker}: Average Volume = {volume:.0f}, Slope = {slope:.6f}")

# Plot the performance of the top 10 stocks
plt.figure(figsize=(12, 6))
for ticker, _ in sorted_stocks:
    data = data_dict[ticker]
    plt.plot(data.index, data['Close'], label=ticker)

plt.title('Performance of Top 10 stocks with highest volume and rising slowly')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.grid(True)
plt.show()