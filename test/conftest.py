import pytest
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from data.model.model import Base


@pytest.fixture(scope='session')
def db_engine():
    engine_ = sa.create_engine('sqlite+pysqlite://', echo=True, future=True)
    Base.metadata.create_all(bind=engine_)
    yield engine_
    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()