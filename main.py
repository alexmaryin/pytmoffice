from data.model.nicedata import NiceData
from data.model.objecttype import ObjectType
from data.model.annualfee import AnnualFee
from data.model.licenses.license import License
from data.repository.db import *


def main():
    db = DataBaseConnection(connection_str)
    result = db.session.query(NiceData).all()
    for nicedata in result.scalars():
        print(f'{nicedata.class_number}:\t{nicedata.description}')


if __name__ == '__main__':
    main()
