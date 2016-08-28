from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.modules import inspector
from kivy.properties import BooleanProperty, ListProperty, NumericProperty

class BusButton(Button):
    is_preview = BooleanProperty(False)
    is_program = BooleanProperty(False)
    fill = ListProperty([0.8, 0.8, 0.8, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_is_preview(self, instance, value):
        self.fill = self.compute_fill()

    def on_is_program(self, instance, value):
        self.fill = self.compute_fill()

    def compute_fill(self):
        if self.is_program:
            return [1, 0, 0, 1]
        elif self.is_preview:
            return [0, 1, 0, 1]
        elif not self.is_preview:
            return [0.8, 0.8, 0.8, 1]

class MainBus(StackLayout):
    preview_feed = NumericProperty()
    program_feed = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feed_buttons = []
        for i in range(10):
            text = str((i + 1) % 10)
            id = "bus_button_{0}".format(text)
            button = BusButton(text=text, id=id)
            self.add_widget(button)
            self.feed_buttons.append(button)

    def on_preview_feed(self, instance, value):
        for feed_button in self.feed_buttons:
            if str(value) == feed_button.text:
                feed_button.is_preview = True
            else:
                feed_button.is_preview = False

    def on_program_feed(self, instance, value):
        for feed_button in self.feed_buttons:
            if str(value) == feed_button.text:
                feed_button.is_program = True
            else:
                feed_button.is_program = False

class SnowmanApp(App):
    preview_feed = NumericProperty(1)
    program_feed = NumericProperty(2)

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.manager.subscribe(self.on_manager_event)

        # todo https://groups.google.com/forum/#!topic/kivy-users/8My4m9PfJo8
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keycode_text = keycode[1]
        if keycode_text in [str(i) for i in range(10)]:
            if keycode_text is '0':
                keycode_text = '10'

            if 'shift' in modifiers:
                self.take(keycode_text)
            else:
                self.preview(keycode_text)
        elif keycode_text is 'enter':
            self.take()
        elif keycode_text is '\\':
            self.manager.transition()

        return True

    def on_manager_event(self, type, value):
        if type == 'set_preview':
            self.preview_feed = value
        elif type == 'set_program':
            self.program_feed = value

    def take(self, feed=None):
        print("take", feed)
        if feed:
            self.manager.set_program(int(feed))
        else:
            self.manager.set_program()

    def preview(self, feed):
        print('preview', feed)
        self.manager.set_preview(int(feed))
