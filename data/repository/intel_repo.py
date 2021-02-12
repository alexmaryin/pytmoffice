from enum import Enum

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import with_polymorphic
from data.model.model import *
from data.repository.result import Result

menu_items = [{"name": "Группы", "icon": "folder"},
              {"name": "Счета", "icon": "folder"},
              {"name": "МКТУ", "icon": "folder"},
              {"name": "Пошлины", "icon": "folder"},
              {"name": "Категории", "icon": "folder"},
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


class IntelRepository:
    def __init__(self, database):
        self.source = database.session

    def get_groups(self, filter_query='') -> list[Group]:
        if filter_query:
            return self.source.query(Group).filter(Group.group_name.like(f'%{filter_query}%')).order_by(Group.group_name).all()
        else:
            return self.source.query(Group).order_by(Group.ID).all()

    def add_group(self, name) -> (Result, str):
        try:
            new_group = Group(group_name=name)
            self.source.add(new_group)
            self.source.commit()
            return Result.SUCCESS, f'Создана новая группа {name}'
        except DBAPIError:
            self.source.rollback()
            return Result.ERROR, 'Группа с таким наименованием уже есть'

    def edit_group(self, group) -> (Result, str):
        try:
            if group in self.source.dirty:
                self.source.flush()
                return Result.SUCCESS, f'Группа {group.group_name} обновлена'
            else:
                return Result.EMPTY, 'Никаких изменений'
        except DBAPIError:
            self.source.rollback()
            return Result.ERROR, 'Скорее всего группа с таким наименованием уже есть'

    def delete_group(self, group) -> (Result, str):
        try:
            self.source.delete(group)
            self.source.commit()
            return Result.SUCCESS, f'Группа {group.group_name} удалена!'
        except DBAPIError:
            self.source.rollback()
            return Result.ERROR, 'Удаление невозможно из-за нарушения целостности данных.'

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

    def get_annual_fees(self) -> list[AnnualFee]:
        return self.source.query(AnnualFee).order_by(AnnualFee.objectType_id, AnnualFee.year).all()
