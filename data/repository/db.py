import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

connection_str = "mysql+pymysql://root:1638432768@localhost/intelobjects20?charset=utf8mb4"


class DataBaseConnection:
    def __init__(self, connect_str):
        self.engine = sa.create_engine(connect_str)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)

    def execute(self, query):
        with self.engine.begin() as connection:
            return connection.execute(sa.text(query))
