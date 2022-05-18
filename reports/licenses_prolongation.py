import datetime
import os

import pandas as pd
from docxtpl import DocxTemplate, Listing

from data.fees.trademark_fees import TrademarkFees
from data.model.model import License, Entity, Legal, Trademark, Invention, Design, UtilityModel
from data.repository.db import DataBaseConnection
from data.repository.intel_repo import IntelRepository

OUTPUT_DIR = f"output/{datetime.date.today().strftime('%Y-%m-%d')}"
PROLONG_TM_AGREEMENT = 'templates/prolong_trademarks_agreement.docx'
PROLONG_TM_APPLICATION = 'templates/license_changes_application.docx'
POST_ADDRESS = 'Бердникову А.И., а/я 109, Москва, 109004'


def add_prolong_tm_fee(fee_table, agr_number, payer, registered_number, registered_date):
    fee = TrademarkFees['additional_agreement_simple']
    fee_table['number'].append(agr_number)
    fee_table['code'].append(fee.code)
    fee_table['payer'].append(payer)
    fee_table['amount'].append(fee.amount)
    fee_table['description'].append(f'{fee.code}. {fee.description} Регистрация N{registered_number} от {registered_date}. НДС не облагается.')


def populate_license_data(context: dict[str, str], license: License):
    context['agr_num'] = license.number or license.id
    context['agr_concluded'] = license.sign_date.strftime('%d.%m.%Y г.')
    context['agr_reg_num'] = license.reg_number
    context['agr_reg_date'] = license.register_date.strftime('%d.%m.%Y г.')
    context['add_date'] = datetime.date.today().strftime('%d.%m.%Y г.')
    context['trademarks'] = '\n'.join([obj.object.short_description() for obj in license.objects])


def populate_parties_data(context: dict[str, str], licensor: Entity, licensee: Entity):
    context['licensor_name'] = licensor.get_fullname()
    context['licensee_name'] = licensee.get_fullname()
    context['lr_ceo_type_gent'] = licensor.get_ceo_type_gent()
    context['lr_ceo_name_gent'] = licensor.get_ceo_gent()
    context['le_ceo_type_gent'] = licensee.get_ceo_type_gent()
    context['le_ceo_name_gent'] = licensee.get_ceo_gent()
    context['lr_requisities'] = licensor.get_requisities()
    context['le_requisities'] = licensee.get_requisities()
    context['lr_ceo_nom'] = licensor.position.position
    context['le_ceo_nom'] = licensee.position.position
    context['lr_ceo_shortname'] = licensor.get_ceo_shortname()
    context['le_ceo_shortname'] = licensee.get_ceo_shortname()


def populate_entity_data(context: dict[str, str], prefix: str, entity: Entity):
    context[f'{prefix}_shortname'] = entity.get_shortname()
    context[f'{prefix}_name'] = entity.get_fullname()
    context[f'{prefix}_req'] = entity.get_req_line()
    context[f'{prefix}_inn'] = str(entity.inn)
    context[f'{prefix}_address'] = str(entity.address)
    context[f'{prefix}_post_address'] = POST_ADDRESS
    context[f'{prefix}_ceo_shortname'] = entity.get_ceo_shortname()
    if isinstance(entity, Legal):
        context[f'{prefix}_is_legal'] = 'true'
        context[f'{prefix}_ogrn'] = str(entity.ogrn)
        context[f'{prefix}_kpp'] = str(entity.kpp)
        context[f'{prefix}_ceo_position'] = str(entity.position.position)
    else:
        context[f'{prefix}_is_person'] = 'true'
        context[f'{prefix}_ceo_position'] = 'индивидуальный предприниматель'


def populate_application_data(context: dict[str, str], license: License, new_term, payer_is_licensee):
    populate_entity_data(context, 'licensor', license.licensor)
    populate_entity_data(context, 'licensee', license.licensee)
    context['reg_num'] = license.reg_number
    context['reg_date'] = license.register_date.strftime('%d.%m.%Y г.')
    context['tm_numbers'] = ', '.join([
        obj.object.number for obj in license.objects if isinstance(obj.object, Trademark) and not obj.object.is_common
    ])
    context['ctm_numbers'] = ', '.join([
        obj.object.number for obj in license.objects if isinstance(obj.object, Trademark) and obj.object.is_common
    ])
    context['inv_numbers'] = ', '.join([
        obj.object.number for obj in license.objects if isinstance(obj.object, Invention)
    ])
    context['dsn_numbers'] = ', '.join([
        obj.object.number for obj in license.objects if isinstance(obj.object, Design)
    ])
    context['um_numbers'] = ', '.join([
        obj.object.number for obj in license.objects if isinstance(obj.object, UtilityModel)
    ])
    context['defined_term'] = 'true'
    context['date_term'] = new_term.strftime('%d.%m.%Y г.')
    if payer_is_licensee:
        populate_entity_data(context, 'payer', license.licensee)
    else:
        populate_entity_data(context, 'payer', license.licensor)


def generate_agreement(license: License, term):
    template = DocxTemplate(PROLONG_TM_AGREEMENT)
    context = {
        'prolong_term': term.strftime('%d.%m.%Y г.')
    }
    populate_license_data(context, license)
    populate_parties_data(context, license.licensor, license.licensee)
    template.render(context)
    filename = f"{OUTPUT_DIR}/{license.number or license.id}_{license.reg_number}_prolong.docx"
    template.save(filename)
    if template.is_saved:
        print(f"Дополнительное соглашение по договору {license.reg_number} сохранено в файл {filename}")
    else:
        print(f"Не удалось сохранить соглашение по договору {license.reg_number}")


def generate_application(license: License, term):
    template = DocxTemplate(PROLONG_TM_APPLICATION)
    context = {
        'date': datetime.date.today().strftime('%d.%m.%Y г.')
    }
    populate_application_data(context, license, term, True)
    template.render(context)
    filename = f"{OUTPUT_DIR}/{license.number or license.id}_{license.reg_number}_prolong_application.docx"
    template.save(filename)
    if template.is_saved:
        print(f"Заявление по договору {license.reg_number} сохранено в файл {filename}")
    else:
        print(f"Не удалось сохранить заявление по договору {license.reg_number}")


def process_licenses(licenses: list[License]):
    fees_table = {
        'number': [],
        'code': [],
        'amount': [],
        'payer': [],
        'description': []
    }

    for license in licenses:
        objects = list(filter(lambda x: x.object.term is not None, license.objects))
        if len(objects) > 0:
            smallest = min(objects, key=lambda x: x.object.term)
            generate_agreement(license, smallest.object.term)
            generate_application(license, smallest.object.term)
            add_prolong_tm_fee(fees_table, license.number or license.id, license.licensee.get_shortname(), license.reg_number, license.register_date)

    fee_data = pd.DataFrame.from_dict(fees_table)
    fee_data['total_amount'] = fee_data['amount'].sum()
    fee_data.to_excel(
        f"{OUTPUT_DIR}/fees.xlsx",
        sheet_name='пошлины пролонгация',
        header=['N договора', 'код', 'сумма', 'плательщик', 'назначение платежа', 'общая сумма']
    )
    print("Работа закончена!")


if __name__ == '__main__':
    db = DataBaseConnection()
    repo = IntelRepository(db)
    year = input('Последний год действия (текущий по умолчанию - Enter):')
    try:
        year = int(year)
    except ValueError:
        year = datetime.datetime.now().year
    licenses = repo.get_active_licenses_expires_at(year)
    print(f'Всего будет обработано {len(licenses)} договоров')
    process_licenses(licenses)
