from sqlalchemy import Column, Integer, Date
from sqlalchemy.dialects.mysql import MEDIUMBLOB

from .intelobject import IntelObject


class UtilityModel(IntelObject):
    year_paid = Column(Integer, name='yearpaided')
    last_paid = Column(Date, name='lastpaid')
    image = Column(MEDIUMBLOB)
    image_preview = Column(MEDIUMBLOB, name='imagepreview')

    __mapper_args__ = {
        'polymorphic_identity': 4
    }
