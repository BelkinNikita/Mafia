from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App

import app.ui.templates as templates
#from app.ui.manager import Observer, Provider
import app.ui.manager as manager


class GameScreen(Screen):
    observer = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.observer = None

        self.phase = "Night"
        self.selected_player = None

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(10),

        )
        layout.add_widget(templates.make_label(
            "MAFIA",
            size=28,
            height=dp(48),
        ))

        self.phase_label = templates.make_label(
            "Phase: Night",
            size=22,
            height=dp(48),
        )
        layout.add_widget(self.phase_label)

        self.role_label = templates.make_label(
            "Your role: Unknown",
            size=18,
            height=dp(42)
        )
        layout.add_widget(self.role_label)

        layout.add_widget(templates.make_label(
            "Select a player",
            size=18,
        ))

        self.players_layout = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
        )
        self.players_layout.bind(
            minimum_height=self.players_layout.setter("height")
        )

        scroll = ScrollView(size_hint_y=0.55)
        scroll.add_widget(self.players_layout)
        layout.add_widget(scroll)

        self.status_label = templates.make_label(
            "Select a player to perform an action",
            size=14,
            height=dp(50),
        )
        layout.add_widget(self.status_label)

        layout.add_widget(templates.make_button(
            "Perform kill action",
            lambda _: self.perform_action(),
        ))

        layout.add_widget(templates.make_button(
            "Next phase (host)",
            lambda _: self.next_phase(),
        ))

        self.add_widget(layout)


    def on_pre_enter(self, *args):
        self.refresh_players()


    def refresh_players(self):
        self.players_layout.clear_widgets()

        for player in manager.Provider.request_players_names():
            button = templates.make_button(
                player,
                lambda instance, name=player: self.select_player(name),
                height=dp(54),
            )
            self.players_layout.add_widget(button)


    def select_player(self, name):
        self.selected_player = name
        self.status_label.text = f"Selected: {name}"


    def perform_action(self):
        manager.Observer.notify_perform_action()
        if not self.selected_player:
            self.status_label.text = "Select a player first."
            return

        self.status_label.text = (
            f"Night action on {self.selected_player}"
            "(not sent to server yet)"
        )


    def vote(self):
        if not self.selected_player:
            self.status_label.text = "Select a player first."
            return

        self.status_label.text = (
            f"Vote for {self.selected_player}"
            "(not sent to server yet)"
        )


    def next_phase(self):
        manager.Observer.notify_next_phase()
        self.phase = "Day" if self.phase == "Night" else "Night"
        self.phase_label.text = f"Phase: {self.phase}"
        self.status_label.text = "Phase changed locally."
        self.selected_player = None


    def back_to_lobby(self):
        manager.Observer.notify_return_to_lobby()
        App.get_running_app().root.current = "lobby"
