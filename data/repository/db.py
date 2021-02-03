import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

connection_str = "mysql+pymysql://root:1638432768@localhost/intelobjects20?charset=utf8mb4"
test_connection_str = 'sqlite+pysqlite:///data/base.sqlite'


class DataBaseConnection:
    def __init__(self):

        self.engine = sa.create_engine(connection_str, echo=True, future=True)
        _session = sessionmaker(bind=self.engine)
        self.session = _session()

    def execute(self, query):
        with self.engine.begin() as connection:
            return connection.execute(query)   # sa.text(query) for SQL queries
