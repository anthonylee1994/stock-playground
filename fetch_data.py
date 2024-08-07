import yfinance as yf

def fetch_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1mo', interval='5m')
        return data
    except Exception:
        return None