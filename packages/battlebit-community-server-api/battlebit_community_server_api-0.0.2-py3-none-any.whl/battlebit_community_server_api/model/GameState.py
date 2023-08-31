from enum import IntEnum


class GameState(IntEnum):
    WAITING_FOR_PLAYERS = 0
    COUNTING_DOWN = 1
    PLAYING = 2
    ENDING_GAME = 3
