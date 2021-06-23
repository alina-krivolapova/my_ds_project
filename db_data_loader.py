from rates_data_downloader import RatesDataProvider
from news_downloader import NewsDataProvider
from db import db_session
from db_model import BTCRate, News


def save_data_to_db():
    rates = RatesDataProvider()
    news = NewsDataProvider()
    db_session.bulk_insert_mappings(BTCRate, rates.get_data())
    db_session.bulk_insert_mappings(News, news.get_data())
    # save data
    db_session.commit()


if __name__ == "__main__":
    save_data_to_db()
