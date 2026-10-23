from kivy.clock import Clock
import app.client.local_server
import app.ui.main

class Observer:
    @staticmethod
    def notify_update_current_phase(updated_phase):
        if app.client.local_server.local_server.current_phase != updated_phase:
            app.client.local_server.local_server.current_phase = updated_phase
            print("Current phase: " + str(updated_phase))
            return True
        else:
            return False

    @staticmethod
    def notify_update_alive_players(alive_players):
        print("alive players: " + str(alive_players))
        # initialize_game()

    @staticmethod
    def notify_update_players_in_lobby(players):
        print("Lobby is refreshed!")
        app.client.local_server.local_server.players = players
        Clock.schedule_once(lambda dt: app.ui.main.screen_manager.current_screen.on_pre_enter(), 0)




class Provider:
    @staticmethod
    def request_game_state():
        return app.client.local_server.local_server.is_playing