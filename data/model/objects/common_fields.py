from sqlalchemy import Column, Integer, Date
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.orm.decl_api import declared_attr


class HasAnnualPaid:
    @declared_attr
    def year_paid(self):
        return self.__table__.c.get('yearpaid', Column(Integer))

    @declared_attr
    def last_paid(self):
        return self.__table__.c.get('lastpaid', Column(Date))


class HasImage:
    @declared_attr
    def image(self):
        return self.__table__.c.get('image', Column(MEDIUMBLOB))

    @declared_attr
    def image_preview(self):
        return self.__table__.c.get('imagepreview', Column(MEDIUMBLOB))
