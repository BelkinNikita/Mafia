from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.app import App

import app.ui.templates as templates
#from app.ui.manager import Observer, Provider
import app.ui.manager as manager


class LobbyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
        )

        layout.add_widget(templates.make_label(
            "Lobby code: NOCODE",
            size=16
        ))

        layout.add_widget(templates.make_label(
           "Players",
            size=20,
        ))

        self.players_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(6),
            size_hint_y=None,
        )

        self.players_layout.bind(
            minimum_height=self.players_layout.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.players_layout)
        layout.add_widget(scroll)

        layout.add_widget(templates.make_button(
            "Start game",
            lambda _: self.start_game(),
        ))

        layout.add_widget(templates.make_button(
            "Back to menu",
            lambda _: self.go_to_menu(),
        ))

        self.add_widget(layout)


    def on_pre_enter(self, *args):
        self.players_layout.clear_widgets()

        for index, player in enumerate(manager.Provider.request_players_names(), start=1):
            self.players_layout.add_widget(
                templates.make_label(
                    f"{index}. {player}",
                    size=17,
                    height=dp(42),
                )
            )


    def start_game(self):
        manager.Observer.notify_start_game()
        app = App.get_running_app()
        app.root.transition = SlideTransition(direction="left")
        app.root.current = "game"


    def go_to_menu(self):
        manager.Observer.notify_go_to_menu()
        App.get_running_app().root.current = "menu"
