from data.model.base import Base
from data.model.nicedata import NiceData
from data.model.objecttype import ObjectType
from data.model.annualfee import AnnualFee
from data.model.account import Account
from data.model.group import Group
from data.model.position import Position
from data.model.licenses.license import License
from data.model.licenses.licenseassociation import LicenseAssociation
from data.model.entities.entity import Entity
from data.model.entities.legal import Legal
from data.model.entities.person import Person
from data.model.objects.intelobject import *
from data.repository.db import *


def main():
    db = DataBaseConnection(connection_str)
    meta = Base.metadata
    meta.create_all(bind=db.engine)


if __name__ == '__main__':
    main()
