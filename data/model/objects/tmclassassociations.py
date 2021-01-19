from sqlalchemy import Column, Integer, ForeignKey, Table
from data.model.base import Base


goods_association_table = Table('tmclassconnections', Base.metadata,
                                Column('id', Integer, primary_key=True, unique=True),
                                Column('classID', Integer, ForeignKey('nicedata.ID', ondelete='CASCADE', onupdate='CASCADE')),
                                Column('trademarkID', Integer, ForeignKey('intelobjects.ID', ondelete='CASCADE', onupdate='CASCADE')))
