from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class GenericListItem(MDBoxLayout, TouchBehavior):
    selected = ObjectProperty()
    main_text = StringProperty()
    second_text = StringProperty()
    edit_callback = ObjectProperty()
    delete_callback = ObjectProperty()

    def edit_item(self):
        self.edit_callback(self.selected)

    def delete_item(self):
        self.delete_callback(self.selected)

    def on_double_tap(self, touch, *args):
        print(f"Double tapped element {self.selected}")
