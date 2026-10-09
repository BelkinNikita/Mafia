import server

class GameServer:
    def __init__(self):
        pass

class LocalPlayer:
    def __init__(self):
        self.id = id
        self.role = None
        self.team = None
        self.server = None
        self.can_make_action = False
        self.is_alive = True

    def print_info(self):
        print(f"Your ID: [{self.id}] \n Your team: {self.team} \n Your role: {self.role}")

    def send_action(self):
        try:
            server.receive_player_input(self.id, input("\nGive your action: \n"))
        except:
            "The message was not sent correctly"
        self.send_action()

local_player = LocalPlayer()
#game_server = GameServer()