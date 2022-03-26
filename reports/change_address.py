import os
import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate

from data.fees.trademark_fees import TrademarkFees, PatentFees
from data.model.model import Trademark, IntelObject, Legal, Person
from data.repository.db import DataBaseConnection
from data.repository.intel_repo import IntelRepository, ObjectCategory

COMMON_TM = 'templates/address_change_common_tm.docx'
REGULAR_TM = 'templates/address_change_regular_tm.docx'
PATENT = 'templates/address_change_patent.docx'
OUTPUT_DIR = 'output'


def add_common_fee(fee_table, number, holder, changes_count=1):
    fee = TrademarkFees['common_registry_change']
    fee_table['number'].append(number)
    fee_table['code'].append(fee.code)
    fee_table['amount'].append(fee.amount * changes_count)
    fee_table['payer'].append(holder)
    fee_table['description'].append(fee.get_description_for_trademark(number))


def add_regular_fee(fee_table, number, holder, changes_count=1):
    fee_registry, fee_paper = TrademarkFees['registry_change'], TrademarkFees['certificate_change']
    fee_table['number'].append(number)
    fee_table['code'].append(fee_registry.code)
    fee_table['amount'].append(fee_registry.amount * changes_count)
    fee_table['payer'].append(holder)
    fee_table['description'].append(fee_registry.get_description_for_trademark(number))
    fee_table['number'].append(number)
    fee_table['code'].append(fee_paper.code)
    fee_table['amount'].append(fee_paper.amount)
    fee_table['payer'].append(holder)
    fee_table['description'].append(fee_paper.get_description_for_trademark(number))


def add_patent_fee(fee_table, number, holder, changes_count=1):
    fee_registry, fee_patent = PatentFees['registry_change'], PatentFees['patent_change']
    fee_table['number'].append(number)
    fee_table['code'].append(fee_registry.code)
    fee_table['amount'].append(fee_registry.amount * changes_count)
    fee_table['payer'].append(holder)
    fee_table['description'].append(fee_registry.get_description_for_patent(number))
    fee_table['number'].append(number)
    fee_table['code'].append(fee_patent.code)
    fee_table['amount'].append(fee_patent.amount)
    fee_table['payer'].append(holder)
    fee_table['description'].append(fee_patent.get_description_for_patent(number))


def populate_legal_context(context: dict[str, str], holder: Legal):
    context['ogrn'] = holder.ogrn
    context['inn'] = holder.inn
    context['kpp'] = holder.kpp
    context['ceo_shortname'] = holder.ceo.get_fullname()
    context['ceo_position'] = holder.position.position


def populate_person_context(context: dict[str, str], holder: Person):
    context['ceo_shortname'] = holder.get_fullname()
    context['ceo_position'] = 'Правообладатель'


def generate_letter_from_template(obj: IntelObject, old_address, new_post=None):
    tm_template = DocxTemplate(COMMON_TM if obj.is_common else REGULAR_TM)
    template = tm_template if isinstance(obj, Trademark) else DocxTemplate(PATENT)
    context = {
        'holder_shortname': obj.holder.get_fullname(),
        'address': obj.holder.address,
        # 'post_address': trademark.post_address, # this correct, but...
        'post_address': 'Бердникову А.И., а/я 109, Москва, 109004',
        'trademark_name': obj.name,
        'trademark_number': obj.number,
        'old_address': old_address,
        'date': datetime.today().strftime('%d.%m.%Y')
    }
    if isinstance(obj.holder, Legal):
        populate_legal_context(context, obj.holder)
    else:
        populate_person_context(context, obj.holder)
    template.render(context)
    number_str = ''.join(filter(str.isdigit, obj.number))
    filename = f"{OUTPUT_DIR}/{datetime.today().strftime('%Y-%m-%d')}/{number_str}_address_change_letter.docx"
    template.save(filename)
    if template.is_saved:
        print(f"Заявление по объекту {obj.name} {obj.number} сохранено в файл {filename}")
    else:
        print(f"Не удалось сохранить заявление по объекту {obj.name} {obj.number}")


def process_objects(objects: list[IntelObject]):
    old_address = input("Введите старый адрес для заявлений: ")
    is_post_change = input("Заменить еще адрес для переписки (Д/Y - да, Н/n - нет): ")
    new_post = None
    if is_post_change in ['y', 'Y', 'д', 'Д']:
        new_post = input("Введите новый адрес для переписки: ")
    dir_name = f"{OUTPUT_DIR}/{datetime.today().strftime('%Y-%m-%d')}"
    os.makedirs(dir_name, exist_ok=True)
    fees_table = {
        'number': [],
        'code': [],
        'amount': [],
        'payer': [],
        'description': []
    }

    for index, item in enumerate(objects):
        generate_letter_from_template(item, old_address, new_post)
        # add lines to fee table
        changes_count = 1 if new_post is None else 2
        if isinstance(item, Trademark):
            if item.is_common:
                add_common_fee(fees_table, item.number, item.holder.get_fullname(), changes_count)
            else:
                add_regular_fee(fees_table, item.number, item.holder.get_fullname(), changes_count)
        else:
            add_patent_fee(fees_table, item.number, item.holder.get_fullname(), changes_count)

    fee_data = pd.DataFrame.from_dict(fees_table)
    fee_data['total_amount'] = fee_data['amount'].sum()
    fee_data.to_excel(
        f"{OUTPUT_DIR}/fees.xlsx",
        sheet_name='пошлины адрес',
        header=['ТЗ', 'код', 'сумма', 'плательщик', 'назначение платежа', 'общая сумма']
    )
    print("Работа закончена!")


def process_select(select: int) -> list[IntelObject]:
    match select:
        case 1:
            print("Выберите правообладателя по номеру:")
            holders = repo.get_entities()
            for holder in holders:
                print(f"{holder.id}: {holder.get_fullname()}")
            query = int(input("Введите номер: "))
            return repo.get_objects_by_holder(query, ObjectCategory.All)
        case 2:
            print("Выберите тип объектов по номеру:")
            object_types = repo.get_categories()
            for category in object_types:
                print(f"{category.id}: {category.name}")
            query = int(input("Введите номер: "))
            return repo.get_objects(ObjectCategory(query))
        case 3:
            numbers = input("Введите номера объектов через запятую: ").split(",")
            assert len(numbers) > 0
            return repo.get_objects_by_numbers(numbers, ObjectCategory.All)


if __name__ == '__main__':
    db = DataBaseConnection()
    repo = IntelRepository(db)
    select = int(
        input("Выберите вариант поиска, 1 - по правообладателю, 2 - по типу объектов, 3 - по номерам объектов: "))
    assert 1 <= select <= 3
    query_result = process_select(select)
    assert len(query_result) > 0
    print(f"Будет обработано {len(query_result)} объектов")
    process_objects(query_result)
