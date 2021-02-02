from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import TwoLineListItem, OneLineIconListItem, MDList
from data.repository.db import *
from data.repository.intel_repo import IntelRepository, menu_items


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def on_item_select(self, instance_item):
        """Called when tap on a menu item."""
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        print(f'selected item {instance_item.text}')


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('kivy/common_list.kv')

    def build(self):
        return self.screen

    def on_start(self):

        """Bind menu items from dict"""
        for item in menu_items:
            self.root.ids.content_drawer.ids.menu_list.add_widget(
                ItemDrawer(icon=item['icon'], text=item['name'])
            )

        db = DataBaseConnection(connection_str)
        repo = IntelRepository(db)
        groups = repo.get_groups()
        self.root.ids.toolbar.title = 'Группы'
        for group in groups:
            self.root.ids.container.add_widget(
                TwoLineListItem(text=f"{group.group_name}", secondary_text=f"{group.ID}")
            )


if __name__ == '__main__':
    Test().run()
