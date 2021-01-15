from sqlalchemy import Column, Boolean
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.orm import relationship
from .intelobject import IntelObject
from .tmclassassociations import goods_association_table


class Trademark(IntelObject):
    image = Column(MEDIUMBLOB)
    image_preview = Column(MEDIUMBLOB, name='imagepreview')
    is_common = Column(Boolean, name='iscommon')

    goods = relationship('NiceData', secondary=goods_association_table)

    __mapper_args__ = {
        'polymorphic_identity': 3
    }
