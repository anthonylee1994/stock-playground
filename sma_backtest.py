from fetch_data import fetch_data
from backtesting.backtesting import Backtest, Strategy
from backtesting.lib import crossover

def sma(data):
    data['fast_sma'] = data['Close'].rolling(10).mean()
    data['slow_sma'] = data['Close'].rolling(30).mean()
    return data

data = fetch_data("TLT")
data = sma(data)

class SmaStrategy(Strategy):
    def init(self):
        super().init()

    def next(self):
        if crossover(self.data['fast_sma'], self.data['slow_sma']):
            self.buy()
        if crossover(self.data['slow_sma'], self.data['fast_sma']):
            self.sell()

bt = Backtest(data, SmaStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output['Return [%]'])
bt.plot()