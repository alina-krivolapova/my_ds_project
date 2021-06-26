""" Module to parse html with news. """

import re
import bs4
from datetime import datetime
from typing import List, Dict, Union

from data_provider import DataProvider

URL_PATTERN = "https://www.theguardian.com/technology/elon-musk"


class NewsDataProvider(DataProvider):
    """ Class to work with news data. """

    def __init__(self):
        self.articles = []

        for url in self.generate_list_of_pages(20):
            src = self.download_data_from_site(url)
            soup = bs4.BeautifulSoup(src, "lxml")

            # save all links to particular news
            news = set()
            for item in soup.find_all('a', {'class': re.compile(".* js-headline-text")}):
                link = item.get('href')
                if re.search('/202[0-1]', link):
                    news.add(link)

            # save particular articles
            for article in news:
                parsed = self.parse_data(article)
                if parsed:
                    self.articles.append(parsed)

    @staticmethod
    def generate_list_of_pages(num_of_pages: int) -> List[str]:
        """ Create list of pages urls based on pattern."""
        list_of_pages = []
        list_of_pages.append(URL_PATTERN)
        for i in range(2, num_of_pages + 1):
            list_of_pages.append(URL_PATTERN + f"?page={i}")
        return list_of_pages

    @staticmethod
    def convert_date(text: str) -> datetime:
        """Return date in datetime format.

        Example:
            Date text is Mon 14 Jun 2021 01.12 BST"""
        return datetime.strptime(' '.join(text.split()[1:4]), '%d %b %Y')

    def parse_data(self, url: str) -> Dict[str, Union[str, datetime]]:
        """Parse data.

        Returns list of dicts with news
        Output example:
        {'date': datetime.datetime(2021, 6, 11, 0, 0), 'news_text': 'It’s famously impossible to take...'}
        """
        src = self.download_data_from_site(url)
        soup = bs4.BeautifulSoup(src, "lxml")
        news = {}
        # in other articles it's hard to identify date
        if soup.find("label", attrs={"for": "dateToggle"}):
            news["date"] = self.convert_date(soup.find("label", attrs={"for": "dateToggle"}).text)
            news["news_text"] = soup.find("div",
                                          class_=re.compile(
                                              "^article-body-commercial-selector article-body-viewer-selector .*")).text
        return news

    def get_data(self):
        """ Function to provide news."""
        return self.articles
