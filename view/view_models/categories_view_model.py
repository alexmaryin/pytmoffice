from kivymd.toast import toast
from data.model.model import ObjectType
from data.repository.result import Result
from view.common_confirmation import ConfirmDialog
from view.view_models.one_item_view_model import OneItemViewModel


class CategoryViewModel(OneItemViewModel):
    def __init__(self, repository, refresh_view_callback):
        super().__init__(
            repository,
            refresh_view_callback,
            dialog_title='Тип объекта интеллектуальной собственности:',
            view='Типы объектов',
            hint_dialog='название вида объектов интеллектуальной собственности'
        )

    def add(self, instance):
        new = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.add_category(new)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Типы объектов")
        toast(result_text)

    def on_add_enter(self):
        super().add_dialog_enter(self.add)

    def edit(self, instance):
        category = self.editor.item
        category.name = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.edit_category(category)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Типы объектов")
        toast(result_text)

    def on_edit_enter(self, category: ObjectType):
        super().edit_dialog_enter(category, category.name, self.edit)

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
