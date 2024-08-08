from fetch_data import fetch_data
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

def macd(data):
    data['ema_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['ema_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['macd'] = data['ema_12'] - data['ema_26']
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()
    return data

class MacdBandStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        if crossover(self.data['macd'], self.data['signal']):
            self.buy()
        if crossover(self.data['signal'], self.data['macd']):
            self.sell()

data = fetch_data("VOO")
data = macd(data)

bt = Backtest(data, MacdBandStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()