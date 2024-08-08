from fetch_data import fetch_data
from backtesting import Backtest, Strategy

def rsi(data):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['rsi'] = 100 - (100 / (1 + rs))
    return data

class RsiStrategy(Strategy):
    def init(self):
        super.init()

    def next(self):
        if self.data['rsi'][-1] < 30:
            self.buy()
        if self.data['rsi'][-1] > 70:
            self.sell()

data = fetch_data("VOO")
data = rsi(data)

bt = Backtest(data, RsiStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()