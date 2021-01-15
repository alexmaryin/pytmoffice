from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    account_number = Column(String(20), name='accountnumber', nullable=False)
    corr_number = Column(String(20), name='korrnumber')
    bic = Column(String(9))
    bank = Column(String(300), nullable=False)
    swift = Column(String(15))
    is_current = Column(Boolean)

    holder_id = Column(Integer, ForeignKey('entities.ID'), nullable=False, index=True)
    holder = relationship('Entity', back_populated='accounts')
