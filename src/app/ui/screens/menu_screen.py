from kivy.metrics import sp
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.app import App

import app.ui.templates as templates
#from app.ui.manager import Observer
import app.ui.manager as manager


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._observer = None

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
        )

        layout.add_widget(Label(
            text="[b]MAFIA[/b]",
            markup=True,
            font_size=sp(38),
            size_hint_y=0.3,
        ))

        layout.add_widget(templates.make_button(
            "Create Lobby",
            lambda _: self.open_lobby(),
        ))

        self.lobby_code = TextInput(
            hint_text="Enter Lobby code",
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            font_size=sp(18)
        )
        layout.add_widget(self.lobby_code)

        layout.add_widget(templates.make_button(
            "Join Lobby",
            lambda _: self.open_lobby(),
        ))

        layout.add_widget(Label(text="", size_hint_y=0.5))

        self.add_widget(layout)


    def open_lobby(self):
        manager.Observer.notify_create_lobby()
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left")
        app.root.current = "lobby"