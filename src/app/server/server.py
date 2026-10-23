# runs by
# .\.venv\Scripts\python.exe -m uvicorn app.server.server:app --host 0.0.0.0 --port 8000

from secrets import token_urlsafe
from uuid import uuid4
from fastapi import FastAPI
from fastapi.security import HTTPBearer

import app.game.lobby as lobby
import app.game.engine as engine


app = FastAPI(title="Mafia Game API")
bearer = HTTPBearer()


class Observer:
    def notify_player_death(self, player):
        # set_player_dead(player)
        pass

    def notify_team_has_no_members(self, team):
        print(f"Team {team} has no members!")


observer = Observer()
engine.game.server_observer = observer
engine.game.time.server_observer = observer
# ---------------- CREATING ----------------
@app.post("/game")
def create_game():
    lobby.lobby.lobby_token = uuid4().hex[:5].upper()
    host_token = token_urlsafe(10)
    lobby.lobby.host_token = host_token
    return {"lobby_id": lobby.lobby.lobby_token, "host_token": host_token}


# ---------------- CONNECTION ----------------
@app.post("/lobby/connect")
def connect_to_the_lobby():
    lobby_token = token_urlsafe(10)
    new_player = lobby.lobby.create_player(uuid4().hex[:4], lobby_token)
    return {
        "lobby_token": lobby_token,
        "name": new_player.name
    }


# ---------------- GAME ENGINE ----------------
@app.post("/game/start")
def start_game(host_token):
    if lobby.lobby.host_token == host_token:
        print("The game is started!")
        players: dict = {}
        for player in lobby.lobby.players:
            players.setdefault(player.name, player.lobby_token)
            print(player.name)
        engine.game.start(players, len(lobby.lobby.players))
        return {"is_playing": True}
    else:
        print("The host token isn't valid!")


# @app.patch("/lobby/players/")
# def set_player_dead(player):
#     print(f"Player {player.name} is dead!")
#     return {
#         "name": player.name, "is_alive": False
#     }

@app.get("/game/command")
def execute_player_command(token, command: str):
    i = 0
    for player in lobby.lobby.players:
        if player.lobby_token == token:
            engine.game.execute_player_command(i, command)
        i += 1


# ---------------- UPDATING ----------------
@app.get("/game/state")
def update_game_state():
    for player in lobby.lobby.players:
        print(player.name)
    return {
        "current_phase": lobby.lobby.current_phase,
        "number_of_players": len(lobby.lobby.players)
            }


@app.get("/lobby/players")
def get_lobby_players():
    players: dict = {}
    for player in lobby.lobby.players:
        players.setdefault(player.name, player.is_alive)
    return players


@app.get("/lobby/players/receive_role")
def receive_player_role(token):
    for player in lobby.lobby.players:
        print(player.lobby_token)
        if player.lobby_token == token:
            return {
                "team": player.team,
                "role": player.role
            }


@app.get("/lobby/players/number")
def get_number_of_players():
    return {"number_of_players": len(lobby.lobby.players)}


@app.patch("/lobby/players/alive")
def return_alive_players():
    players: dict = {}
    for player in lobby.lobby.players:
        players.setdefault(player.name, player.is_alive)
    print("Player_satus: " + str(players))
    return players