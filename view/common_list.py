from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from data.repository.db import *
from data.repository.intel_repo import IntelRepository, menu_items
from view.view_models.categories_view_model import CategoryViewModel
from view.view_models.generic_list_item import GenericListItem
from view.view_models.groups_view_model import GroupViewModel
from view.view_models.legals_view_model import LegalViewModel
from view.view_models.nice_data_view_model import NiceDataViewModel
from view.view_models.persons_view_model import PersonViewModel
from view.view_models.positions_view_model import PositionViewModel

view_models_dict = {
                'Группы': GroupViewModel,
                'Типы объектов': CategoryViewModel,
                'Должности': PositionViewModel,
                'МКТУ': NiceDataViewModel,
                'Физические лица': PersonViewModel,
                'Юридические лица': LegalViewModel,
            }


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


class RVList(RecycleView):
    view_class = ObjectProperty(GenericListItem)

    def __init__(self, **kwargs):
        super(RVList, self).__init__(**kwargs)


class CommonList(MDApp):
    data = ListProperty()
    current_selection = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view = menu_items[0]['name']
        self.db = DataBaseConnection()
        self.repo = IntelRepository(self.db)
        self.screen = Builder.load_file('view/kivy/common_list.kv')
        self.container = self.screen.ids.container
        self.active_view_model = None
        self.dropdown = None

    def build(self):
        return self.screen

    def select_row(self, rv_key, active):
        if active and rv_key not in self.current_selection:
            self.current_selection.append(rv_key)
        elif not active and rv_key in self.current_selection:
            self.current_selection.remove(rv_key)

    def on_start(self):
        """Bind menu items from dict"""
        for item in menu_items:
            self.root.ids.content_drawer.ids.menu_list.add_widget(
                MenuItemDrawer(icon=item['icon'], text=item['name'])
            )
        self.navigate(self.view)

    def loading(self):
        self.data = []
        self.current_selection = []
        self.root.ids.nav_drawer.set_state('close')

    def navigate(self, view, filtered=False):
        self.loading()
        self.root.ids.toolbar.title = view
        if filtered and self.active_view_model:
            self.data = self.active_view_model.show_items()
        else:
            self.view = view
            view_model = view_models_dict.get(view)
            if view_model:
                self.active_view_model = view_model(self.repo, self.navigate)
                self.container.view_class = self.active_view_model.view_class or GenericListItem
                self.data = self.active_view_model.show_items()
                if hasattr(self.active_view_model, 'items_menu'):
                    self.dropdown = MDDropdownMenu(
                        caller=self.root.ids.toolbar,
                        items=self.active_view_model.items_menu,
                        position='auto',
                        width_mult=6,
                        callback=self.click_menu_item
                    )
                else:
                    self.dropdown = None
            else:
                toast('Пока не реализовано')

    def add_item(self):
        if self.active_view_model:
            self.active_view_model.on_add_enter()
        else:
            toast('Пока не реализовано')

    def open_items_menu(self):
        if self.dropdown:
            self.dropdown.open()

    def click_menu_item(self, clicked_item):
        self.active_view_model.on_menu_clicked(clicked_item)
        self.dropdown.dismiss()
