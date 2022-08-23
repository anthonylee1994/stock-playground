import numpy as np
import pandas as pd
import yfinance as yf

from macrotrends_crawler import MacrotrendsCrawler


class StockCrawler:
    symbol: str
    crawler: MacrotrendsCrawler

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.crawler = MacrotrendsCrawler(symbol)

    def fundamentals(self) -> pd.DataFrame:
        pe_table = self.crawler.price_earnings_ratio()
        ps_table = self.crawler.price_sales_ratio()
        pfcf_table = self.crawler.price_fcf_ratio()
        fundamentals = pe_table.merge(ps_table, left_index=True, right_index=True, how='outer').merge(pfcf_table, left_index=True, right_index=True, how='outer')
        fundamentals['EPS'] = fundamentals['TTM Net EPS'].replace('', np.nan).astype(float)
        fundamentals['SPS'] = fundamentals['TTM Sales per Share'].replace('', np.nan).astype(float)
        fundamentals['FCF'] = fundamentals['TTM FCF per Share'].replace('', np.nan).astype(float)
        return fundamentals[['EPS', 'SPS', 'FCF']].dropna()

    def prices(self) -> pd.DataFrame:
        return yf.Ticker(self.symbol).history(period='max')

    def table(self) -> pd.DataFrame:
        df = self.prices().merge(self.fundamentals(), left_index=True, right_index=True, how='outer')
        df.fillna(method='ffill', inplace=True)
        df.dropna(inplace=True)
        return df
