from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from data.model.model import Group
from view.common_confirmation import ConfirmDialog
from data.repository.result import Result


class GroupEditor(BoxLayout):
    pass


class GroupViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback

        self.group_dialog = MDDialog(
            title='Группа:',
            type='custom',
            content_cls=GroupEditor(),
            buttons=[
                MDFlatButton(text='Отмена', on_release=self.close_dialog),
                MDFlatButton(text='Записать', on_release=self.add)]
        )
        self.group_dialog.set_normal_height()

    def open_dialog(self):
        self.group_dialog.open()

    def close_dialog(self, instance):
        self.group_dialog.content_cls.name_property = ''
        self.group_dialog.dismiss()

    def add(self, instance):
        new = self.group_dialog.content_cls.name_property
        result, result_text = self.repo.add_group(new)
        if result == Result.SUCCESS:
            self.group_dialog.content_cls.name_property = ''
            self.group_dialog.dismiss()
            self.refresh_view("Группы")
        toast(result_text)

    def on_delete_enter(self, group: Group):
        ConfirmDialog(f'Удалить группу {group.group_name}?', self.confirmed_delete, group)

    def on_edit_enter(self, group: Group):
        toast(f'Здесь будет редактирование группы {group.group_name}', 1)

    def confirmed_delete(self, group: Group):
        result, result_text = self.repo.delete_group(group)
        if result == Result.SUCCESS:
            self.refresh_view("Группы")
        toast(result_text)

    def show_groups(self) -> list:
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
