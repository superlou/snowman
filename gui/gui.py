from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.modules import inspector

class BusButton(Button):
    pass

class MainBus(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(8):
            self.add_widget(BusButton(text=str(i + 1)))

class SnowmanApp(App):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keycode_text = keycode[1]
        if keycode_text in [str(i) for i in range(10)]:
            if 'shift' in modifiers:
                self.take(keycode_text)
            else:
                self.preview(keycode_text)
        elif keycode_text is 'enter':
            self.take()

        return True

    def take(self, feed=None):
        print("take", feed)
        if feed:
            self.manager.set_program(int(feed))
        else:
            self.manager.set_program()

    def preview(self, feed):
        print('preview', feed)
        self.manager.set_preview(int(feed))
