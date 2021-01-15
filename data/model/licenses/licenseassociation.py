from sqlalchemy import Column, Integer, ForeignKey, Float

from data.model.base import Base


class LicenseAssociation(Base):
    __tablename__ = 'licenseconnections'

    id = Column(Integer, name='ID', primary_key=True, unique=True)
    license_id = Column(Integer, ForeignKey('licenses.ID', ondelete='CASCADE', onupdate='CASCADE'), name='licenseID',
                        nullable=False, index=True)
    object_id = Column(Integer, ForeignKey('intelobjects.ID', ondelete='CASCADE', onupdate='CASCADE'), name='objectID',
                       nullable=False, index=True)
    payment_type = Column(Integer, name='paymenttype', nullable=False)
    payment = Column(Float, nullable=False)
