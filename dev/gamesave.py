"""
GameSave:
    Manages saving a game in its state to a persistent file
"""

"""
Imports
"""
from copy       import deepcopy
from os.path    import exists, join
from pickle     import dumps, loads

from gamedata   import GameData
from gamesetup  import GameSetup

class GameSave:
    """
    Constants
    """
    FILE_WRITE_CODE     = "wb"
    FILE_READ_CODE      = "rb"
    GAME_SAVE_FILE_EXT  = ".pok"

    """
    Constructor
    """
    def __init__(self, save_name):
        """
        Macro game save objects
        """
        self._save_name             = save_name     ### Name of the serialized file
        self._save_setup            = None          ### Object containing game setup data
        self._save_hands            = list()        ### Object containing a list hands played in the game

        """
        Save hand buffer objects
        """
        self._round_number          = None      ### Round number in the game (used to track big blind increase)
        self._player_state_init     = None      ### Buffer variable to hold all player data before a hand
        self._timestamp_init        = None      ### Buffer variable to hold the blind timestamp before a hand
        self._actions               = None      ### Buffer variable to hold all actions made in a hand
        self._cards                 = None      ### Buffer variable to hold all cards dealt in a hand
        self._player_state_final    = None      ### Buffer variable to hold all player data after a hand
        self._timestamp_final       = None      ### Buffer variable to hold the blind timestamp after a hand

    """
    Getter Methods
    """
    def get_game_save_name(self):
        return self._save_name

    def get_game_save(self):
        """
        Return a copy of the saved game's setup and hand history
        """
        return deepcopy( ( self._save_setup, self._save_hands ) )

    """
    Game "Snapshot" Methods
    """
    def snap_game_setup(self, setup):
        """
        Store the game setup data in the setup buffer object
        """
        self._save_setup = setup

    def begin_hand_snapshot(self, round_number, player_state, timestamp):
        """
        Save the round number, initial player state of all players, and blind timer timestamp
        """
        self._round_number      = round_number
        self._player_state_init = player_state
        self._timestamp_init    = timestamp

    def end_hand_snapshot(self, actions, cards, player_state, timestamp):
        """
        Save all actions and cards in the played hand as well as the new states of all players and the new blind timer timestamp
        """
        self._actions               = actions
        self._cards                 = cards
        self._player_state_final    = player_state
        self._timestamp_final       = timestamp

        self._save_hands.append((
            self._round_number,
            self._player_state_init,
            self._timestamp_init,
            self._actions,
            self._cards,
            self._player_state_final,
            self._timestamp_final
        ))

    """
    Public Methods
    """
    def save(self):
        """
        Check if the save happens without errors
        """
        save_clean = True

        try:
            """
            Create a save file object (this will overwrite an existing file of the same name)
            then package and serialize setup and hand history objects to a serialized string
            """
            save_file               = open("%s%s" % (self._save_name, GameSave.GAME_SAVE_FILE_EXT), GameSave.FILE_WRITE_CODE)
            save_obj                = ( self._save_setup, self._save_hands )
            serialized_setup_obj    = dumps( save_obj )

            """
            Write the serialized data string to the file
            """
            save_file.write( serialized_setup_obj )

            """
            Close the file stream
            """
            save_file.close()

        except:
            save_clean = False

        """
        Return Result
        """
        return save_clean

    def load(self):
        """
        Create a save file object (this will overwrite an existing file of the same name)
        then deserialize the file data and unpackage them in the setup and hands buffers
        """
        load_file                           = open("%s%s" % (self._save_name, GameSave.GAME_SAVE_FILE_EXT), GameSave.FILE_READ_CODE)
        file_data                           = load_file.read()
        file_rebuild                        = loads(file_data)
        self._save_setup, self._save_hands  = file_rebuild

        """
        Close the file stream
        """
        load_file.close()

    def save_exists(self):
        """
        Check if a save file of the same name already exists in this directory
        """
        return exists( self._save_name + GameSave.GAME_SAVE_FILE_EXT )

    def is_game_complete(self):
        """
        Check if the current game save is a completed game or an in-progress game
        """
        is_game_complete = False

        """
        Game cannot be complete if there are no saved hands
        """
        if len(self._save_hands) > 0:
            """
            Parse the most recent hand to get the player data
            """
            last_hand = self._save_hands[-1]
            _, _, _, _, _, players, _ = last_hand

            """
            Game is complete if and only if there is only one player remaining in the game
            """
            is_game_complete = len(players) == 1

        return is_game_complete
