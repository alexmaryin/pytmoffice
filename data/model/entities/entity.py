from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from data.model.base import Base


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    type = Column(Integer, nullable=False)
    name = Column(String(45), nullable=False, index=True)
    address = Column(String(300))

    accounts = relationship('Account', back_populated='holder')
    objects = relationship('IntelObject', back_populated='holder')
    licensor_in = relationship('License', back_populated='licensor')
    licensee_in = relationship('License', back_populated='licensee')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'entities'
    }
