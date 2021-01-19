from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import declared_attr
from data.model.base import Base
from data.model.objects.tmclassassociations import goods_association_table


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
    group = relationship('Group', back_populates='objects_in_group')

    holder_id = Column(Integer, ForeignKey('entities.ID'), nullable=False, index=True)
    holder = relationship('Entity', back_populates='objects')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'intelobjects'
    }


class HasAnnualPaid:
    @declared_attr
    def year_paid(self):
        return self.__table__.c.get('yearpaid', Column(Integer, name='yearpaid'))

    @declared_attr
    def last_paid(self):
        return self.__table__.c.get('lastpaid', Column(Date, name='lastpaid'))


class HasImage:
    @declared_attr
    def image(self):
        return self.__table__.c.get('image', Column(LargeBinary))

    @declared_attr
    def image_preview(self):
        return self.__table__.c.get('imagepreview', Column(LargeBinary, name='imagepreview'))


class Invention(HasAnnualPaid, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 1
    }


class Design(HasAnnualPaid, HasImage, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 2
    }


class UtilityModel(HasAnnualPaid, HasImage, IntelObject):

    __mapper_args__ = {
        'polymorphic_identity': 4
    }


class Trademark(HasImage, IntelObject):

    is_common = Column(Boolean, name='iscommon')

    goods = relationship('NiceData', secondary=goods_association_table)

    __mapper_args__ = {
        'polymorphic_identity': 3
    }
