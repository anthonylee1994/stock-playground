from fetch_data import fetch_data
from backtesting import Backtest, Strategy

def bollinger_bands(data, window=20, num_std_dev=2):
    data['rolling_mean'] = data['Close'].rolling(window).mean()
    data['rolling_std'] = data['Close'].rolling(window).std()
    data['upper_band'] = data['rolling_mean'] + (data['rolling_std'] * num_std_dev)
    data['lower_band'] = data['rolling_mean'] - (data['rolling_std'] * num_std_dev)
    return data

class BollingerBandStrategy(Strategy):
    def init(self):
        super().init()

    def next(self):
        if self.data['Close'][-1] < self.data['lower_band'][-1]:
            self.buy()
        if self.data['Close'][-1] > self.data['upper_band'][-1]:
            self.position.close()

data = fetch_data("GOOG")
data = bollinger_bands(data)

bt = Backtest(data, BollingerBandStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()