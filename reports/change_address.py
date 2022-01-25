import os
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from data.repository.db import DataBaseConnection
from data.repository.intel_repo import IntelRepository, ObjectCategory


COMMON_TM = 'templates/address_change_common_tm.docx'
REGULAR_TM = 'templates/address_change_regular_tm.docx'
OUTPUT_DIR = 'output'


def add_common_fee(fee_table, number, holder):
    fee_table['number'].append(number)
    fee_table['code'].append('2.18')
    fee_table['amount'].append(4800)
    fee_table['payer'].append(holder)
    fee_table['description'].append(f"2.18. Пошлина за внесение изменений в Перечень общеизвестных товарных знаков в части адреса правобладателя и выдачу свидетельства на бумажном носителе. Свидетельство N{number}. 4800 р. НДС не облагается.")


def add_regular_fee(fee_table, number, holder):
    fee_table['number'].append(number)
    fee_table['code'].append('2.16')
    fee_table['amount'].append(2800)
    fee_table['payer'].append(holder)
    fee_table['description'].append(f"2.16. Пошлина за внесение изменений в Реестр товарных знаков в части адреса правобладателя. Свидетельство N{number}. 2800 р. НДС не облагается.")
    fee_table['number'].append(number)
    fee_table['code'].append('2.17')
    fee_table['amount'].append(4000)
    fee_table['payer'].append(holder)
    fee_table['description'].append(f"2.17. Пошлина за внесение изменений в Свидетельство на товарный знак N{number} в части адреса правообладателя и выдачу свидетельства на бумажном носителе. 4000 р. НДС не облагается.")


def trademarks_by_holder(repo: IntelRepository, holder_id: int):
    trademarks = repo.get_objects_by_holder(holder_id, ObjectCategory.Trademarks)
    print(f"Актуальный адрес правообладателя:\n{trademarks[0].holder.address}")
    old_address = input("Введите старый адрес для заявлений: ")
    dir_name = f"{OUTPUT_DIR}/{datetime.today().strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)
    fees_table = {
        'number': [],
        'code': [],
        'amount': [],
        'payer': [],
        'description': []
    }
    for index, trademark in enumerate(trademarks):

        # generate application from template
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

        # add lines to fee table
        if trademark.is_common:
            add_common_fee(fees_table, trademark.number, trademark.holder.get_fullname())
        else:
            add_regular_fee(fees_table, trademark.number, trademark.holder.get_fullname())

    fee_data = pd.DataFrame.from_dict(fees_table)
    fee_data['total_amount'] = fee_data['amount'].sum()
    fee_data.to_excel(
        f"{OUTPUT_DIR}/fees.xlsx",
        sheet_name='пошлины адрес',
        header=['ТЗ', 'код', 'сумма', 'плательщик', 'назначение платежа', 'общая сумма']
    )
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

