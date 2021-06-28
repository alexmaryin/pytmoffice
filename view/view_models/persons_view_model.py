from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout

from data.model.model import Person
from data.repository.intel_repo import EntityCategory
from view.view_models.entities_view_model import EntitiesViewModel


class PersonEditDialog(MDBoxLayout):
    name_property = ObjectProperty()
    second_name_property = ObjectProperty()
    surname_property = ObjectProperty()
    birthdate_property = ObjectProperty()
    address_property = ObjectProperty()
    accounts_property = ObjectProperty()
    edit_mode = BooleanProperty(False)

    def __init__(self, person: Person, **kwargs):
        super().__init__(**kwargs)
        self.name_property.text = person.name
        self.second_name_property.text = person.second_name
        self.surname_property.text = person.surname
        self.address_property.text = person.address
        self.birthdate_property.text = person.birthdate.strftime('%d.%m.%Y')
        # fill accounts if present


class PersonViewModel(EntitiesViewModel):
    def __init__(self, repository, refresh_view_callback):
        super().__init__(repository, refresh_view_callback, 'Физические лица')
        self.dialog = None
        self.view_class = None
        self.items_menu = [
            {'text': 'Связанные юридические лица', 'call': self.show_managed_legals},
        ]

    def show_items(self) -> list[dict]:
        persons_data = self.repo.get_entities(category=EntityCategory.Persons)
        data_dict = []
        for item in persons_data:
            data_dict.append({
                'main_text': f'{item.get_fullname()}',
                'second_text': f'{item.get_simple_line()}',
                'selected': item,
                'rv_key': item.id,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        return data_dict

    def show_managed_legals(self):
        pass
