from sqlalchemy import Column, Integer, String
from .base import Base


class NiceData(Base):
    __tablename__ = 'nicedata'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    class_number = Column(Integer, name='class', nullable=False)
    description = Column(String, name='goods', nullable=False)
