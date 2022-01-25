import os
from datetime import datetime
from docxtpl import DocxTemplate
from data.repository.db import DataBaseConnection
from data.repository.intel_repo import IntelRepository, ObjectCategory


COMMON_TM = 'templates/address_change_common_tm.docx'
REGULAR_TM = 'templates/address_change_regular_tm.docx'
OUTPUT_DIR = 'output'


def trademarks_by_holder(repo: IntelRepository, holder_id: int):
    trademarks = repo.get_objects_by_holder(holder_id, ObjectCategory.Trademarks)
    print(f"Актуальный адрес правообладателя:\n{trademarks[0].holder.address}")
    old_address = input("Введите старый адрес для заявлений: ")
    dir_name = f"{OUTPUT_DIR}/{datetime.today().strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)
    for trademark in trademarks:
        template = DocxTemplate(COMMON_TM if trademark.is_common else REGULAR_TM)
        context = {
            'holder_shortname': trademark.holder.get_fullname(),
            'ogrn': trademark.holder.ogrn,
            'inn': trademark.holder.inn,
            'kpp': trademark.holder.kpp,
            'address': trademark.holder.address,
            # 'post_address': trademark.post_address, # this correct, but...
            'post_address': 'Бердникову А.И., а/я 109, Москва, 109004',
            'trademark_name': trademark.name,
            'trademark_number': trademark.number,
            'old_address': old_address,
            'ceo_shortname': trademark.holder.ceo.get_fullname(),
            'ceo_position': trademark.holder.position.position,
            'date': datetime.today().strftime('%d.%m.%Y')
        }
        template.render(context)
        filename = f"{OUTPUT_DIR}/{datetime.today().strftime('%Y-%m-%d')}/{trademark.number}_address_change_letter.docx"
        template.save(filename)
        if template.is_saved:
            print(f"Заявление по товарному знаку {trademark.name} {trademark.number} сохранено в файл {filename}")
        else:
            print(f"Не удалось сохранить заявление по товарному знаку {trademark.name} {trademark.number}")
    print("Работа закончена!")


if __name__ == '__main__':
    db = DataBaseConnection()
    repo = IntelRepository(db)
    print("Выберите правообладателя по номеру:")
    holders = repo.get_entities()
    for holder in holders:
        print(f"{holder.id}: {holder.get_fullname()}")
    query = int(input("Введите номер: "))
    trademarks_by_holder(repo, query)

