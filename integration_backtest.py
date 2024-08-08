from fetch_data import fetch_data
from backtesting import Backtest, Strategy

def td_sequential(data):
    buy_condition = data['Close'] < data['Close'].shift(4)
    sell_condition = data['Close'] > data['Close'].shift(4)
    data['td_buy_setup'] = buy_condition.groupby((buy_condition != buy_condition.shift()).cumsum()).cumsum()
    data['td_sell_setup'] = sell_condition.groupby((sell_condition != sell_condition.shift()).cumsum()).cumsum()
    return data

def bollinger_bands(data, window=20, num_std_dev=2):
    data['rolling_mean'] = data['Close'].rolling(window).mean()
    data['rolling_std'] = data['Close'].rolling(window).std()
    data['upper_band'] = data['rolling_mean'] + (data['rolling_std'] * num_std_dev)
    data['lower_band'] = data['rolling_mean'] - (data['rolling_std'] * num_std_dev)
    return data

data = fetch_data("GOOG")
data = td_sequential(data)
data = bollinger_bands(data)

class IntegrationStrategy(Strategy):
    def init(self):
        super.init()

    def next(self):
        if 9 == self.data['td_buy_setup'][-1]:
            self.buy()
        if 13 == self.data['td_sell_setup'][-1]:
            self.position.close()

bt = Backtest(data, IntegrationStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()