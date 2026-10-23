from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from app.ui.screens import menu_screen as menu_screen
from app.ui.screens import lobby_screen as lobby_screen
from app.ui.screens import game_screen as game_screen

screen_manager = ScreenManager()


class MafiaApp(App):
    def build(self):

        screen_manager.add_widget(menu_screen.MainMenuScreen(name="menu"))
        screen_manager.add_widget(lobby_screen.LobbyScreen(name="lobby"))
        screen_manager.add_widget(game_screen.GameScreen(name="game"))

        return screen_manager


def start_ui():
    MafiaApp().run()

if __name__ == "__main__":
    MafiaApp().run()