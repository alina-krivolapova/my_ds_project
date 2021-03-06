from sqlalchemy import Column, Integer, DateTime, Numeric, String
from db import Base


class BTCRate(Base):
    __tablename__ = 'btc_rates'
    date = Column(DateTime, primary_key=True)
    open_price = Column(Numeric)
    high_price = Column(Numeric)
    low_price = Column(Numeric)
    close_price = Column(Numeric)
    volume = Column(Integer)
    market_cap = Column(Numeric)

    def __repr__(self):
        return f'<BTCRate object for date={self.date}>'


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    news_text = Column(String)

    def __repr__(self):
        return f'<News object for date={self.date}>'
