from fetch_data import fetch_data
from backtesting import Backtest, Strategy

def td_sequential(data):
    buy_condition = data['Close'] < data['Close'].shift(4)
    sell_condition = data['Close'] > data['Close'].shift(4)
    data['td_buy_setup'] = buy_condition.groupby((buy_condition != buy_condition.shift()).cumsum()).cumsum()
    data['td_sell_setup'] = sell_condition.groupby((sell_condition != sell_condition.shift()).cumsum()).cumsum()
    return data

class TdSequentialStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        if 9 == self.data['td_buy_setup'][-1]:
            self.buy()
        if 9 == self.data['td_sell_setup'][-1]:
            self.sell()

data = fetch_data("VOO")
data = td_sequential(data)

bt = Backtest(data, TdSequentialStrategy,
              cash=10000, commission=.002,
              exclusive_orders=True)

output = bt.run()
print(output)
bt.plot()