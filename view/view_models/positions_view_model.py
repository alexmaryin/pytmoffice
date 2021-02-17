from kivymd.toast import toast
from data.model.model import Position
from data.repository.result import Result
from view.common_confirmation import ConfirmDialog
from view.view_models.one_item_view_model import OneItemViewModel


class PositionViewModel(OneItemViewModel):
    def __init__(self, repository, refresh_callback):
        super(PositionViewModel, self).__init__(
            repository,
            refresh_callback,
            dialog_title='Должность:',
            view='Должности',
            hint_dialog='Название должности или статуса'
        )

    def add(self, instance):
        new = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.add_position(new)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Должности")
        toast(result_text)

    def on_add_enter(self):
        super(PositionViewModel, self).add_dialog_enter(self.add)

    def edit(self, instance):
        position = self.editor.item
        position.position = self.editor_dialog.content_cls.name_property
        result, result_text = self.repo.edit_position(position)
        if result == Result.SUCCESS:
            self.editor_dialog.content_cls.name_property = ''
            self.editor_dialog.dismiss()
            self.refresh_view("Должности")
        toast(result_text)

    def on_edit_enter(self, position: Position):
        super(PositionViewModel, self).edit_dialog_enter(position, position.position, self.edit)

    def on_delete_enter(self, position: Position):
        ConfirmDialog(f'Удалить должность {position.position}?', self.confirmed_delete, position)

    def confirmed_delete(self, position):
        result, result_text = self.repo.delete_position(position)
        if result == Result.SUCCESS:
            self.refresh_view("Должности")
        toast(result_text)

    def show_items(self) -> list:
        positions = self.repo.get_positions()
        data_dict = []
        for position in positions:
            data_dict.append({
                'main_text': f"{position.position}",
                'second_text': f"{position.id}",
                'selected': position,
                'rv_key': position.id,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        return data_dict
