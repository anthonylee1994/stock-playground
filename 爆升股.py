import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch S&P 500 tickers
sp500_url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
sp500 = pd.read_csv(sp500_url)
tickers = sp500['Symbol'].tolist()
tickers = [ticker.replace('.', '-') for ticker in tickers]

def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='12mo', interval='1d')
        return ticker, data
    except Exception:
        return ticker, None

# Fetch data for all tickers
data_dict = {ticker: fetch_data(ticker)[1] for ticker in tickers}

# Calculate total return and average volume over the last 12 months
returns = {}
volumes = {}
for ticker, data in data_dict.items():
    if data is not None and not data.empty:
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        total_return = (end_price - start_price) / start_price
        avg_volume = data['Volume'].mean()
        returns[ticker] = total_return
        volumes[ticker] = avg_volume

# Normalize returns and volumes
max_return = max(returns.values())
max_volume = max(volumes.values())
normalized_scores = {ticker: (returns[ticker] / max_return) * 0.5 + (volumes[ticker] / max_volume) * 0.5 for ticker in returns}

# Find the top 10 stocks with the highest scores
top_10_stocks = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)[:10]

# Print the results
print("Top 10 stocks with the highest return and significant trading volume:")
for ticker, score in top_10_stocks:
    print(f"{ticker}: Return = {returns[ticker]:.2%}, Average Volume = {volumes[ticker]:.0f}, Score = {score:.2f}")

# Plot the performance of the top 10 stocks
plt.figure(figsize=(12, 6))
for ticker, _ in top_10_stocks:
    data = data_dict[ticker]
    plt.plot(data.index, data['Close'], label=ticker)

plt.title('Performance of Top 10 Stocks')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.grid(True)
plt.show()