from data.model.base import *
from data.repository.db import DataBaseConnection, connection_str


def main():
    db = DataBaseConnection(connection_str)
    result = db.session.query(Group).order_by(Group.ID).all()
    for group in result:
        print(f'{group.ID}\t{group.group_name}')
        for obj in group.objects_in_group:
            print(f'\t\t- {obj.number}\t{obj.name}')


if __name__ == '__main__':
    main()
