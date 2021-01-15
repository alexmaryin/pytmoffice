from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    position = Column(String(100), nullable=False, unique=True)

    ceo_with_position = relationship('Legal', back_populates='ceo')
