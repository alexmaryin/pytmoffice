from kivymd.uix.behaviors import TouchBehavior
from view.view_models.generic_list_item import GenericListItem


class EntityListItem(GenericListItem, TouchBehavior):
    def on_double_tap(self, touch, *args):
        print(f"Double tapped element {self.selected.get_fullname()}")
