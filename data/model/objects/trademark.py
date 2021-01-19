from sqlalchemy import Column, Boolean
from sqlalchemy.orm import relationship
from .common_fields import HasImage
from .intelobject import IntelObject
from .tmclassassociations import goods_association_table


class Trademark(HasImage, IntelObject):

    is_common = Column(Boolean, name='iscommon')

    goods = relationship('NiceData', secondary=goods_association_table)

    __mapper_args__ = {
        'polymorphic_identity': 3
    }
