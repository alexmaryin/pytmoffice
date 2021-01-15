from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from .entity import Entity


class Person(Entity):
    second_name = Column(String(45), name='secondname')
    surname = Column(String(45))
    birthdate = Column(Date)

    ceo_in_legals = relationship('Legal', back_populates='ceo')

    __mapper_args__ = {
        'polymorphic_identity': 1
    }
