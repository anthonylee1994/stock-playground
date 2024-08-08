import yfinance as yf

def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='max', interval='1d')
        return data
    except Exception:
        return None