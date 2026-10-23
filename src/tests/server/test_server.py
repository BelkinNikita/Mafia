from fastapi.testclient import TestClient
import app.server.server as api
from app.game.lobby import lobby as lobby

client = TestClient(api.app)

def test_create_game():
    #api.create_game()
    api.create_game()
    #print(lobby.id)
    assert lobby.lobby_token is not None
