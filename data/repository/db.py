import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

connection_str = "mysql+pymysql://root:1638432768@localhost/intelobjects20?charset=utf8mb4"
test_connection_str = 'sqlite+pysqlite:///data/base.sqlite'


class DataBaseConnection:
    def __init__(self):
        try:
            print('Connecting to working database on mySQL...')
            self.engine = sa.create_engine(connection_str, pool_pre_ping=True, echo=True, future=True)
            c = self.engine.connect()
            c.close()
        except DBAPIError:
            print('Failed to connect. Connect to develop version of base sqlite...')
            self.engine = sa.create_engine(test_connection_str, echo=True, future=True)
        finally:
            _session = sessionmaker(bind=self.engine)
            self.session = _session()

    def execute(self, query):
        with self.engine.begin() as connection:
            return connection.execute(query)  # sa.text(query) for SQL queries
