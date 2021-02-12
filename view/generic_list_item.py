from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class GenericListItem(MDBoxLayout, TouchBehavior):
    selected = ObjectProperty()
    main_text = StringProperty()
    second_text = StringProperty()
    edit_callback = ObjectProperty()
    delete_callback = ObjectProperty()
    checked = BooleanProperty(False)

    def edit_item(self):
        self.edit_callback(self.selected)

    def delete_item(self):
        self.delete_callback(self.selected)

    def on_double_tap(self, *args):
        print(f'Состояние - {"выделено" if self.checked else "пропущено"}')
