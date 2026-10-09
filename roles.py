import random

class Role:
    def __init__(self, name, team, actions, night_role):
        self.name = name
        self.team = team
        self.actions = []
        self.night_role = night_role


class Player:
    def __init__(self, id = int):
        self.id = id
        self.role = None
        self.team = None
        self.is_alive = True
        #print(f"Player {self.id} is created")


class Team:
    def __init__(self, name):
        self.players = []
        self.name = name
        self.num_of_players = 0
        self.free_roles = []
        #print(f"Team {self.name} is created")

    def add_players(self, free_players):
        for _ in range(self.num_of_players):
            added_player = random.randint(0, len(free_players)-1)

            self.players.append(free_players[added_player])
            #print(f"Player {free_players[added_player].id} is in the team {self.name}")
            free_players[added_player].team = self.name
            free_players[added_player].role = self.free_roles[0]

            self.free_roles.remove(self.free_roles[0])
            free_players.remove(free_players[added_player])
        return free_players

    def wake_up(self, role):
        pass