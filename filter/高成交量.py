import pandas as pd
import yfinance as yf

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

# Calculate average volume for each stock
average_volumes = {ticker: data['Volume'].mean() for ticker, data in data_dict.items() if data is not None}

# Sort stocks by average volume in descending order and get the top 10
top_10_volume_stocks = sorted(average_volumes.items(), key=lambda item: item[1], reverse=True)[:10]

# Print the top 10 volume stocks
for ticker, avg_volume in top_10_volume_stocks:
    print(f"{ticker}: {avg_volume}")