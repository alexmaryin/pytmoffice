from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from data.repository.intel_repo import EntityCategory


class PersonDialog(MDBoxLayout):
    name_property = ObjectProperty()
    second_name_property = ObjectProperty()
    surname_property = ObjectProperty()
    birthdate_property = ObjectProperty()
    address_property = ObjectProperty()
    accounts_property = ObjectProperty()


class PersonViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.dialog = None
        self.edited_item = None
        self.filter_class = None
        self.filter_text = None
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

    def on_edit_enter(self, instance):
        pass

    def on_delete_enter(self, instance):
        pass

    def show_managed_legals(self):
        pass
