from sqlalchemy.orm import with_polymorphic
from data.model.model import *

menu_items = [{"name": "Группы", "icon": "folder"},
              {"name": "Счета", "icon": "folder"},
              {"name": "МКТУ", "icon": "folder"},
              {"name": "Пошлины", "icon": "folder"},
              {"name": "Категории", "icon": "folder"},
              {"name": "Должности", "icon": "folder"},
              {"name": "Владельцы", "icon": "folder"},
              {"name": "Все объекты", "icon": "folder"},
              {"name": "Лицензии", "icon": "folder"},
              ]


class IntelRepository:
    def __init__(self, database):
        self.source = database.session

    def get_groups(self, filter_query='') -> list[Group]:
        if filter_query:
            return self.source.query(Group).filter(Group.group_name.like(f'%{filter_query}%')).order_by(Group.group_name).all()
        else:
            return self.source.query(Group).order_by(Group.ID).all()

    def get_entities(self) -> list[Entity]:
        all_entities = with_polymorphic(Entity, [Person, Legal])
        return self.source.query(all_entities).order_by(Entity.type).all()

    def get_annual_fees(self) -> list[AnnualFee]:
        return self.source.query(AnnualFee).order_by(AnnualFee.objectType_id, AnnualFee.year).all()
