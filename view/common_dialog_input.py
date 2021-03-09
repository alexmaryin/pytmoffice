from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class Content(BoxLayout):
    input_field = ObjectProperty()

    def __init__(self, text, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        text_widget = MDLabel(text=text)
        input_widget = MDTextField()
        self.input_field = input_widget
        self.add_widget(text_widget)
        self.add_widget(input_widget)


class OneStrInputDialog(MDDialog):
    def __init__(self, title, text, apply_callback):
        super().__init__(title=title,
                         type='custom',
                         content_cls=Content(text),
                         buttons=[
                             MDFlatButton(text="Отмена", on_release=self.set_cancel),
                             MDRaisedButton(text="Ок", on_release=self.set_confirmation)])
        self.action = apply_callback
        self.set_normal_height()

    def set_cancel(self, instance):
        self.dismiss()

    def set_confirmation(self, instance):
        self.dismiss()
        self.action(self.content_cls.input_field.text)
