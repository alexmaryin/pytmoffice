from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog


class NiceClassViewer(MDBoxLayout):
    description_text = StringProperty()

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.description_text = text


class NiceDataListItem(MDBoxLayout, TouchBehavior):
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
        content = NiceClassViewer(self.description_text)
        dialog = MDDialog(
            title=f"{self.class_number_text} класс МКТУ:",
            type="custom",
            content_cls=content
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
