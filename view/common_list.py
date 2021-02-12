from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from data.repository.db import *
from data.repository.intel_repo import IntelRepository, menu_items, EntityCategory
from view.view_models.categories_view_model import CategoryViewModel
from view.view_models.group_view_model import GroupViewModel


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

    def on_double_tap(self, *args):
        print(f'Состояние - {"выделено" if self.checked else "пропущено"}')


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


def on_edit(obj):
    pass


def on_delete(obj):
    toast(f'Предполагается удаление объекта {obj}', 1)


class RVList(RecycleView):
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
        self.screen_manager = self.screen.ids.screen_manager
        self.active_view_model = GroupViewModel(self.repo, self.navigate)
        # self.groups_view_model = GroupViewModel(self.repo, self.navigate)
        # self.categories_view_model = CategoryViewModel(self.repo, self.navigate)

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

    def navigate(self, view):
        self.view = view
        self.root.ids.toolbar.title = self.view
        self.loading()
        if view == 'Группы':
            self.active_view_model = GroupViewModel(self.repo, self.navigate)
        elif view == 'Типы объектов':
            self.active_view_model = CategoryViewModel(self.repo, self.navigate)
        elif view == 'Физические лица':
            self.show_entities(entity_type=EntityCategory.Persons)
            self.active_view_model = None
        elif view == 'Юридические лица':
            self.show_entities(entity_type=EntityCategory.Legals)
            self.active_view_model = None
        elif view == 'Пошлины':
            self.show_annual_fees()
            self.active_view_model = None
        else:
            self.active_view_model = None
            toast('Пока не реализовано')
        if self.active_view_model:
            self.data = self.active_view_model.show_items()

    def add_item(self):
        if self.active_view_model:
            self.active_view_model.on_add_enter()
        else:
            toast('Пока не реализовано')

    def show_entities(self, entity_type):
        entities = self.repo.get_entities(category=entity_type)
        self.root.ids.toolbar.title = self.view
        for entity in entities:
            fullname = entity.get_fullname()
            label = entity.get_simple_line()
            self.data.append({
                'main_text': fullname,
                'second_text': label,
                'selected': entity,
                'rv_key': entity.id,
                'edit_callback': on_edit,
                'delete_callback': on_delete
            })

    def show_annual_fees(self):
        fees = self.repo.get_annual_fees()
        self.root.ids.toolbar.title = self.view
        for fee in fees:
            first_line = f'{fee.code} пошлина за {fee.year} год = {fee.fee} ₽'
            fee_object = fee.object_type.name
            self.data.append({
                'main_text': first_line,
                'second_text': fee_object,
                'selected': fee,
                'rv_key': fee.id,
                'edit_callback': on_edit,
                'delete_callback': on_delete
            })
