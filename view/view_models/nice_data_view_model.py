from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import TouchBehavior, RectangularRippleBehavior, BackgroundColorBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from data.repository.result import Result
from view.common_confirmation import ConfirmDialog
from view.widget_utils import show_widget, hide_widget


class NiceClassViewer(MDBoxLayout):
    description_property = ObjectProperty()
    selected_text = StringProperty()
    class_property = ObjectProperty()
    edit_mode = BooleanProperty(False)

    def __init__(self, _class, _description, **kwargs):
        super().__init__(**kwargs)
        self.class_property.text = _class
        self.description_property.text = _description
        if self.edit_mode:
            show_widget(self.ids.class_layout)
            self.dropdown = MDDropdownMenu(
                caller=self.class_property,
                items=[{'text': f'{x} класс', 'height': '36dp', 'on_release': self.select_class} for x in range(1, 46)],
                width_mult=4,
                position='bottom',
                callback=self.select_class
            )
        else:
            hide_widget(self.ids.class_layout)

    def select_class(self, selected_class):
        self.class_property.text = selected_class.text[:selected_class.text.find(' класс')]
        self.dropdown.dismiss()

    def copy_text(self, copy_all=False):
        if self.selected_text != "" or copy_all:
            Clipboard.copy(self.description_property.text if copy_all else self.selected_text)
            toast("Весь текст скопирован в буфер обмена" if copy_all else "Скопировано в буфер обмена", duration=1)


class NiceDataListItem(MDBoxLayout, TouchBehavior, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    selected = ObjectProperty()
    class_number_text = StringProperty()
    description_text = StringProperty()
    edit_callback = ObjectProperty()
    delete_callback = ObjectProperty()

    def edit_item(self):
        self.edit_callback(self.selected)

    def delete_item(self):
        self.delete_callback(self.selected)

    def on_double_tap(self, touch, *args):
        dialog = MDDialog(
            title=f"{self.class_number_text} класс МКТУ:",
            type="custom",
            size_hint_x=0.8,
            content_cls=NiceClassViewer(self.class_number_text, self.description_text, edit_mode=False),
        )
        dialog.open()


class ClassFilterSnackBar(Snackbar):
    class_filter_text = ObjectProperty()
    filter_callback = ObjectProperty()

    def filter(self):
        self.filter_callback(int(self.class_filter_text.text))


class NiceDataViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.view_class = NiceDataListItem
        self.dialog = None
        self.edited_item = None
        self.items_menu = [
            {'text': 'Фильтр по номеру класса', 'call': self.open_filter},
        ]
        self.filter_class = None

    def close_dialog(self, instance):
        self.dialog.dismiss()

    def on_edit_enter(self, item):
        self.dialog = MDDialog(
            title=f"{item.class_number} класс МКТУ:",
            type="custom",
            size_hint_x=0.8,
            content_cls=NiceClassViewer(str(item.class_number), item.description.decode('utf-8'), edit_mode=True),
            buttons=[
                MDFlatButton(text='Отмена', on_release=self.close_dialog),
                MDRaisedButton(text='Записать', on_release=self.edit_item)]
        )
        self.edited_item = item
        self.dialog.set_normal_height()
        self.dialog.open()

    def edit_item(self, instance):
        self.edited_item.class_number = int(self.dialog.content_cls.class_property.text)
        self.edited_item.description = self.dialog.content_cls.description_property.text.encode('utf-8')
        result, result_text = self.repo.edit_nice_data(self.edited_item)
        if result == Result.SUCCESS:
            self.dialog.dismiss()
            self.refresh_view("МКТУ")
        toast(result_text)

    def on_add_enter(self):
        self.dialog = MDDialog(
            title='Добавление класса МКТУ',
            type="custom",
            size_hint_x=0.8,
            content_cls=NiceClassViewer("1", "", edit_mode=True),
            buttons=[
                MDFlatButton(text='Отмена', on_release=self.close_dialog),
                MDRaisedButton(text='Записать', on_release=self.add_item)]
        )
        self.edited_item = None
        self.dialog.set_normal_height()
        self.dialog.open()

    def add_item(self, instance):
        _class, _description = self.dialog.content_cls.class_property.text, self.dialog.content_cls.description_property.text
        result, result_text = self.repo.add_nice_data(int(_class), _description.encode('utf-8'))
        if result == Result.SUCCESS:
            self.dialog.dismiss()
            self.refresh_view("МКТУ")
        toast(result_text)

    def on_delete_enter(self, item):
        ConfirmDialog(f'Удалить запись о классе {item.class_number}?', self.delete_item, item)

    def delete_item(self, item):
        result, result_text = self.repo.delete_nice_data(item)
        if result == Result.SUCCESS:
            self.refresh_view("МКТУ")
        toast(result_text)

    def show_items(self) -> list[dict]:
        nice_data = self.repo.get_nice_data(class_filter=self.filter_class)
        data_dict = []
        for item in nice_data:
            data_dict.append({
                'class_number_text': f"{item.class_number}",
                'description_text': f"{item.description.decode('utf-8')}",
                'selected': item,
                'rv_key': item.id,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        self.filter_class = None
        return data_dict

    def show_items_filtered(self, filter_class):
        self.filter_class = filter_class
        self.refresh_view('МКТУ')

    def open_filter(self):
        ClassFilterSnackBar(
            filter_callback=self.show_items_filtered,
            text='Фильтр по классу:',
            duration=6
        ).show()

    def on_menu_clicked(self, clicked_item):
        for menu_item in self.items_menu:
            if menu_item['text'] == clicked_item.text:
                menu_item['call']()
