from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class ObjectType(Base):
    __tablename__ = 'objecttypes'

    id = Column(Integer, primary_key=True, unique=True)
    object_type = Column(String(150), name='objecttype', nullable=False, unique=True)

    annual_fees = relationship('AnnualFee')
    licenses = relationship('License', back_populates='type')
