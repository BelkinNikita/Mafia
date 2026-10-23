from enum import Enum

# ---------------- Indexes ----------------
class GameTime(Enum):
    LOBBY_TIME = -1
    DAY_TIME = 0
    NIGHT_TIME = 1

class GameState(Enum):
    WAITING = 0
    PLAYING = 1
    VOTING = 2
    ENDED = 3


# ---------------- Game Values ----------------
class Duration(Enum):
    VOTING = 20
    MAFIA = 15


# RED = '\033[31m'
# GREEN = '\033[32m'
# YELLOW = '\033[33m'
# RESET = '\033[0m'
