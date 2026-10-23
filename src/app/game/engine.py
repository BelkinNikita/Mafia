import app.game.lobby as game_lobby
import app.game.ai as ai

import threading
from app.game.manager import Observer
import app.constants as constants


def find_the_most_high_score(given_list):
    the_highest_score = -1
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
    game_lobby.lobby.players[id].is_alive = False
    for bot in ai.ai_brain.bots:
            if bot.lobby_token == id:
                bot.is_alive = False
                bot.target = -1
                break
    team_still_has_alive_players = False
    for player in game_lobby.lobby.players:
        if player.team == game_lobby.lobby.players[id] and player.is_alive:
            team_still_has_alive_players = True
    if not team_still_has_alive_players:
        game_lobby.lobby.is_alive = False
        Observer.notify_team_has_no_members(game_lobby.lobby.players[id].team)
        #game.observer.notify_team_has_no_members(game_lobby.lobby.players[id].team)
    game.list_of_players[id] = -1

    #game.observer.notify_player_death(game_lobby.lobby.players[id])

def show_alive_players():
    for player in game_lobby.lobby.players:
        if player.is_alive:
            print(f"Player {player.lobby_token} ---- {player.team}")


class Time:
    def __init__(self):
        self.period = constants.GameTime.LOBBY_TIME
        self.game = None
        self.observer = None
        print(f"Game time {self.period} is initialized")

    def switch_period(self):
        for player in game_lobby.lobby.players:
            player.used_his_action = False
        if self.period == constants.GameTime.DAY_TIME:

            for action in ALL_ACTIONS:
                if not action.is_instant and not action.is_night:
                    action.next_period()
            self.game.update_list_of_players()
            #ai.ai_brain.find_target_kill_player()
            if game_lobby.lobby.is_playing:
                self.period = constants.GameTime.NIGHT_TIME
                self.set_phase_timer(constants.Duration.MAFIA)
                print("The current time period: Night")
            else:
                print("The game is over!")
        else:
            for action in ALL_ACTIONS:
                if not action.is_instant and action.is_night:
                    action.next_period()
            self.game.update_list_of_players()
            show_alive_players()
            if game_lobby.lobby.is_playing:
                self.period = constants.GameTime.DAY_TIME
                self.set_phase_timer(constants.Duration.VOTING)
                print("The current time period: Day")
            else:
                print("The game is over!")
        Observer.notify_next_period(self.period)
            #ai.ai_brain.find_target_vote_player()
        #ai.ai_brain.make_bot_actions(self.period)


    def set_phase_timer(self, time):
        game_lobby.lobby.current_phase = time
        timer = threading.Timer(time, self.switch_period)
        timer.start()
        print(f"The next phase is started! The current phase lasts in {time} seconds")


class Game:
    def __init__(self):
            self.time = Time()
            self.time.game = self
            self.state = constants.GameState.WAITING
            self.observer = None
            self.list_of_players = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    def update_list_of_players(self):
        for player in range(len(game_lobby.lobby.players)):
            if game_lobby.lobby.players[player].is_alive:
                self.list_of_players[player] = 0
            else:
                self.list_of_players[player] = -1

    def execute_player_command(self, id: int, command: str):
        print(f"player {id} sends: {command}")
        execution = command.split(" ")
        caster_player = int(id)
        action = int(execution[0])
        target_player = int(execution[1])
        ALL_ACTIONS[action].execute(caster_player, target_player)

    def start(self, players: dict, number_of_players: int):
        #game_lobby.lobby.create_player(True)
        game_lobby.lobby.create_team("mafia")
        game_lobby.lobby.create_team("city")
        if number_of_players == 1:
            game_lobby.lobby.teams[0].num_of_players = 1
            game_lobby.lobby.teams[1].num_of_players = 0
            for _ in range(1):
                game_lobby.lobby.create_role("mafia", 0, "mafia", [VOTE], True)
        elif number_of_players <= 5:
            game_lobby.lobby.teams[0].num_of_players = 1
            game_lobby.lobby.teams[1].num_of_players = number_of_players - 1
            for _ in range(1):
                game_lobby.lobby.create_role("mafia", 0, "mafia", [VOTE], True)
            for _ in range(number_of_players - 1):
                game_lobby.lobby.create_role("civilian", 1, "city", [VOTE], False)
        elif number_of_players <= 8:
            game_lobby.lobby.teams[0].num_of_players = 2
            game_lobby.lobby.teams[1].num_of_players = number_of_players - 2
            for _ in range(2):
                game_lobby.lobby.create_role("mafia", 0, "mafia", [VOTE], True)
            for _ in range(number_of_players - 2):
                game_lobby.lobby.create_role("civilian", 1, "city", [VOTE], False)
        else:
            game_lobby.lobby.teams[0].num_of_players = 3
            game_lobby.lobby.teams[1].num_of_players = number_of_players - 3
            for _ in range(3):
                game_lobby.lobby.create_role("mafia", 0, "mafia", [VOTE], True)
            for _ in range(number_of_players - 3):
                game_lobby.lobby.create_role("civilian", 1, "city", [VOTE], False)


        # for i in range(9):
        #     ai_player = ai.AIPlayer()
        #     # ai_player.id = i + 1
        #     ai.ai_brain.bots.append(ai_player)



        print("Number of free players: " + str(game_lobby.lobby.free_players))
        # for name, token in players.items():
        #     game_lobby.lobby.create_player(name, token)
        #     print(name + " " + token)
        print("Number of players: " + str(game_lobby.lobby.free_players))

        game_lobby.lobby.assign_players_to_their_teams()
        show_alive_players()
        for player in game_lobby.lobby.players:
            print("Player name" + player.name)
        # for ai_bot, lobby_bot in zip(ai.ai_brain.bots, game_lobby.lobby.bots):
        #     ai_bot.team = lobby_bot.team
        #     ai_bot.lobby_token = lobby_bot.lobby_token
            # print(f"AI: {ai_bot.team} - LOBBY: {lobby_bot.team}")
            # print(f"AI: {ai_bot.id} - LOBBY: {lobby_bot.id}")


        self.state = constants.GameState.PLAYING
        #self.switch_period()
        print(f"Game starts")
        #self.time.set_phase_timer(3)
        self.time.period = constants.GameTime.DAY_TIME
        self.time.set_phase_timer(constants.Duration.VOTING)
        print("The current time period: Day")
        self.update_list_of_players()

        #ai.ai_brain.find_target_vote_player()
        #ai.ai_brain.make_bot_actions(self.time.period)



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
        if game_lobby.lobby.players[caster].is_alive:
            if game_lobby.lobby.players[target].is_alive:
                if not game_lobby.lobby.players[caster].used_his_action:
                    game_lobby.lobby.players[caster].used_his_action = True
                    return True
                else:
                    print(f"The action by Player {caster} is already used!")
                    return False
            else:
                print(f"Target Player {target} is dead!")
                return False
        else:
            print(f"Caster Player {caster} is dead!")
            return False

    def next_period(self):
        pass


class Vote(Action):
    def __init__(self, name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant):
        super().__init__(name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant)
        self.players_who_received_votes = game.list_of_players.copy()

    def execute(self, caster, target):
        if super().execute(caster, target):
            if game.time.period == constants.GameTime.DAY_TIME:
                self.players_who_received_votes[target] += 1
            else:
                print("Wrong period for the action!")

    def next_period(self):
        kicked_player = find_the_most_high_score(self.players_who_received_votes)
        match kicked_player:
            case -1:
                print("Nobody was kicked by court")
            case _:
                print(f"Player {kicked_player} is kicked by court")
                kill_player(kicked_player)
                self.players_who_received_votes = game.list_of_players.copy()



class MafiaKill(Action):
    def __init__(self, name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant):
        super().__init__(name, is_night, can_be_used_on_allies, can_be_used_on_enemies, can_be_used_on_dead, is_instant)
        self.players_who_under_mafia_attack = game.list_of_players.copy()

    def execute(self, caster, target):
        if super().execute(caster, target):
            if game.time.period == constants.GameTime.NIGHT_TIME:
                self.players_who_under_mafia_attack[target] += 1
            else:
                print("Wrong period for the action!")
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
                self.players_who_under_mafia_attack = game.list_of_players.copy()


game = Game()
VOTE = Vote("vote", False, True, True, False, False)
MAFIA_KILL = MafiaKill("kill", True, True, True, False, False)
ALL_ACTIONS = [VOTE, MAFIA_KILL]
