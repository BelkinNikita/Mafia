import roles

class Lobby:
    def __init__(self):
        self.players = []
        self.free_players = []
        self.teams = []
        self.bots = []
        self.roles = ["mafia", "civilian"]
        self.is_playing = True

    def create_player(self, is_bot):
        player = roles.Player(len(self.players) + 1)
        self.players.append(player)
        self.free_players.append(player)
        if is_bot:
            self.bots.append(player)

    def create_team(self, name):
        self.teams.append(roles.Team(name))

    def create_role(self, name, team_id, team_name, action, wakes_up):
        self.teams[team_id].free_roles.append(roles.Role(name, team_name, action, wakes_up))

    def assign_players_to_their_teams(self):
        for team in self.teams:
            self.free_players = team.add_players(self.free_players)

lobby = Lobby()