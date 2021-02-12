from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from data.model.model import ObjectType
from view.common_confirmation import ConfirmDialog
from data.repository.result import Result


class CategoryEditor(BoxLayout):
    def __init__(self, cancel_callback, ok_callback, **kwargs):
        super().__init__(**kwargs)
        self.cancel_callback = cancel_callback
        self.ok_callback = ok_callback
        self.category = None


class CategoryViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.editor = None
        self.category_dialog = None

    def create_dialog(self):
        return MDDialog(
            title='Тип объекта интеллектуальной собственности:',
            type='custom',
            content_cls=self.editor,
            buttons=[
                MDFlatButton(text='Отмена', on_release=self.editor.cancel_callback),
                MDFlatButton(text='Записать', on_release=self.editor.ok_callback)]
        )

    def close_dialog(self, instance):
        self.category_dialog.content_cls.category_property = ''
        self.category_dialog.dismiss()
        self.category_dialog = None
        self.editor = None

    def add(self, instance):
        new = self.category_dialog.content_cls.category_property
        result, result_text = self.repo.add_category(new)
        if result == Result.SUCCESS:
            self.category_dialog.content_cls.category_property = ''
            self.category_dialog.dismiss()
            self.refresh_view("Типы объектов")
        toast(result_text)

    def on_add_enter(self):
        self.editor = CategoryEditor(self.close_dialog, self.add)
        self.category_dialog = self.create_dialog()
        self.category_dialog.set_normal_height()
        self.category_dialog.open()

    def edit(self, instance):
        self.editor.category.name = self.category_dialog.content_cls.category_property
        result, result_text = self.repo.edit_category(self.editor.category)
        if result == Result.SUCCESS:
            self.category_dialog.content_cls.category_property = ''
            self.category_dialog.dismiss()
            self.refresh_view("Типы объектов")
        toast(result_text)

    def on_edit_enter(self, category: ObjectType):
        self.editor = CategoryEditor(self.close_dialog, self.edit)
        self.editor.category = category
        self.category_dialog = self.create_dialog()
        self.category_dialog.content_cls.category_property = category.name
        self.category_dialog.set_normal_height()
        self.category_dialog.open()

    def on_delete_enter(self, category: ObjectType):
        ConfirmDialog(f'Удалить тип объекта {category.name}?', self.confirmed_delete, category)

    def confirmed_delete(self, category):
        result, result_text = self.repo.delete_category(category)
        if result == Result.SUCCESS:
            self.refresh_view("Типы объектов")
        toast(result_text)

    def show_items(self) -> list:
        categories = self.repo.get_categories()
        data_dict = []
        for category in categories:
            data_dict.append({
                'main_text': f"{category.name}",
                'second_text': '',
                'selected': category,
                'rv_key': category.id,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        return data_dict
