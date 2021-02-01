from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, NumericProperty, DictProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

Window.size = (600, 325)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """

    selected_row = NumericProperty(0)

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:  # nothing selected, select the first
            self.select_node(nodes[0])
            self.selected_row = 0
            return None, None

        if len(nodes) == 1:  # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self):
        """ Select next row """
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.select_node(nodes[0])
            self.selected_row = nodes[0]
        else:
            self.select_node(nodes[last + 1])
            self.selected_row = nodes[last + 1]

    def select_previous(self):
        """ Select previous row """
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.select_node(nodes[-1])
            self.selected_row = nodes[-1]
        else:
            self.select_node(nodes[last - 1])
            self.selected_row = nodes[last - 1]

    def select_current(self):
        """ Select current row """
        last, nodes = self.get_nodes()
        if not nodes:
            return

        self.select_node(nodes[self.selected_row])


class TwoLabelListItem(RecycleDataViewBehavior, BoxLayout):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        self.ids.label1.text = data['text1']
        self.ids.label2.text = data['text2']
        self.data = data

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(TwoLabelListItem, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if self.selected:
            print(self.data)


def display_keystrokes(keycode, text, modifiers):
    print("\nThe key", keycode, "have been pressed")
    print(" - text is %r" % text)
    print(" - modifiers are %r" % modifiers)


class RV(BoxLayout):
    data_items = ListProperty([])
    row_data = DictProperty({})
    data = ListProperty([])
    col_row_controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_states()
        Clock.schedule_once(self.set_default_first_row, .0005)
        self._request_keyboard()

    def _request_keyboard(self):
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'down':  # keycode[274, 'down'] pressed
            # Respond to keyboard down arrow pressed
            display_keystrokes(keycode, text, modifiers)
            self.col_row_controller.select_next()

        elif keycode[1] == 'up':  # keycode[273, 'up] pressed
            # Respond to keyboard up arrow pressed
            display_keystrokes(keycode, text, modifiers)
            self.col_row_controller.select_previous()

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def on_keyboard_select(self):
        """ Respond to keyboard event to call Popup """

        # setup row data for Popup
        self.row_data = self.data[self.col_row_controller.selected_row]

        # call Popup
        self.popup_callback()

    def on_mouse_select(self, instance):
        """ Respond to mouse event to call Popup """

        if self.col_row_controller.selected_row != instance.index:
            # Mouse clicked on row is not equal to current selected row
            self.col_row_controller.selected_row = instance.index

            # Highlight mouse clicked/selected row
            self.col_row_controller.select_current()

        # setup row data for Popup
        self.row_data = self.data[instance.index]

        # call Popup
        self.popup_callback()

    def popup_callback(self):

        # enable keyboard request
        self._request_keyboard()

    def set_default_first_row(self, pd):
        """ Set default first row as selected """
        self.col_row_controller.select_next()

    def update(self):
        self.data = [{'text1': str(x[0]), 'text2': x[1], 'Id': str(x[0]), 'Name': x[1], 'key': 'Id', 'selectable': True}
                     for x in self.data_items]

    def get_states(self):
        rows = [(x, 'abc') for x in range(25)]

        i = 0
        for row in rows:
            self.data_items.append([row[0], row[1], i])
            i += 1
        print(self.data_items)
        self.update()


class MainMenu(BoxLayout):
    states_cities_or_areas = ObjectProperty(None)
    rv = ObjectProperty(None)

    def display_states(self):
        self.remove_widgets()
        self.rv = RV()
        self.states_cities_or_areas.add_widget(self.rv)

    def remove_widgets(self):
        self.states_cities_or_areas.clear_widgets()


class TestApp(App):
    title = "test2"

    def build(self):
        Builder.load_file('kivy/test2.kv')
        return MainMenu()


if __name__ == '__main__':
    TestApp().run()
