import pytest
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

from data.model.model import Base, Group


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


def test_database_should_be_created(db_session):
    groups = db_session.query(Group).all()
    assert groups == []


def test_new_group_should_be_added(db_session):
    group = Group(group_name='Group1')
    db_session.add(group)
    db_session.commit()
    group_from_base = db_session.query(Group).first()
    print(group_from_base.ID, group_from_base.group_name)
    assert group.group_name == group_from_base.group_name
