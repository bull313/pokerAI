"""
GameTheater:
    Takes a saved finished game and plays it back to the user
"""

"""
Imports
"""
from gameui import GameUI

class GameTheater:
    """
    Constructor
    """
    def __init__(self, setup, hands):
        self._setup = setup     ### Game setup data
        self._hands = hands     ### List of all played hands in the game
        self._ui    = GameUI()  ### Interface object to display game history

    """
    Private Methods
    """
    def _announce_setup(self):
        """
        Display how the game was set up
        """
        self._ui.display_game_setup(
            self._setup.starting_chip_count, 
            self._setup.starting_big_blind, 
            self._setup.blind_increase_interval
        )

        """
        Pause interface and wait for user acknowledgement
        """
        self._ui.get_user_acknowledgement()

    def _display_hands(self):
        """
        Show the hand history of the game in order
        """
        for hand in self._hands:
            """
            Separate each hand
            """
            self._ui.display_round_border()
            
            """
            Gather all data from the hand and determine the current big blind size
            """
            round_number, init_player_state, timestamp_init, actions, cards, _, _ = hand
            current_big_blind = self._setup.starting_big_blind * round_number

            """
            Display all hand data
            """
            self._ui.display_timer_set(round_number, current_big_blind, timestamp_init)
            self._ui.display_player_data(init_player_state)
            self._ui.show_board(cards)
            self._ui.show_actions(actions)

            """
            Wait for user acknowledgement
            """
            self._ui.display_round_border()
            self._ui.get_user_acknowledgement()

    def _display_winner(self):
        """
        Make the following assumptions:
            * The game has had at least one completed hand
            * There is one and only one player left after the most recent hand
        """
        assert len(self._hands)                 > 0
        last_hand                               = self._hands[-1]
        _, _, _, _, _, player_state_final, _    = last_hand
        assert len(player_state_final)          == 1
        winner                                  = player_state_final[0]

        """
        Display the winner
        """
        self._ui.display_winner(winner)

    """
    Public Methods
    """
    def playback_game(self):
        """
        Game Playback:
            * Display how the game was set up
            * Show the hand history of the game in order
            * Display which player won the game
        """
        self._announce_setup()
        self._display_hands()
        self._display_winner()
