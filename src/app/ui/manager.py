
import app.client.local_server
import app.server.client


class Observer:
    @staticmethod
    def notify_create_lobby():
        print("Lobby is created!")
        app.server.client.create_lobby()

    @staticmethod
    def notify_return_to_lobby():
        print("Lobby is returned!")

    @staticmethod
    def notify_start_game():
        print("Game is started!")
        app.server.client.start_game()

    @staticmethod
    def notify_next_phase():
        print("Next phase is started!")

    @staticmethod
    def notify_go_to_menu():
        print("Menu is returned!")

    @staticmethod
    def notify_perform_action():
        print("Action if performed!")


class Provider:
    @staticmethod
    def request_players_names():
        return app.client.local_server.local_server.players
        #pass




