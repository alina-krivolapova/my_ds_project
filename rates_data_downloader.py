""" Module to parse html with Bitcoin rates. """

import re
import bs4
import requests
from typing import List, Dict

LIST_OF_COLUMNS = ["date", "open_price", "high_price", "low_price", "close_price", "volume", "market_cap"]


def read_file(name: str) -> str:
    """Read data from file."""
    with open(name) as file:
        return file.read()


def download_data_from_site(data_url: str) -> str:
    """Download data from site with specified URL"""
    try:
        result = requests.get(data_url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError):
        raise ConnectionError("Cannot download data from site")


def write_to_file(name: str, content: str) -> None:
    """Write content to file."""
    with open(name, "w") as pretty_file:
        pretty_file.write(content)


def parse_rates(initial_rates: List[bs4.element.Tag]) -> List[Dict[str, str]]:
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
            day_prices[column] = text.replace(",", "")
        rates.append(day_prices)
    return rates


if __name__ == "__main__":
    src = read_file('Bitcoin price today, BTC live marketcap, chart, and info _ CoinMarketCap.html')
    # TODO: use real site data
    # src = download_data_from_site("https://coinmarketcap.com/currencies/bitcoin/historical-data/")
    soup = bs4.BeautifulSoup(src, "lxml")
    # save for future to have prettier version
    write_to_file("pretty.html", soup.prettify())
    raw_rates = soup.find('table', {'class': re.compile('^cmc-table.*')}).find("tbody").find_all("tr")
    final_rates = parse_rates(raw_rates)
