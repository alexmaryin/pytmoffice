import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

# connection_str = "mysql+pymysql://root:1638432768@localhost/intelobjects20?charset=utf8mb4"
connection_str = 'sqlite+pysqlite:///{0}data/base.sqlite'


class DataBaseConnection:
    def __init__(self, path_prefix=''):

        self.engine = sa.create_engine(connection_str.format(path_prefix), echo=True, future=True)
        _session = sessionmaker(bind=self.engine)
        self.session = _session()

    def execute(self, query):
        with self.engine.begin() as connection:
            return connection.execute(query)   # sa.text(query) for SQL queries
