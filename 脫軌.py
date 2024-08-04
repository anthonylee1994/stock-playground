import yfinance as yf
import pandas as pd
import asyncio
import warnings

warnings.filterwarnings('ignore')

sp500_url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'

# Fetch S&P 500 tickers
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

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    data['sma'] = data['Close'].rolling(window=window).mean()
    data['std_dev'] = data['Close'].rolling(window=window).std()
    data['bb_upper'] = data['sma'] + (data['std_dev'] * num_std_dev)
    data['bb_lower'] = data['sma'] - (data['std_dev'] * num_std_dev)
    return data

def filter_stocks(data):
    if data is not None and not data.empty:
        current_high = data['High'].iloc[-1]
        current_low = data['Low'].iloc[-1]
        current_open = data['Open'].iloc[-1]
        current_close = data['Close'].iloc[-1]
        current_bb_upper = data['bb_upper'].iloc[-1]
        current_bb_lower = data['bb_lower'].iloc[-1]
        
        if (current_high < current_bb_lower and current_low < current_bb_lower and 
            current_open < current_bb_lower and current_close < current_bb_lower):
            return 'lower'
        elif (current_high > current_bb_upper and current_low > current_bb_upper and 
              current_open > current_bb_upper and current_close > current_bb_upper):
            return 'upper'
    return None

async def process_ticker(ticker):
    ticker, data = await asyncio.to_thread(fetch_data, ticker)
    if data is not None and not data.empty:
        data = calculate_bollinger_bands(data)
        result = filter_stocks(data)
        if result == 'lower':
            print(f'{ticker} current price bar is totally lower than the lower Bollinger Band.')
        elif result == 'upper':
            print(f'{ticker} current price bar is totally higher than the upper Bollinger Band.')

async def main():
    tasks = [process_ticker(ticker) for ticker in tickers]
    await asyncio.gather(*tasks)

# Run the main event loop
if __name__ == '__main__':
    asyncio.run(main())