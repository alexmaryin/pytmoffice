from sqlalchemy import Column, Integer, Date
from .intelobject import IntelObject


class Invention(IntelObject):
    year_paid = Column(Integer, name='yearpaided')
    last_paid = Column(Date, name='lastpaid')

    __mapper_args__ = {
        'polymorphic_identity': 1
    }
