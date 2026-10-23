import app.client.user as user
import app.game.server as server
import app.game.lobby as game_lobby
import random


NIGHT_TIME = 1


class AIBrain:
    def __init__(self):
        self.target_vote_player = None
        self.target_kill_player = None
        self.bots= []

    def find_target_vote_player(self):
        target_players = []
        no_more_mafia = True
        for player in game_lobby.lobby.players:
            if player.is_alive:
                target_players.append(player)
                if player.team == "mafia":
                    no_more_mafia = False
        if no_more_mafia:
            print("No more mafia players. City has won!")
        if len(target_players) != 0:
            self.target_vote_player = random.choice(target_players).lobby_token - 1
            #print("Voting for: ", self.target_vote_player)
            for bot in ai_brain.bots:
                if bot.is_alive:
                    bot.target = self.target_vote_player
        else:
            print("No more target players. City has won!")
            exit(0)
            for bot in ai_brain.bots:
                if bot.is_alive:
                    bot.target = -1

    def find_target_kill_player(self):
        target_players = []
        for player in game_lobby.lobby.players:
            if player.is_alive and player.team != "mafia":
                target_players.append(player)
        if len(target_players) != 0:
            self.target_kill_player = random.choice(target_players).lobby_token - 1
            #print("Killing for: ", self.target_kill_player)
            for bot in ai_brain.bots:
                if bot.team == "mafia" and bot.is_alive:
                    bot.target = self.target_kill_player
        else:
            print("No more target players")
            exit(0)
            for bot in ai_brain.bots:
                if bot.team == "mafia" and bot.is_alive:
                    bot.target = -1

    def make_bot_actions(self, time):
        for bot in self.bots:
            if time == NIGHT_TIME:
                if bot.team == "mafia":
                    bot.send_action()
            else:
                if bot.team == "city":
                    bot.send_action()



class AIPlayer(user.LocalPlayer):
    def __init__(self):
        super().__init__()
        self.target = None
        self.is_bot = True

    def send_action(self):
        if self.target != -1:
            print(f"Bot {self.id} sends an action from team {self.team} to player {self.target}")
            if self.team == "mafia": #need to learn mafia to kill
                #print(self.id, f"1 {str(self.target)}")
                server.receive_player_input(self.id, f"1 {str(self.target)}")
            elif self.team == "city":
                server.receive_player_input(self.id, f"0 {str(self.target)}")




ai_brain = AIBrain()