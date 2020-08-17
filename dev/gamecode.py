"""
GameCode:
    enumeration that represents the "mode" of a current game
"""

class GameCode:
    NEW_GAME          = 0 ### Game is set to play a brand new game
    PLAY_LOAD_GAME    = 1 ### Game is set to load and continue and existing game
    CONTINUE_GAME     = 2 ### Game is ongoing
    PLAYBACK_GAME     = 3 ### Game is set to play back a finished game
    NO_PLAY           = 4 ### Game is set not to play or play back any game
