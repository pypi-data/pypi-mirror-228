import datetime
import threading

from absl import logging
from bewe.services.crawler import secret_manager
from bewe.services.databases import asset_orm
from bewe.services.databases import db_manager
from FinMind.data import data_loader
from typing import Optional

_FINMIND_KEY = 'FINMIND_API'


class FinmindWrapper:
    def __init__(self):
        self.token = secret_manager.get_secret_tokens(_FINMIND_KEY)
        self.data_loader = data_loader.DataLoader()
        self.data_loader.login_by_token(self.token)
        self.db_manager = db_manager.DBManager()

    def get_tw_stock_info(self):
        df = self.data_loader.taiwan_stock_info()

        stocks, categories = [], []
        for _, row in df.iterrows():
            stock = asset_orm.Stock(
                stock_id=row.stock_id,
                stock_name=row.stock_name
            )

            category = asset_orm.Category(
                stock_id=row.stock_id,
                category=row.industry_category
            )

            stocks.append(stock)
            categories.append(category)

        self.db_manager.update(stocks)
        self.db_manager.update(categories)

    def incremental_get_stock_price(self, limit: int = 2):
        stocks = self.db_manager.query(
            asset_orm.Stock,
            conditions={'flag': True},
            order_conditions={'last_execution': True},
            limit=limit)

        jobs = []

        for stock in stocks:
            job = threading.Thread(target=self.get_stock_price, args=(stock.stock_id, stock.last_price_date))
            job.start()
            jobs.append(job)

        for job in jobs:
            job.join()
        return

    def get_stock_price(
            self,
            stock_id: str,
            start_date: datetime.datetime,
            end_date: Optional[datetime.datetime] = None):
        if not end_date:
            end_date = datetime.datetime.now()

        date_diff = (end_date - start_date).days
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')

        if date_diff == 0:
            logging.info('Start and End are on the same date. Skip the query.')
            return

        logging.info(f'[Execution] get stock price: {stock_id}, {start_date}~{end_date}.')

        try:
            df = self.data_loader.taiwan_stock_daily(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date
            )

            prices = []
            stock = self.db_manager.query(asset_orm.Stock, {'stock_id': stock_id})[0]
            stock.last_execution = datetime.datetime.now()

            for _, row in df.iterrows():

                price = asset_orm.StockPrice(
                    stock_id=row.stock_id,
                    date=row.date,
                    open_price=row.open,
                    close_price=row.close,
                    max_price=row['max'],
                    min_price=row['min'],
                    volume=row.Trading_Volume
                )
                prices.append(price)

            if prices:
                max_price_date = datetime.datetime.strptime(
                    max(df.date.values), '%Y-%m-%d')
                stock.last_price_date = max_price_date
                self.db_manager.update(prices, flush=False)
            if not prices and date_diff >= 10:
                stock.flag = False
            self.db_manager.update([stock])

        except Exception:
            logging.exception('API reach limitation.')
