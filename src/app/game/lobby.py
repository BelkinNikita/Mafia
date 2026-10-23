import app.game.roles as roles

class Lobby:
    def __init__(self):
        self.players = []
        self.free_players = []
        self.teams = []
        self.bots = []
        self.roles = ["mafia", "civilian"]
        self.is_playing = False
        self.current_phase = None
        self.id = None
        self.host_token = None

    def create_player(self, name: str, token: str, is_bot: bool=False):
        #player = roles.Player(len(self.players) + 1)
        player = roles.Player(name, token)
        self.players.append(player)
        self.free_players.append(player)
        if is_bot:
            self.bots.append(player)
        return player

    def create_team(self, name):
        self.teams.append(roles.Team(name))

    def create_role(self, name, team_id, team_name, action, wakes_up):
        self.teams[team_id].free_roles.append(roles.Role(name, team_name, action, wakes_up))

    def assign_players_to_their_teams(self):
        print("free players list: " + str(self.free_players))
        for team in self.teams:
            if self.free_players:
                for player in self.players:
                    print("free player: " + str(player.name))
                self.free_players = team.add_players(self.free_players)
        else:
            print("no more players to assign")


lobby = Lobby()