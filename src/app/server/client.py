import requests
import time
import threading

import app.client.local_server as local_server
import app.ui.main
from app.server.manager import Observer, Provider
URL = "http://127.0.0.1:8000"


#local_server.local_server.is_playing = True
#local_server.local_server.current_phase = "игра"
#received = requests.get(URL + "/lobby/players/get_role", params={"token": local_server.local_server.local_player.lobby_token}).json()


# ---------------- CREATING ----------------
def create_lobby():
    try:
        received = requests.post(URL + "/game").json()
        local_server.local_server.local_player.host_token = received["host_token"]
        local_server.local_server.lobby_token = received["lobby_id"]
        connect_to_the_game()
    except:
        raise Exception("The creating of lobby is failed!")


# ---------------- CONNECTION ----------------
def connect_to_the_game():
    try:
        received = requests.post(URL + "/lobby/connect").json()
        local_server.local_server.local_player.lobby_token = received["lobby_token"]
        local_server.local_server.local_player.name = received["name"]
        print("is connected!")

        #print(local_server.local_server.local_player.name)
        #time.sleep(5)
        print(local_server.local_server.local_player.lobby_token)
        received = requests.get(URL + "/lobby/players/receive_role", params= {"token": local_server.local_server.local_player.lobby_token}).json()
        print(received)
        threading.Thread(target=update_players_in_lobby, daemon=True).start()
    except:
        raise Exception('The connection was interrupt!')


# ---------------- GAME ENGINE ----------------
def next_phase():
    print("The phase is changed!")


def start_game():
    requests.post(URL + "/game/start", params={"host_token": local_server.local_server.local_player.host_token})
    threading.Thread(target=send_command).start()



def send_command():
    while True:
        requests.get(
            URL + "/game/command", params={
                "token": local_server.local_server.local_player.lobby_token,
                "command": local_server.local_server.local_player.send_command()
            }
        )

# ---------------- UPDATING ----------------
def update_game_state():
    #try:
        while Provider.request_game_state():
            received = requests.get(URL + "/game/state").json()
            print("Current phase: " + str(received["current_phase"]))
            if Observer.notify_update_current_phase(received["current_phase"]):
                Observer.notify_update_alive_players(requests.patch(URL + "/lobby/players/alive").json())
            print("Number of server players: " + str(received["number_of_players"]))
            print("Number of local players: " + str(len(local_server.local_server.players)))
            if received["number_of_players"] != len(local_server.local_server.players):
                print("Number of players is not equal!")
                get_lobby_players()
            time.sleep(3)
        update_players_in_lobby()
    #except:
        print("The loop was interrupted!")


def get_lobby_players():
    received = requests.get(URL + "/lobby/players").json()
    local_server.local_server.players = {local_server.local_server.local_player.name: local_server.local_server.local_player.is_alive}
    for name, is_alive in received.items():
        local_server.local_server.players.setdefault(name, is_alive)
    print(local_server.local_server.players)

def update_players_in_lobby():
    while not Provider.request_game_state():
        Observer.notify_update_players_in_lobby(requests.get(URL + "/lobby/players").json())
        time.sleep(6)
    update_game_state()

def get_alive_players():
    pass




if __name__ == "__main__":
    # create_lobby()
    # connect_to_the_game()
    # update_game_state()
    app.ui.main.start_ui()

