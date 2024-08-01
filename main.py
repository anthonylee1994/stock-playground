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

def td_sequential(data):
    data['td_buy_setup'] = 0
    data['td_sell_setup'] = 0

    buy_condition = data['Close'] < data['Close'].shift(4)
    sell_condition = data['Close'] > data['Close'].shift(4)

    data['td_buy_setup'] = buy_condition.groupby((buy_condition != buy_condition.shift()).cumsum()).cumsum()
    data['td_sell_setup'] = sell_condition.groupby((sell_condition != sell_condition.shift()).cumsum()).cumsum()

    return data

async def process_ticker(ticker):
    ticker, data = await asyncio.to_thread(fetch_data, ticker)
    if data is not None and not data.empty:
        data = td_sequential(data)
        td_buy_setup = data['td_buy_setup'].iloc[-1]
        td_sell_setup = data['td_sell_setup'].iloc[-1]

        if td_buy_setup >= 9 and td_buy_setup<= 13:
            print(f'{ticker} is on a TD Buy Setup {td_buy_setup}')
        elif td_sell_setup >= 9 and td_sell_setup <= 13:
            print(f'{ticker} is on a TD Sell Setup {td_sell_setup}')

async def main():
    tasks = [process_ticker(ticker) for ticker in tickers]
    await asyncio.gather(*tasks)

# Run the main event loop
if __name__ == '__main__':
    asyncio.run(main())