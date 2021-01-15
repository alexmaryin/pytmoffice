from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.model.base import Base


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    number = Column(String(45))
    sign_date = Column(Date, name='signdate', nullable=False)
    registered = Column(Boolean)
    register_date = Column(Date, name='regdate')
    reg_number = Column(String(15), name='regnumber')
    term = Column(Date)
    unlimited = Column(Boolean)
    terminated = Column(Boolean)
    terminate_date = Column(Date, name='termdate')
    stage = Column(String(100))
    scan_link = Column(String(255), name='scanlink')

    type = Column(Integer, ForeignKey('objecttypes.id'), name='objtype', index=True)
    licensorID = Column(Integer, ForeignKey('entities.ID'), nullable=False, index=True)
    licensor = relationship('Entity', back_populated='licensor_in')
    licenseeID = Column(Integer, ForeignKey('entities.ID'), nullable=False, index=True)
    licensee = relationship('Entity', back_populated='licensee_in')
    objects = relationship('LicenseAssociation')
