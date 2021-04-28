from sqlalchemy import Table, Column, String, PrimaryKeyConstraint, create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import MONEY, VARCHAR, TIMESTAMP, NUMERIC

base = declarative_base()


class Price(base):
    __tablename__ = 'Prices'
    address = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR)
    symbol = Column(VARCHAR)
    price = Column(MONEY)

    def __init__(self, address, name, symbol, price):
        self.address = address
        self.name = name
        self.symbol = symbol
        self.price = price

class Historical(base):
    __tablename__ = 'Historical0xTableMS'
    Day = Column(TIMESTAMP, primary_key=True)
    Price = Column(NUMERIC)

    def __init__(self, Day, Price):
        self.Day = Day
        self.Price = Price

# either make new class for every new coin you want or do it in the practice data file