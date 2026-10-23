import app.game.engine as game_engine
import pytest

class MockPlayer:
    def __init__(self, player_id, team, is_alive):
        self.id = player_id
        self.team = team
        self.is_alive = is_alive
        self.is_bot = False
        self.target = None

class MockLobby:
    def __init__(self):
        self.players = []

class MockAIBrain:
    def __init__(self):
        self.target_vote_player = None
        self.target_kill_player = None
        self.bots = []

class MockAction:
    def __init__(self):
        self.caster = None
        self.target = None

    def execute(self, caster, target):
        self.caster = caster
        self.target = target


class MockGame:
    def __init__(self):
        self.list_of_players = None


def test_find_the_most_high_score():
    assert game_engine.find_the_most_high_score([0, -1, -1, -1, -1]) == 0
    assert game_engine.find_the_most_high_score([0, 0, 0, 0, 0]) == -1
    assert game_engine.find_the_most_high_score([0, 0, 0, 0, 0]) == -1
    assert game_engine.find_the_most_high_score([1, 1, -1, -1, -1]) == -1
    assert game_engine.find_the_most_high_score([1, -1, -1, -1, -1]) == 0
    assert game_engine.find_the_most_high_score([1, 3, -1, -1, -1]) == 1
    assert game_engine.find_the_most_high_score([-1, 3, -1, 3, -1]) == -1


def test_kill_player(monkeypatch):
    player_1 = MockPlayer(0, "mafia", True)
    player_2 = MockPlayer(1, "city", False)
    MockAIBrain.bots = [player_1, player_2]
    MockLobby.players = [player_1, player_2]
    MockGame.list_of_players = [0, 0]
    monkeypatch.setattr("app.game.game_engine.game_lobby.lobby", MockLobby)
    monkeypatch.setattr("app.game.game_engine.ai.ai_brain", MockAIBrain)
    assert player_1.is_alive == True
    game_engine.kill_player(0)
    assert player_1.is_alive == False
    assert player_2.is_alive == False


def test_show_alive_players(monkeypatch, capsys):

    player_1 = MockPlayer(0, "mafia", True)
    player_2 = MockPlayer(1, "city", False)
    MockLobby.players = [player_1, player_2]

    monkeypatch.setattr("app.game.game_engine.game_lobby.lobby", MockLobby)

    game_engine.show_alive_players()

    captured = capsys.readouterr()
    assert f"Player {player_1.id} ---- {player_1.team}\n" == captured.out
    assert f"Player {player_2.id} ---- {player_2.team}\n" not in captured.out
    player_1.is_alive = False
    player_2.is_alive = True
    game_engine.show_alive_players()
    captured = capsys.readouterr()
    assert f"Player {player_1.id} ---- {player_1.team}\n" not in captured.out
    assert f"Player {player_2.id} ---- {player_2.team}\n" == captured.out
    player_1.is_alive = False
    player_2.is_alive = False
    game_engine.show_alive_players()
    captured = capsys.readouterr()
    assert f"Player {player_1.id} ---- {player_1.team}\n" not in captured.out
    assert f"Player {player_2.id} ---- {player_2.team}\n" not in captured.out


def test_execute_player_command(monkeypatch):
    action = MockAction()
    all_actions = [action]
    monkeypatch.setattr("app.game.game_engine.ALL_ACTIONS", all_actions)
    game_engine.Game.execute_player_command(game_engine.Game,0,"0 1")
    assert action.caster == 0
    assert action.target == 1
    game_engine.Game.execute_player_command(game_engine.Game, 5, "0 8")
    assert action.caster == 5
    assert action.target == 8
    with pytest.raises(IndexError):
        game_engine.Game.execute_player_command(game_engine.Game, 0, "5 0")
