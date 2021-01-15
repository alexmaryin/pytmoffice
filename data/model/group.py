from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Group(Base):
    __tablename__ = 'groups'

    ID = Column(Integer, primary_key=True, unique=True)
    group_name = Column(String(100), name='groupname', unique=True)

    objects_in_group = relationship('IntelObject', back_populates='group')

