import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

from stock_crawler import StockCrawler


def estimate(feature_names, target_name, df):
    train_df = df[df.index < '2020-01-01']
    regr = linear_model.LinearRegression(fit_intercept=False)
    model = regr.fit(train_df[feature_names], train_df[target_name])
    return (model, model.score(df[feature_names], df[target_name]),
            regr.predict(df[feature_names]))


def set_date_as_index(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)


aapl = StockCrawler('AAPL').table()
uup = StockCrawler('UUP').prices()
uup['UUP'] = uup['Close']
uup = uup[['UUP']]

df = aapl.merge(uup, left_index=True, right_index=True)
df = df[df.index >= '2010-01-01']


df['Mean'] = df['Close'].rolling(10).mean()
df['Std'] = df['Close'].rolling(1250).std()
df['Low'] = df['Mean'] - df['Std']
df['High'] = df['Mean'] + df['Std']

df.dropna(inplace=True)

model_low, confidence_low, df['Low-E'] = estimate(
    ['SPS', 'EPS', 'UUP'], 'Low', df)
model_mean, confidence_mean, df['Mean-E'] = estimate(
    ['SPS', 'EPS', 'UUP'], 'Mean', df)
model_high, confidence_high, df['High-E'] = estimate(
    ['SPS', 'EPS', 'UUP'], 'High', df)

print('[Low]')
print('Coefficient', model_low.coef_)
print('Intercept', model_low.intercept_)
print('Confidence:', confidence_low)
print('\n')

print('[Mean]')
print('Coefficient', model_mean.coef_)
print('Intercept', model_mean.intercept_)
print('Confidence:', confidence_mean)
print('\n')

print('[High]')
print('Coefficient', model_high.coef_)
print('Intercept', model_high.intercept_)
print('Confidence:', confidence_high)
print('\n')

df[['Mean', 'Mean-E', 'Low-E', 'High-E']].plot()

# df.to_csv(f'report/{symbol}.csv')
plt.show()
