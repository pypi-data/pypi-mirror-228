from bewe.services.crawler import secret_manager
from sqlalchemy import orm
from google.cloud.sql.connector import Connector, IPTypes
from typing import Any, Sequence, Mapping, Optional
import pymysql
import sqlalchemy
import os


DB_NAME_KEY = 'DB_NAME'
DB_USER_KEY = 'DB_USER'
DB_PASS_KEY = 'DB_PASS'
INSTANCE_KEY = 'DB_INSTANCE'


class DBManager:
    def __init__(self):
        self.instance = secret_manager.get_secret_tokens(INSTANCE_KEY)
        self.engine = sqlalchemy.create_engine(
            'mysql+pymysql://',
            creator=self.get_conn,
            pool_size=50,
            max_overflow=100
        )

    def get_conn(self) -> pymysql.connections.Connection:
        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
        connector = Connector(ip_type)
        conn: pymysql.connections.Connection = connector.connect(
            self.instance,
            'pymysql',
            user=secret_manager.get_secret_tokens(DB_USER_KEY),
            password=secret_manager.get_secret_tokens(DB_PASS_KEY),
            db=secret_manager.get_secret_tokens(DB_NAME_KEY)
        )
        return conn

    def query(
            self,
            entity: orm.DeclarativeBase,
            conditions: Optional[Mapping[str, Any]] = None,
            order_conditions: Optional[Mapping[str, bool]] = None,
            limit: Optional[int] = None
    ):

        if not conditions:
            conditions = {}

        if not order_conditions:
            order_conditions = []

        session = orm.Session(self.engine)
        q = session.query(entity)

        for attr, value in conditions.items():
            q = q.filter(getattr(entity, attr) == value)

        for attr, asc in order_conditions.items():
            if asc:
                q = q.order_by(getattr(entity, attr))
            else:
                q = q.order_by(getattr(entity, attr).desc())

        if limit:
            q = q.limit(limit)

        executions = session.execute(q)
        results = []

        for obj in executions.scalars():
            results.append(obj)

        return results

    def insert(self, records: Sequence[orm.DeclarativeBase]):

        with orm.Session(self.engine) as session:
            for record in records:
                session.add(record)
            session.commit()

    def update(self, records: Sequence[orm.DeclarativeBase], flush=True):
        with orm.Session(self.engine, autoflush=flush) as session:
            for record in records:
                session.merge(record)
            session.commit()

    @staticmethod
    def _chunk(records: Sequence[orm.DeclarativeBase], n=10):
        results = []

        for i in range(0, len(records), n):
            results.append(records[i:i+n])
        return results
