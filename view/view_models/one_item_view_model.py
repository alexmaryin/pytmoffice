from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class OneItemEditor(BoxLayout):
    hint_property = StringProperty()

    def __init__(self, cancel_callback, ok_callback, hint, **kwargs):
        super().__init__(**kwargs)
        self.cancel_callback = cancel_callback
        self.ok_callback = ok_callback
        self.item = None
        self.hint_property = hint


class OneItemViewModel:
    def __init__(self, repository, refresh_view_callback, dialog_title, view, hint_dialog):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.editor = None
        self.editor_dialog = None
        self.dialog_title = dialog_title
        self.view = view
        self.hint_dialog = hint_dialog
        self.view_class = None

    def create_dialog(self):
        if self.editor:
            return MDDialog(
                title=self.dialog_title,
                type='custom',
                content_cls=self.editor,
                buttons=[
                    MDFlatButton(text='Отмена', on_release=self.editor.cancel_callback),
                    MDFlatButton(text='Записать', on_release=self.editor.ok_callback)]
            )

    def close_dialog(self, instance):
        self.editor_dialog.content_cls.name_property = ''
        self.editor_dialog.dismiss()
        self.editor_dialog = None
        self.editor = None

    def add_dialog_enter(self, add_callback):
        self.editor = OneItemEditor(self.close_dialog, add_callback, self.hint_dialog)
        self.editor_dialog = self.create_dialog()
        self.editor_dialog.set_normal_height()
        self.editor_dialog.open()

    def edit_dialog_enter(self, item, item_property, edit_callback):
        self.editor = OneItemEditor(self.close_dialog, edit_callback, self.hint_dialog)
        self.editor.item = item
        self.editor_dialog = self.create_dialog()
        self.editor_dialog.content_cls.name_property = item_property
        self.editor_dialog.set_normal_height()
        self.editor_dialog.open()

    def show_items(self) -> list[dict]:
        return []
