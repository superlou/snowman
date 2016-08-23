from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

class MainBus(Widget):
    pass


class SnowmanApp(App):
    def build(self):
        return MainBus()
