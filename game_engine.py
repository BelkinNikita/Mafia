import game_lobby
import ai

from enum import Enum
import time #is ised for .sleep()
import threading

LOBBY_TIME = -1
DAY_TIME = 0
NIGHT_TIME = 1

VOTING_TIME = 10
MAFIA_TIME = 8

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'


class GameState(Enum):
    WAITING = 0
    PLAYING = 1
    VOTING = 2
    ENDED = 3


def find_the_most_high_score(given_list):
    the_highest_score = 0
    picked_player = -1
    #print(given_list)
    for player in range(len(given_list) - 1):
        if given_list[player] > the_highest_score:
            the_highest_score = given_list[player]
            picked_player = player
        elif given_list[player] == the_highest_score:
            picked_player = -1
    if picked_player == -1:
        return -1
    else:
        return picked_player

def kill_player(id = int):
    #print("ID: ", id)
    game_lobby.lobby.players[id].is_alive = False
    for bot in ai.ai_brain.bots:
            if bot.id == id:
                bot.is_alive = False
                bot.target = -1
                break
    GAME.list_of_players[id] = -1

def show_alive_players():
    for player in game_lobby.lobby.players:
        if player.is_alive:
            print(f"Player {player.id} ---- {player.team}")


class Time:
    def __init__(self):
        self.period = LOBBY_TIME
        self.game = None
        print(f"Game time {self.period} is initialized")

    def switch_period(self):
        if self.period == DAY_TIME:
            self.period = NIGHT_TIME
            self.set_phase_timer(MAFIA_TIME)
            for action in all_actions:
                if not action.is_instant and not action.is_night:
                    action.next_period()
            self.game.update_list_of_players()
            ai.ai_brain.find_target_kill_player()
            print("The current time period: Night")
        else:
            self.period = DAY_TIME
            self.set_phase_timer(VOTING_TIME)
            for action in all_actions:
                if not action.is_instant and action.is_night:
                    action.next_period()
            self.game.update_list_of_players()
            show_alive_players()
            print("The current time period: Day")
            ai.ai_brain.find_target_vote_player()
        ai.ai_brain.make_bot_actions(self.period)

    def set_phase_timer(self, time):
        timer = threading.Timer(time, self.switch_period)
        timer.start()
        print(f"The next phase is started! The current phase lasts in {time} seconds")


class Game:
    def __init__(self):
            self.time = Time()
            self.time.game = self
            self.state = GameState.WAITING
            self.list_of_players = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    def update_list_of_players(self):
        for player in range(len(game_lobby.lobby.players)):
            if game_lobby.lobby.players[player].is_alive:
                self.list_of_players[player] = 0
            else:
                self.list_of_players[player] = -1

    def execute_player_command(self, id: int, command: str):
        #print(f"player {id} sends: {command}")
        execution = command.split(" ")
        caster_player = int(id)
        action = int(execution[0])
        target_player = int(execution[1])
        all_actions[action].execute(caster_player, target_player)

    def start(self):

        game_lobby.lobby.create_player(False)
        for _ in range(10):
            game_lobby.lobby.create_player(True)

        game_lobby.lobby.create_team("mafia")
        game_lobby.lobby.create_team("city")

        ## TEMPORAL Creating of team settings
        game_lobby.lobby.teams[0].num_of_players = 3
        game_lobby.lobby.teams[1].num_of_players = 7

        for i in range(9):
            ai_player = ai.AIPlayer()
            # ai_player.id = i + 1
            ai.ai_brain.bots.append(ai_player)
        for _ in range(3):
            game_lobby.lobby.create_role("mafia", 0, "mafia", [VOTE], True)
        for _ in range(7):
            game_lobby.lobby.create_role("civilian", 1, "city", [VOTE], False)

        game_lobby.lobby.assign_players_to_their_teams()
        show_alive_players()
        for ai_bot, lobby_bot in zip(ai.ai_brain.bots, game_lobby.lobby.bots):
            ai_bot.team = lobby_bot.team
            ai_bot.id = lobby_bot.id
            # print(f"AI: {ai_bot.team} - LOBBY: {lobby_bot.team}")
            # print(f"AI: {ai_bot.id} - LOBBY: {lobby_bot.id}")


        self.state = GameState.PLAYING
        #self.switch_period()
        print(f"Game starts")
        #self.time.set_phase_timer(3)
        self.time.period = DAY_TIME
        self.time.set_phase_timer(VOTING_TIME)
        print("The current time period: Day")
        self.update_list_of_players()
        ai.ai_brain.find_target_vote_player()
        ai.ai_brain.make_bot_actions(self.time.period)


class Action:
    def __init__(self, name: str, is_night: bool, can_be_used_on_allies: bool, can_be_used_on_enemies: bool, can_be_used_on_dead: bool, is_instant: bool):
        self.is_night = is_night
        self.can_be_used_on_allies = can_be_used_on_allies
        self.can_be_used_on_enemies = can_be_used_on_enemies
        self.can_be_used_on_dead = can_be_used_on_dead
        self.name = name
        self.is_instant = is_instant

    def execute(self, caster, target):
        #print("Target: ", target)
        if game_lobby.lobby.players[target].is_alive:
            return True
        else:
            print(f"Player {target} is dead!")
            return False

    def next_period(self):
        pass


class Vote(Action):
    def __init__(self, name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant):
        super().__init__(name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant)
        self.players_who_received_votes = GAME.list_of_players.copy()

    def execute(self, caster, target):
        if super().execute(caster, target):
            self.players_who_received_votes[target] += 1

    def next_period(self):
        kicked_player = find_the_most_high_score(self.players_who_received_votes)
        match kicked_player:
            case -1:
                print("Nobody was kicked by court")
            case _:
                print(f"Player {kicked_player} is kicked by court")
                kill_player(kicked_player)
                self.players_who_received_votes = GAME.list_of_players.copy()



class MafiaKill(Action):
    def __init__(self, name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant):
        super().__init__(name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant)
        self.players_who_under_mafia_attack = GAME.list_of_players.copy()

    def execute(self, caster, target):
        if super().execute(caster, target):
            self.players_who_under_mafia_attack[target] += 1
            #print("Атака мафии: ", self.players_who_received_votes[target])

    def next_period(self):
        #print(self.players_who_under_mafia_attack)
        killed_player = find_the_most_high_score(self.players_who_under_mafia_attack)
        match killed_player:
            case -1:
                print("Mafia didn't kill anyone")
            case _:
                print(f"Player {killed_player} is killed by Mafia")
                kill_player(killed_player)
                self.players_who_under_mafia_attack = GAME.list_of_players.copy()



GAME = Game()
VOTE = Vote("vote", False, True, True, False, False)
MAFIA_KILL = MafiaKill("kill", True, True, True, False, False)
all_actions = [VOTE, MAFIA_KILL]


GAME.start()