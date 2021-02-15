from kivymd.toast import toast
from data.model.model import Group
from data.repository.result import Result
from view.common_confirmation import ConfirmDialog
from view.view_models.abstract_view_model import AbstractViewModel


class GroupViewModel(AbstractViewModel):
    def __init__(self, repository, refresh_view_callback):
        super().__init__(
            repository,
            refresh_view_callback,
            dialog_title='Группа:',
            view="Группы",
            hint_dialog="Название группы"
        )

    def add(self, instance):
        new = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.add_group(new)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Группы")
        toast(result_text)

    def on_add_enter(self):
        super().add_dialog_enter(self.add)

    def edit(self, instance):
        group = self.editor.item
        group.group_name = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.edit_group(group)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Группы")
        toast(result_text)

    def on_edit_enter(self, group: Group):
        super().edit_dialog_enter(group, group.group_name, self.edit)

    def on_delete_enter(self, group: Group):
        ConfirmDialog(f'Удалить группу {group.group_name}?', self.confirmed_delete, group)

    def confirmed_delete(self, group):
        result, result_text = self.repo.delete_group(group)
        if result == Result.SUCCESS:
            self.refresh_view("Группы")
        toast(result_text)

    def show_items(self) -> list:
        groups = self.repo.get_groups()
        data_dict = []
        for group in groups:
            data_dict.append({
                'main_text': f"{group.group_name}",
                'second_text': f"{group.ID}",
                'selected': group,
                'rv_key': group.ID,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        return data_dict
