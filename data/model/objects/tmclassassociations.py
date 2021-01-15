from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.model.base import Base


class GoodsAssociation(Base):
    __tablename__ = 'tmclassconnections'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    goods = relationship('NiceData')
    trademarks = relationship('Trademark')

    classID = Column(ForeignKey('nicedata.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    trademarkID = Column(ForeignKey('intelobjects.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                         index=True)
