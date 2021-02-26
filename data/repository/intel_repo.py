from enum import Enum
from sqlalchemy.orm import with_polymorphic
from data.model.model import *
from .common_repo import CommonRepository
from .result import Result

menu_items = [{"name": "Группы", "icon": "folder"},
              {"name": "Счета", "icon": "folder"},
              {"name": "МКТУ", "icon": "folder"},
              {"name": "Пошлины", "icon": "folder"},
              {"name": "Типы объектов", "icon": "folder"},
              {"name": "Должности", "icon": "folder"},
              {"name": "Физические лица", "icon": "folder"},
              {"name": "Юридические лица", "icon": "folder"},
              {"name": "Все объекты", "icon": "folder"},
              {"name": "Лицензии", "icon": "folder"},
              ]


class EntityCategory(Enum):
    All = 0
    Persons = 1
    Legals = 2


class IntelRepository(CommonRepository):
    def __init__(self, database):
        super(IntelRepository, self).__init__(database)

        # Groups CRUD methods

    def get_groups(self, filter_query='') -> list[Group]:
        if filter_query:
            return self.source.query(Group).filter(Group.group_name.like(f'%{filter_query}%')).order_by(Group.group_name).all()
        else:
            return self.source.query(Group).order_by(Group.ID).all()

    def add_group(self, name) -> (Result, str):
        new_group = Group(group_name=name)
        return self.common_add_item(
            item=new_group,
            override_success=f'Создана новая группа {name}',
            override_error='Группа с таким наименованием уже есть')

    def edit_group(self, group) -> (Result, str):
        return self.common_edit_item(
            item=group,
            override_success=f'Группа {group.group_name} обновлена',
            override_error='Скорее всего группа с таким наименованием уже есть')

    def delete_group(self, group) -> (Result, str):
        return self.common_delete_item(
            item=group,
            override_success=f'Группа {group.group_name} удалена!')

        # Entities CRUD methods

    def get_entities(self, filter_query='', category=EntityCategory.All) -> list[Entity]:
        entities_for_query = {
            EntityCategory.All: with_polymorphic(Entity, [Person, Legal]),
            EntityCategory.Persons: Person,
            EntityCategory.Legals: Legal
        }[category]
        if filter_query:
            return self.source.query(entities_for_query).filter(Entity.name.like(f'%{filter_query}%')).order_by(Entity.name).all()
        else:
            return self.source.query(entities_for_query).order_by(Entity.type, Entity.name).all()

        # AnnualFees CRUD methods

    def get_annual_fees(self) -> list[AnnualFee]:
        return self.source.query(AnnualFee).order_by(AnnualFee.objectType_id, AnnualFee.year).all()

        # ObjectTypes CRUD methods

    def get_categories(self) -> list[ObjectType]:
        return self.source.query(ObjectType).order_by(ObjectType.id).all()

    def add_category(self, new_type) -> (Result, str):
        new = ObjectType(name=new_type)
        return self.common_add_item(
            item=new,
            override_success=f'Создан новый тип объектов интеллектуальной собственности {new_type}',
            override_error='Тип объектов с таким наименованием уже есть')

    def edit_category(self, category) -> (Result, str):
        return self.common_edit_item(
            item=category,
            override_success=f'Тип объектов {category.name} обновлен',
            override_error='Скорее всего тип объектов с таким наименованием уже есть')

    def delete_category(self, category) -> (Result, str):
        return self.common_delete_item(
            item=category,
            override_success=f'Тип объектов интеллектуальной собственности {category.name} удален!')

        # Positions CRUD methods

    def get_positions(self) -> list[Position]:
        return self.source.query(Position).order_by(Position.position).all()

    def add_position(self, position_name) -> (Result, str):
        new = Position(position=position_name)
        return self.common_add_item(item=new)

    def edit_position(self, position) -> (Result, str):
        return self.common_edit_item(item=position)

    def delete_position(self, position) -> (Result, str):
        return self.common_delete_item(item=position)

        # NICE CRUD methods

    def get_nice_data(self, class_filter=None) -> list[NiceData]:
        if class_filter:
            return self.source.query(NiceData).filter(NiceData.class_number.like(class_filter)).order_by(NiceData.description).all()
        else:
            return self.source.query(NiceData).order_by(NiceData.class_number, NiceData.description).all()

    def add_nice_data(self, class_number, description) -> (Result, str):
        new = NiceData(class_number=class_number, description=description)
        return self.common_add_item(item=new)

    def edit_nice_data(self, nice_data) -> (Result, str):
        return self.common_edit_item(item=nice_data)

    def delete_nice_data(self, nice_data) -> (Result, str):
        return self.common_delete_item(item=nice_data)
