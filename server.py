import game_engine

def receive_player_input(id, input):
    game_engine.GAME.execute_player_command(id, input)


