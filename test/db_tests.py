import pytest
from sqlalchemy.exc import IntegrityError
from data.model.model import Group


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


def test_fail_with_similar_group_id(db_session):
    group_from_base = db_session.query(Group).first()
    group = Group(ID=group_from_base.ID, group_name='Group2')
    db_session.add(group)
    with pytest.raises(IntegrityError):
        db_session.commit()
