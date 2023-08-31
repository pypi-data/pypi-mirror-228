import datetime
import sqlalchemy
from bewe.services.databases import db_manager
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    def get_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Stock(Base):
    __tablename__ = 'stock'

    stock_id = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    stock_name = sqlalchemy.Column(sqlalchemy.String(60))
    flag = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    last_execution = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=True,
        default=datetime.datetime.strptime('2021-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
    last_price_date = sqlalchemy.Column(
        sqlalchemy.DateTime, nullable=True,
        default=datetime.datetime.strptime('2023-08-29 00:00:00', '%Y-%m-%d %H:%M:%S'))
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, stock_id, stock_name):
        self.stock_id = stock_id
        self.stock_name = stock_name

    def __repr__(self):
        return f'Stock: [{self.stock_id}, {self.stock_name}, {self.last_execution}]'


class Category(Base):
    __tablename__ = 'stock_category'

    stock_id = sqlalchemy.Column(
        sqlalchemy.String(50), sqlalchemy.ForeignKey('stock.stock_id'), nullable=False, primary_key=True)
    category = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, stock_id, category):
        self.stock_id = stock_id
        self.category = category


class StockPrice(Base):
    __tablename__ = 'stock_price'

    stock_id = sqlalchemy.Column(
        sqlalchemy.String(50), sqlalchemy.ForeignKey('stock.stock_id'), nullable=False, primary_key=True)
    date = sqlalchemy.Column(sqlalchemy.String(10), nullable=False, primary_key=True)
    open_price = sqlalchemy.Column(sqlalchemy.Float)
    close_price = sqlalchemy.Column(sqlalchemy.Float)
    max_price = sqlalchemy.Column(sqlalchemy.Float)
    min_price = sqlalchemy.Column(sqlalchemy.Float)
    volume = sqlalchemy.Column(sqlalchemy.Double)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


def create_all():
    db = db_manager.DBManager()
    Base.metadata.create_all(db.engine, checkfirst=True)


def delete_all():
    db = db_manager.DBManager()
    Base.metadata.drop_all(db.engine)


if __name__ == '__main__':
    create_all()

