from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from data.model.base import Base


class IntelObject(Base):
    __tablename__ = 'intelobjects'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    number = Column(String(10), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    post_address = Column(String(300), name='postaddress')
    priority = Column(Date, nullable=False)
    register_date = Column(Date, name='registerdate', nullable=False)
    number_in_group = Column(Integer, name='gnumber')
    remark = Column(String(300))
    term = Column(Date)
    type = Column(Integer, name='objtype', nullable=False, index=True)

    group_id = Column(Integer, ForeignKey('groups.ID', ondelete='SET NULL', onupdate='SET NULL'), name='groupID', index=True)
    group = relationship('Group', back_populated='objects_in_group')

    holder_id = Column(Integer, ForeignKey('entities.ID'), nullable=False, index=True)
    holder = relationship('Entity', back_populated='objects')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'intelobjects'
    }
