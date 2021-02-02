from data.model.model import *
from data.repository.db import DataBaseConnection
from data.repository.intel_repo import IntelRepository


def main():
    db = DataBaseConnection()
    # result = db.session.query(License).order_by(License.licensorID).all()
    # for ld in result:
    #     print(f'{ld.id}\t{ld.licensor.name}\t{ld.licensee.name}')
    #     for ass in ld.objects:
    #         print(f'\t\t- {ass.object.number}\t{ass.object.name}')

    repo = IntelRepository(db)
    groups = repo.get_groups()
    print(groups)
    # print("А теперь добаим немного групп...")
    # g1 = Group(group_name='Абракадабра')
    # g2 = Group(group_name='Карбукзунки')
    # g3 = Group(group_name='Слава капсс')
    # g4 = Group(group_name='Новая папка')
    # repo.source.add_all([g1, g2, g3, g4])
    # repo.source.commit()
    pos = Position(position='генеральный директор')
    pos2 = Position(position='директор')
    pers1 = Person(name='Иван', second_name='Иванович', surname='Иванов')
    legal1 = Legal(name='ООО "Ромашка"', address='Москва', ceo=pers1, position=pos)
    repo.source.add(legal1)
    repo.source.commit()


if __name__ == '__main__':
    main()
