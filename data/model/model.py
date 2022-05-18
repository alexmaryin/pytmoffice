import pymorphy2
from pymorphy2 import MorphAnalyzer
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Table, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declared_attr, deferred


Base = declarative_base()


def list_to_gent(morph: MorphAnalyzer, source: list[str]) -> list[str]:
    # print(f'Inflecting list of {source}')
    return [morph.parse(word)[0].inflect({'gent'}).word for word in source]


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    account_number = Column(String(20), name='accountnumber', nullable=False)
    corr_number = Column(String(20), name='korrnumber')
    bic = Column(String(9))
    bank = Column(String(300), nullable=False)
    swift = Column(String(15))
    is_current = Column(Boolean, name="iscurrent")

    holder_id = Column(Integer, ForeignKey('entities.id'), name="holderid", nullable=False, index=True)
    holder = relationship('Entity', back_populates='accounts')


class AnnualFee(Base):
    __tablename__ = 'annualfees'

    id = Column(Integer, primary_key=True, unique=True)
    year = Column(Integer, nullable=False)
    code = Column(String(45), nullable=False)
    fee = Column(Integer)

    objectType_id = Column(Integer, ForeignKey('objecttypes.id'), name='objecttype', nullable=False, index=True)
    object_type = relationship("ObjectType", lazy='joined')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    group_name = Column(String(100), name='groupname', unique=True)

    objects_in_group = relationship('IntelObject', back_populates='group')


class NiceData(Base):
    __tablename__ = 'nicedata'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    class_number = Column(Integer, name='class', nullable=False)
    description = Column(String, name='goods', nullable=False)


class ObjectType(Base):
    __tablename__ = 'objecttypes'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(150), name='objecttype', nullable=False, unique=True)


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    position = Column(String(100), nullable=False, unique=True)


class Entity(Base):
    __tablename__ = 'entities'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    type = Column(Integer, nullable=False)
    name = Column(String(45), nullable=False, index=True)
    address = Column(String(300))
    inn = Column(String(10))

    accounts = relationship('Account', back_populates='holder')
    objects = relationship('IntelObject', back_populates='holder')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'entities'
    }

    def get_fullname(self) -> str:
        raise NotImplementedError

    def get_shortname(self) -> str:
        raise NotImplementedError

    def get_ceo_gent(self) -> str:
        raise NotImplementedError

    def get_ceo_type_gent(self) -> str:
        raise NotImplementedError

    def get_requisities(self) -> str:
        raise NotImplementedError

    def get_req_line(self) -> str:
        raise NotImplementedError

    def get_ceo_shortname(self) -> str:
        raise NotImplementedError


class Legal(Entity):
    fullname = Column(String(300))
    ogrn = Column(String(13))
    kpp = Column(String(9))

    ceo_type = Column(Integer, ForeignKey('positions.id', ondelete='SET NULL', onupdate='SET NULL'), name="ceotype", index=True)
    position = relationship('Position')

    ceo_id = Column(Integer, ForeignKey('entities.id', ondelete='SET NULL', onupdate='SET NULL'), name="ceoID", index=True)
    ceo = relationship('Person', remote_side=[Entity.id])

    def get_fullname(self) -> str:
        return str(self.fullname) or str(self.name)

    def get_shortname(self) -> str:
        return str(self.name)

    def get_ceo_shortname(self) -> str:
        return self.ceo.get_ceo_shortname()

    def get_ceo_gent(self) -> str:
        return self.ceo.get_ceo_gent()

    def get_ceo_type_gent(self) -> str:
        morph = pymorphy2.MorphAnalyzer()
        result = list_to_gent(morph, self.position.position.split())
        return ' '.join(result)

    def get_req_line(self) -> str:
        return f'ОГРН: {self.ogrn}, ИНН: {self.inn}, КПП: {self.kpp}'

    def get_requisities(self) -> str:
        return '\n'.join([
            str(self.name),
            str(self.address),
            f'ОГРН: {self.ogrn}',
            f'ИНН/КПП: {self.inn}/{self.kpp}'
        ])

    __mapper_args__ = {
        'polymorphic_identity': 2
    }


class Person(Entity):
    second_name = Column(String(45), name='secondname')
    surname = Column(String(45))
    birthdate = Column(Date)

    def get_fullname(self) -> str:
        return ' '.join([self.surname or '', self.name or '', self.second_name or ''])

    def get_shortname(self) -> str:
        return self.get_ceo_shortname()

    def get_ceo_shortname(self) -> str:
        return '. '.join([self.name[0] or '', self.second_name[0] or '', self.surname or ''])

    def get_ceo_type_gent(self) -> str:
        pass

    def get_req_line(self) -> str:
        return f'ИНН: {self.inn}'

    def get_ceo_gent(self) -> str:
        morph = pymorphy2.MorphAnalyzer()
        morph_list = list(filter(lambda s: len(s.strip()) > 0, [str(self.name), str(self.second_name), str(self.surname)]))
        result = list_to_gent(morph, morph_list)
        return (' '.join(result)).title()

    def get_requisities(self) -> str:
        pass

    __mapper_args__ = {
        'polymorphic_identity': 1
    }


goods_association_table = Table('tmclassconnections', Base.metadata,
                                Column('id', Integer, primary_key=True, unique=True),
                                Column('classid', Integer, ForeignKey('nicedata.id', ondelete='CASCADE', onupdate='CASCADE')),
                                Column('trademarkid', Integer, ForeignKey('intelobjects.id', ondelete='CASCADE', onupdate='CASCADE')))


class IntelObject(Base):
    __tablename__ = 'intelobjects'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    number = Column(String(10), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    post_address = Column(String(300), name='postaddress')
    priority = Column(Date, nullable=False)
    register_date = Column(Date, name='registerdate', nullable=False)
    number_in_group = Column(Integer, name='gnumber')
    remark = Column(String(300))
    term = Column(Date)
    type = Column(Integer, name='objtype', nullable=False, index=True)

    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL', onupdate='SET NULL'), name='groupid', index=True)
    group = relationship('Group', back_populates='objects_in_group')

    holder_id = Column(Integer, ForeignKey('entities.id'), name="holderid", nullable=False, index=True)
    holder = relationship('Entity', back_populates='objects')

    def short_description(self) -> str:
        raise NotImplementedError


    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'intelobjects'
    }


class HasAnnualPaid:
    @declared_attr
    def year_paid(self):
        return self.__table__.c.get('yearpaided', Column(Integer, name='yearpaided'))

    @declared_attr
    def last_paid(self):
        return self.__table__.c.get('lastpaid', Column(Date, name='lastpaid'))


class HasImage:
    @declared_attr
    def image(self):
        return self.__table__.c.get('image', deferred(Column(LargeBinary)))

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
        'polymorphic_identity': 3
    }


class Trademark(HasImage, IntelObject):

    is_common = Column(Boolean, name='iscommon')

    goods = relationship('NiceData', secondary=goods_association_table)

    def short_description(self) -> str:
        goods = ', '.join([f'{good.class_number} класс МКТУ: {good.description.decode("utf-8")}' for good in self.goods])
        return f'№{self.number} "{self.name}", приоритет: {self.priority.strftime("%d.%m.%Y г.")}, зарегистрирован: {self.register_date.strftime("%d.%m.%Y г.")}, действует в отношении следующих товаров и услуг: {goods};'

    __mapper_args__ = {
        'polymorphic_identity': 0
    }


class LicenseAssociation(Base):
    __tablename__ = 'licenseconnections'

    id = Column(Integer, name='id', primary_key=True, unique=True)
    license_id = Column(Integer, ForeignKey('licenses.id', ondelete='CASCADE', onupdate='CASCADE'), name='licenseid',
                        nullable=False, index=True)
    object_id = Column(Integer, ForeignKey('intelobjects.id', ondelete='CASCADE', onupdate='CASCADE'), name='objectid',
                       nullable=False, index=True)
    object = relationship('IntelObject', lazy='joined')
    payment_type = Column(Integer, name='paymenttype', nullable=False)
    payment = Column(Float, nullable=False)


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, name='id', primary_key=True, unique=True)
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

    licensorID = Column(Integer, ForeignKey('entities.id'), nullable=False, index=True)
    licensor = relationship('Entity', foreign_keys=[licensorID], lazy='joined')

    licenseeID = Column(Integer, ForeignKey('entities.id'), nullable=False, index=True)
    licensee = relationship('Entity', foreign_keys=[licenseeID], lazy='joined')

    objects = relationship('LicenseAssociation', lazy='subquery')

