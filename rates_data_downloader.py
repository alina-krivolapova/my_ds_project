""" Module to parse html with Bitcoin rates. """

import re
import bs4
from datetime import datetime
from typing import List, Dict

from data_provider import DataProvider

LIST_OF_COLUMNS = ["date", "open_price", "high_price", "low_price", "close_price", "volume", "market_cap"]


class RatesDataProvider(DataProvider):
    """ Class to work with rates data. """

    def __init__(self):
        # use local downloaded file
        src = self.read_file('Bitcoin price today, BTC live marketcap, chart, and info _ CoinMarketCap.html')
        soup = bs4.BeautifulSoup(src, "lxml")
        # save for future to have prettier version
        self.write_to_file("pretty_rates.html", soup.prettify())
        self.raw_rates = soup.find('table', {'class': re.compile('^cmc-table.*')}).find("tbody").find_all("tr")

    @staticmethod
    def get_date_like_datetime(text: str) -> datetime:
        """ Change format for date field."""
        return datetime.strptime(text, '%b %d, %Y')

    def parse_data(self, initial_rates: List[bs4.element.Tag]) -> List[Dict[str, str]]:
        """Parse data.

        Returns list of dicts with prices for each day in downloaded period.
        Output example:
        {'date': 'Jun 05 2021', 'open_price': '36880.16', 'high_price': '37917.71', 'low_price': '34900.41',
        'close_price': '35551.96', 'volume': '35959473399', 'market_cap': '665804639833'}
        """
        rates = []
        for rate in initial_rates:
            day_prices = {}
            for value, column in zip(rate.find_all("td"), LIST_OF_COLUMNS):
                text = value.text.split("$")[1] if value.text.startswith("$") else value.text
                if column == "date":
                    day_prices[column] = self.get_date_like_datetime(text)
                else:
                    day_prices[column] = text.replace(",", "")
            rates.append(day_prices)
        return rates

    def get_data(self) -> List[Dict[str, str]]:
        """ Function to provide rates data."""
        return self.parse_data(self.raw_rates)
