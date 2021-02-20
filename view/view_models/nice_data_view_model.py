from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import TouchBehavior, RectangularRippleBehavior, BackgroundColorBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel


class ClassListItem(MDLabel):
    pass


class NiceClassViewer(MDBoxLayout):
    label = ObjectProperty()
    class_selector = ObjectProperty()
    description_property = StringProperty()
    selected_text = StringProperty()
    class_property = NumericProperty()
    classes_list = ListProperty([x for x in range(1, 46)])

    def copy_text(self, copy_all=False):
        if self.selected_text != "" or copy_all:
            Clipboard.copy(self.description_property if copy_all else self.selected_text)
            toast("Скопировано в буфер обмена", duration=1)


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
            content_cls=NiceClassViewer(
                class_property=self.class_number_text,
                description_property=self.description_text)
        )
        dialog.open()


class NiceDataViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.view_class = NiceDataListItem

    def on_edit_enter(self, instance):
        pass

    def edit_item(self, instance):
        pass

    def on_delete_enter(self, instance):
        pass

    def delete_item(self, instance):
        pass

    def show_items(self) -> list[dict]:
        nice_data = self.repo.get_nice_data()
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
        return data_dict
