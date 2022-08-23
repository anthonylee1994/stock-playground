from __future__ import annotations
import requests
import pandas as pd
from bs4 import BeautifulSoup, NavigableString


class MacrotrendsCrawler:
    baseURL: str

    def __init__(self, symbol: str):
        self.baseURL = f'https://www.macrotrends.net/stocks/charts/{symbol}/xxx'

    def price_earnings_ratio(self) -> pd.DataFrame:
        return MacrotrendsCrawler.data(self.html('pe-ratio'))

    def price_sales_ratio(self) -> pd.DataFrame:
        return MacrotrendsCrawler.data(self.html('price-sales'))

    def price_fcf_ratio(self) -> pd.DataFrame:
        return MacrotrendsCrawler.data(self.html('price-fcf'))

    def html(self, category: str) -> str:
        return requests.get(f'{self.baseURL}/{category}').text

    @staticmethod
    def data(html: str) -> pd.DataFrame:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table"})

        if (not table) or isinstance(table, NavigableString):
            raise Exception('No data found')

        soup_col_headers = table.select("thead th:not([colspan='4'])")

        headers = []
        for header in soup_col_headers:
            headers.append(header.text)

        rows = []
        soup_rows = table.select("tbody tr")

        for soup_row in soup_rows:
            row = {}
            cells = soup_row.select("td")
            for i in range(len(cells)):
                row[headers[i]] = cells[i].text.replace('$', '')
            rows.append(row)

        return MacrotrendsCrawler.to_dataframe(headers, rows)

    @staticmethod
    def to_dataframe(headers, rows):
        df = pd.DataFrame()
        for header in headers:
            df[header] = [row[header] for row in rows]
        MacrotrendsCrawler.set_date_as_index(df)
        return df

    @staticmethod
    def set_date_as_index(df: pd.DataFrame):
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
