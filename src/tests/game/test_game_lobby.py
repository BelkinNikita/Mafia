import app.game.lobby as game_lobby




class MockAction:
    pass


mock_action = MockAction()

def test_assign_players_to_their_teams():
    for _ in range(10):
        game_lobby.lobby.create_player(True)
    game_lobby.lobby.create_team("mafia")
    game_lobby.lobby.create_team("city")
    game_lobby.lobby.teams[0].num_of_players = 5
    game_lobby.lobby.teams[1].num_of_players = 5
    for _ in range(5):
        game_lobby.lobby.create_role("mafia", 0, "mafia", [mock_action], True)
        game_lobby.lobby.create_role("civilian", 1, "city", [mock_action], False)
    game_lobby.lobby.assign_players_to_their_teams()
    mafia_players = 0
    civilian_players = 0
    for player in game_lobby.lobby.players:
        if player.role.name == "civilian":
            civilian_players += 1
        else:
            mafia_players += 1

    assert mafia_players == 5
    assert civilian_players == 5
