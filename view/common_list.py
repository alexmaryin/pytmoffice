from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineIconListItem, MDList
from data.model.model import Group
from data.repository.db import *
from data.repository.intel_repo import IntelRepository, menu_items, EntityCategory
from view.common_confirmation import ConfirmDialog


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


class ContentNavigationDrawer(BoxLayout):
    pass


class GroupEditor(BoxLayout):
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view = menu_items[0]['name']
        self.db = DataBaseConnection()
        self.repo = IntelRepository(self.db)
        self.screen = Builder.load_file('view/kivy/common_list.kv')
        self.screen_manager = self.screen.ids.screen_manager
        self.data_list = self.screen.ids.container

        self.group_dialog = MDDialog(
            title='Группа:',
            type='custom',
            content_cls=GroupEditor(),
            buttons=[
                MDFlatButton(text='Отмена', on_release=self.close_group_dialog),
                MDFlatButton(text='Записать', on_release=self.add_group)]
        )
        self.group_dialog.set_normal_height()

    def close_group_dialog(self, instance):
        self.group_dialog.content_cls.name_property = ''
        self.group_dialog.dismiss()

    def build(self):
        return self.screen

    def on_start(self):
        """Bind menu items from dict"""
        for item in menu_items:
            self.root.ids.content_drawer.ids.menu_list.add_widget(
                MenuItemDrawer(icon=item['icon'], text=item['name'])
            )
        self.navigate(self.view)

    def loading(self):
        self.data_list.data = []
        self.root.ids.nav_drawer.set_state('close')

    def navigate(self, view):
        self.view = view
        self.loading()
        if view == 'Группы':
            self.show_groups()
        elif view == 'Физические лица':
            self.show_entities(entity_type=EntityCategory.Persons)
        elif view == 'Юридические лица':
            self.show_entities(entity_type=EntityCategory.Legals)
        elif view == 'Пошлины':
            self.show_annual_fees()
        else:
            toast('Пока не реализовано')

    def add_item(self):
        if self.view == 'Группы':
            self.group_dialog.open()

    def add_group(self, instance):
        try:
            new = self.group_dialog.content_cls.name_property
            self.repo.add_group(new)
            self.group_dialog.content_cls.name_property = ''
            self.group_dialog.dismiss()
            toast(f'Создана новая группа {new}')
            self.navigate(self.view)
        except DBAPIError:
            toast('Группа с таким наименованием уже есть')

    def on_group_edit(self, group: Group):
        toast(f'Здесь будет редактирование группы {group.group_name}', 1)

    def on_group_delete(self, group: Group):
        ConfirmDialog(f'Удалить группу {group.group_name}?', self.confirmed_delete_group, group)

    def confirmed_delete_group(self, group: Group):
        try:
            name = group.group_name
            self.repo.delete_group(group)
            toast(f'Группа {name} удалена!')
            self.navigate(self.view)
        except DBAPIError:
            toast('Удаление невозможно из-за нарушения целостности данных.')

    def show_groups(self):
        groups = self.repo.get_groups()
        self.root.ids.toolbar.title = self.view
        for group in groups:
            self.data_list.data.append({
                'main_text': f"{group.group_name}",
                'second_text': f"{group.ID}",
                'selected': group,
                'edit_callback': self.on_group_edit,
                'delete_callback': self.on_group_delete
            })

    def show_entities(self, entity_type):
        entities = self.repo.get_entities(category=entity_type)
        self.root.ids.toolbar.title = self.view
        for entity in entities:
            fullname = entity.get_fullname()
            label = entity.get_simple_line()
            self.data_list.data.append({
                'main_text': fullname,
                'second_text': label,
                'selected': entity,
                'edit_callback': on_edit,
                'delete_callback': on_delete
            })

    def show_annual_fees(self):
        fees = self.repo.get_annual_fees()
        self.root.ids.toolbar.title = self.view
        for fee in fees:
            first_line = f'{fee.code} пошлина за {fee.year} год = {fee.fee} ₽'
            fee_object = fee.object_type.name
            self.data_list.data.append({
                'main_text': first_line,
                'second_text': fee_object,
                'selected': fee,
                'edit_callback': on_edit,
                'delete_callback': on_delete
            })
