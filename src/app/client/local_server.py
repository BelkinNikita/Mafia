import app.client.user as user


class LocalServer:
    def __init__(self, local_player):
        self.local_player = local_player
        self._is_playing = False
        self.players: dict = {local_player.name: True}
        self.current_phase = None
        self.id = None

    @property
    def is_playing(self):
        return self._is_playing

    @is_playing.setter
    def is_playing(self, value):
        if value:
            if not self._is_playing:
                self._is_playing = value
                print("the game is started")
            else:
                print("the game is already playing")


local_server = LocalServer(user.local_player)