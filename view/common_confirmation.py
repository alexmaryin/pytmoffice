from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog


class ConfirmDialog(MDDialog):
    def __init__(self, question, confirmed_callback, obj):
        super().__init__(title="Подтверждение действия",
                         text=question,
                         buttons=[
                             MDFlatButton(text="Нет", on_release=self.set_cancel),
                             MDRaisedButton(text="Да", on_release=self.set_confirmation)])
        self.confirmed_action = confirmed_callback
        self.type = "confirmation"
        self.obj = obj
        self.set_normal_height()
        self.open()

    def set_cancel(self, instance):
        self.dismiss()

    def set_confirmation(self, instance):
        self.dismiss()
        self.confirmed_action(self.obj)
