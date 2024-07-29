import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='12mo', interval='1d')

def td_sequential(data):
    data['td_buy_setup'] = 0
    data['td_sell_setup'] = 0
    
    for i in range(4, len(data)):
        if (data['Close'].iloc[i] < data['Close'].iloc[i-4]):
            data['td_buy_setup'].iloc[i] = data['td_buy_setup'].iloc[i-1] + 1
        else:
            data['td_buy_setup'].iloc[i] = 0
            
        if (data['Close'].iloc[i] > data['Close'].iloc[i-4]):
            data['td_sell_setup'].iloc[i] = data['td_sell_setup'].iloc[i-1] + 1
        else:
            data['td_sell_setup'].iloc[i] = 0
    
    return data

sp500 = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
tickers = sp500['Symbol'].tolist()
tickers = list(map(lambda x: x.replace('.', '-'), tickers))

for ticker in tickers:
    try:
        data = fetch_data(ticker)
        data = td_sequential(data)
        if data['td_buy_setup'].iloc[-1] == 9:
            print(f'{ticker} is on a TD Buy Setup 9')
    except Exception:
        pass
