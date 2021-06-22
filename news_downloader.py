""" Module to parse html with news. """

import re
import bs4
from datetime import datetime
from typing import List, Dict, Union

from parser_common import download_data_from_site

PATTERN = "https://www.theguardian.com/technology/elon-musk"


def generate_list_of_pages(num_of_pages: int) -> List[str]:
    """ Create list of pages urls based on pattern."""
    list_of_pages = list()
    list_of_pages.append(PATTERN)
    for i in range(2, num_of_pages + 1):
        list_of_pages.append(PATTERN + f"?page={i}")
    return list_of_pages


def get_date_like_datetime(text: str) -> datetime:
    """Return date in datetime format.

    Example:
        Date text is Mon 14 Jun 2021 01.12 BST"""
    return datetime.strptime(' '.join(text.split()[1:4]), '%d %b %Y')


def parse_news(url: str) -> Dict[str, Union[str, datetime]]:
    """Parse data.

     Returns list of dicts with news
     Output example:
     {'date': datetime.datetime(2021, 6, 11, 0, 0), 'news_text': 'It’s famously impossible to take...'}
     """
    src = download_data_from_site(url)
    soup = bs4.BeautifulSoup(src, "lxml")
    news = dict()
    # in other articles it's hard to identify date
    if soup.find("label", attrs={"for": "dateToggle"}):
        news["date"] = get_date_like_datetime(soup.find("label", attrs={"for": "dateToggle"}).text)
        news["news_text"] = soup.find("div",
                                      class_=re.compile(
                                          "^article-body-commercial-selector article-body-viewer-selector .*")).text
    return news


def get_news():
    """ Function to download and parse news."""
    articles = []

    for url in generate_list_of_pages(20):
        src = download_data_from_site(url)
        soup = bs4.BeautifulSoup(src, "lxml")

        # save all links to particular news
        news = set()
        for item in soup.find_all('a', {'class': re.compile(".* js-headline-text")}):
            link = item.get('href')
            if re.search('/202[0-1]', link):
                news.add(link)

        # save particular articles
        for article in news:
            parsed = parse_news(article)
            if parsed:
                articles.append(parsed)
    return articles
