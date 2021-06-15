from rates_data_downloader import get_rates
from db import db_session
from db_model import BTCRate


def save_data_to_db():
    db_session.bulk_insert_mappings(BTCRate, get_rates())
    db_session.commit()


if __name__ == "__main__":
    save_data_to_db()
