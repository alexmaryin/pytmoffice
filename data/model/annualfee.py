from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base


class AnnualFee(Base):
    __tablename__ = 'annualfees'

    id = Column(Integer, primary_key=True, unique=True)
    year = Column(Integer, nullable=False)
    code = Column(String(45), nullable=False)
    fee = Column(Integer)

    objectType_id = Column(Integer, ForeignKey('objecttypes.id'), name='type', nullable=False, index=True)
    object_type = relationship("ObjectType", back_populates='annual_fees')
