import locale
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineIconListItem, MDList
from data.model.model import Group
from data.repository.db import *
from data.repository.intel_repo import IntelRepository, menu_items


class GenericListItem(MDCardSwipe, TouchBehavior):
    selected = ObjectProperty()
    main_text = StringProperty()
    second_text = StringProperty()
    edit_callback = ObjectProperty()

    def edit_item(self):
        self.edit_callback(self.selected)

    def on_double_tap(self, *args):
        print(f'двойной клик на {self.selected}')
        self.open_card()


class ContentNavigationDrawer(BoxLayout):
    pass


class MenuItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def on_item_select(self, instance_item, app):
        """Called when tap on a menu item."""
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        app.navigate(instance_item.text)


def on_group_edit(group: Group):
    toast(f'Здесь будет редактирование группы {group.group_name}', 1)


class CommonList(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view = menu_items[0]['name']
        self.db = DataBaseConnection()
        self.screen = Builder.load_file('view/kivy/common_list.kv')

    def build(self):
        return self.screen

    def on_start(self):
        """Bind menu items from dict"""
        for item in menu_items:
            self.root.ids.content_drawer.ids.menu_list.add_widget(
                MenuItemDrawer(icon=item['icon'], text=item['name'])
            )
        self.navigate(self.view)

    def navigate(self, view):
        self.view = view
        self.root.ids.container.clear_widgets()
        repo = IntelRepository(self.db)
        if view == 'Группы':
            self.show_groups(repo)
        elif view == 'Владельцы':
            self.show_entities(repo)
        elif view == 'Пошлины':
            self.show_annual_fees(repo)
        else:
            toast('Пока не реализовано')
        self.root.ids.nav_drawer.set_state('close')

    def show_groups(self, repo):
        groups = repo.get_groups()
        self.root.ids.toolbar.title = self.view
        for group in groups:
            self.root.ids.container.add_widget(
                GenericListItem(selected=group, main_text=f"{group.group_name}", second_text=f"{group.ID}",
                                edit_callback=on_group_edit)
            )

    def show_entities(self, repo):
        entities = repo.get_entities()
        self.root.ids.toolbar.title = self.view
        for entity in entities:
            fullname = entity.get_fullname()
            label = entity.get_simple_line()
            self.root.ids.container.add_widget(
                GenericListItem(selected=entity, main_text=fullname, second_text=label)
            )

    def show_annual_fees(self, repo):
        fees = repo.get_annual_fees()
        self.root.ids.toolbar.title = self.view
        locale.setlocale(locale.LC_ALL, 'ru_RU')
        for fee in fees:
            first_line = f'{fee.code} пошлина за {fee.year} год = {locale.currency(fee.fee)}'
            fee_object = fee.object_type.name
            self.root.ids.container.add_widget(
                GenericListItem(selected=fee, main_text=first_line, second_text=fee_object)
            )
