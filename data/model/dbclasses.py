from sqlalchemy import Column, Date, Float, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB, TINYINT
from sqlalchemy.orm import relationship

class License(Base):
    __tablename__ = 'licenses'

    ID = Column(INTEGER(11), primary_key=True, unique=True)
    licensorID = Column(ForeignKey('entities.ID'), nullable=False, index=True)
    licenseeID = Column(ForeignKey('entities.ID'), nullable=False, index=True)
    signdate = Column(Date, nullable=False)
    registered = Column(TINYINT(1))
    regdate = Column(Date)
    regnumber = Column(String(15))
    term = Column(Date)
    unlimited = Column(TINYINT(1))
    terminated = Column(TINYINT(1))
    termdate = Column(Date)
    stage = Column(String(100))
    scanlink = Column(String(255))
    oldID = Column(INTEGER(11))
    number = Column(String(45))
    objtype = Column(ForeignKey('objecttypes.id'), index=True)

    objects = relationship('Licenseconnection')


class Licenseconnection(Base):
    __tablename__ = 'licenseconnections'

    ID = Column(INTEGER(11), primary_key=True, unique=True)
    licenseID = Column(ForeignKey('licenses.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    objectID = Column(ForeignKey('intelobjects.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    paymenttype = Column(TINYINT(1), nullable=False)
    payment = Column(Float, nullable=False)

