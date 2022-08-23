import matplotlib.pyplot as plt
import pandas as pd

from estimator import Estimator
from stock_crawler import StockCrawler

symbol = 'AMZN'
training_upto: str = '2017-12-31'
fit_intercept: bool = False
pd.options.mode.chained_assignment = None

base_features = ['SPS']

crawler = StockCrawler(symbol)

df = crawler \
    .add_fundamentals() \
    .add_prices() \
    .add_feature('UUP', 21) \
    .table()

df = df[df.index >= '2010-01-01']

df['Mean'] = df['Close'].rolling(21).mean()
df['Std'] = df['Close'].rolling(252).std()
df['Low'] = df['Mean'] - df['Std']
df['High'] = df['Close'] + df['Std']

df.dropna(inplace=True)

all_features = base_features + crawler.features

print('[LOW]')
df['Low-E'] = Estimator(all_features, 'Low', training_upto, df, fit_intercept).estimate()

print('[MEAN]')
df['Mean-E'] = Estimator(all_features, 'Mean', training_upto, df, fit_intercept).estimate()

print('[HIGH]')
df['High-E'] = Estimator(all_features, 'High', training_upto, df, fit_intercept).estimate()

df[['Mean', 'Mean-E', 'Low-E', 'High-E']].plot()

plt.show()
