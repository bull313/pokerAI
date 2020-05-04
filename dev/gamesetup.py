"""
GameSetup:
    Collection of data representing the setup information for a poker game
"""

class GameSetup:
    """
    Constructor:
        This class is a collection of named data values (like a struct)
        No methods are necessary and all properties are public
    """
    def __init__(self):
        self.starting_chip_count        = 0     ### Initial chip count for each player in the game
        self.starting_big_blind         = 0     ### Initial value of the big blind
        self.blind_increase_interval    = 0     ### Rate (in minutes) that the blinds increase
        self.handle_time_expired        = None  ### Callback function called when the blind timer goes off (raising blinds)
        self.init_timestamp             = 0     ### Initial time to set the blind timer to (could be less than blind interval if game is loaded)
        self.round_number               = 0     ### Current round number (relatd to number of times the blinds have increased)
        self.init_player_state          = None  ### Initial data for all players

    """
    Get State Override
    This allows the handle time expired function to be "transient"
    """
    def __getstate__(self):
        """
        Get the object state as a dictionary
        """
        state = dict(self.__dict__)

        """
        Remove Transient Properties
        """
        transient_props = [
            "handle_time_expired"
        ]

        for tprop in transient_props:
            if tprop in state:
                del state["handle_time_expired"]

        """
        Return Result
        """
        return state
