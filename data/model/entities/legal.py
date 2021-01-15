from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .entity import Entity


class Legal(Entity):
    fullname = Column(String(300))
    ogrn = Column(String(13))
    inn = Column(String(10))
    kpp = Column(String(9))

    ceo_type = Column(Integer, ForeignKey('positions.ID', ondelete='SET NULL', onupdate='SET NULL'), index=True)
    position = relationship('Position', back_populates='ceo_with_position')

    ceo_id = Column(Integer, ForeignKey('entities.ID', ondelete='SET NULL', onupdate='SET NULL'), index=True)
    ceo = relationship('Person', back_populates='ceo_in_legals')

    __mapper_args__ = {
        'polymorphic_identity': 2
    }
