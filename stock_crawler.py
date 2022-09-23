from typing import List, Any

import numpy as np
import pandas as pd
import yfinance as yf

from macrotrends_crawler import MacrotrendsCrawler


class StockCrawler:
    features: list[str]
    symbol: str
    crawler: MacrotrendsCrawler
    df: pd.DataFrame

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.crawler = MacrotrendsCrawler(symbol)
        self.df = pd.DataFrame()
        self.features = []

    def add_fundamentals(self):
        pe_table = self.crawler.price_earnings_ratio()
        ps_table = self.crawler.price_sales_ratio()
        pfcf_table = self.crawler.price_fcf_ratio()
        fundamentals = pe_table.merge(ps_table, left_index=True, right_index=True, how='outer').merge(pfcf_table, left_index=True, right_index=True, how='outer')
        fundamentals['EPS'] = fundamentals['TTM Net EPS'].replace('', np.nan).astype(float)
        fundamentals['SPS'] = fundamentals['TTM Sales per Share'].replace('', np.nan).astype(float)
        fundamentals['FCF'] = fundamentals['TTM FCF per Share'].replace('', np.nan).astype(float)

        self.merge(fundamentals[['EPS', 'SPS', 'FCF']].dropna())

        return self

    def merge(self, data: pd.DataFrame):
        if self.df.empty:
            self.df = data
        else:
            self.df = self.df.merge(data, left_index=True, right_index=True, how='outer')
        return self

    def add_prices(self):
        prices = yf.Ticker(self.symbol).history(period='max')
        self.merge(prices[['Close']].dropna())
        return self

    def add_feature(self, symbol: str, rolling_period: int = 1):
        prices = yf.Ticker(symbol).history(period='max')
        prices[symbol] = prices['Close'].rolling(rolling_period).mean().dropna()
        self.merge(prices[[symbol]])
        self.features.append(symbol)
        return self

    def add_features(self, symbols: List[str], rolling_period: int = 21):
        for symbol in symbols:
            self.add_feature(symbol, rolling_period)
        return self

    def table(self) -> pd.DataFrame:
        self.df.fillna(method='ffill', inplace=True)
        self.df.dropna(inplace=True)
        return self.df
