"""
GameUI:
    Interface for the user to see and interact with the game
"""

"""
Imports
"""
from os         import name     as os_name
from os         import system   as os_system

from gameinput  import GameInput
from gamemove   import GameMove
from gamesave   import GameSave
from gametimer  import GameTimer

class GameUI:
    """
    Constants
    """

    """
    Clear Screen Constants
    """
    CLEAR_COMMAND_OTHER         = "clear"
    CLEAR_COMMAND_WINDOWS       = "cls"
    CLEAR_COMMAND_WINDOWS_NAME  = "nt"

    """
    Game Title Strings
    """
    DISPLAY_TITLE = "Welcome to Poker AI!"

    """
    Hot Key Command Strings
    """
    DISPLAY_HOT_KEY_COMMAND                 = "Press %s to %s"
    DISPLAY_HOT_KEY_COMMAND_NOT_RECOGNIZED  = "No hot key registered to callback function when attempted"

    """
    Game Save Strings
    """
    ### Prompt Game Save ###
    INPUT_GAME_SAVE_NAME_STR        = "Enter game save name: "
    INPUT_GAME_SAVE_NAME_NONALNUM   = "Please enter a save name using only numbers and letters"

    ### Display Confirmation ###
    DISPLAY_GAME_SAVE_SUCCESSFUL    = "Game has been successfully saved as %s%s!"
    DISPLAY_GAME_SAVE_FAILURE       = "There was a problem saving the game"

    ### Save Game History Prompt ###
    INPUT_ENDGAME_SAVE_STR              = "Would you like to save the finished game to keep the history (y/n)?"
    INPUT_ENDGAME_SAVE_INVALID_RESPONSE = "Please enter %s for yes or %s for no to respond"
    INPUT_ENDGAME_SAVE_CONFIRM          = "Game history successfully saved to %s%s!"
    INPUT_ENDGAME_SAVE_DENY             = "Game history was not saved"
    INPUT_ENDGAME_SAVE_PROBLEM          = "There was a problem saving the game history"

    """
    Game Loading Strings
    """
    ### Game Load Prompts ###
    INPUT_LOAD_GAME_STR                         = "A game with this name has been found! Would you like to continue playing this game (y/n)?"
    INPUT_LOAD_GAME_INVALID_RESPONSE            = "Please enter %s for yes or %s for no to respond"

    ### Completed Game History Load Prompts ###
    INPUT_LOAD_GAME_HISTORY_STR                 = "A game made with this name has been found! This game is already finished. Would you like to view the game history (y/n)?"
    INPUT_LOAD_GAME_HISTORY_INVALID_RESPONSE    = "Please enter %s for yes or %s for no to respond"

    ### Load Game Confirmation Message ###
    DISPLAY_GAME_SAVE_OVERWRITE_WARNING         = "WARNING: If you continue and save this new game, you will overwrite the existing game in this file.\nIf you would like to keep the save in this file, quit and restart this program with a different save name"
    DISPLAY_GAME_SAVE_HISTORY_CANCELLATION      = "Please restart the software and enter a unique save name to play a new game"

    """
    Set Up New Game Strings
    """
    ### Starting Chip Count ###
    INPUT_STARTING_CHIP_COUNT_STR                   = "Enter the starting chip count: "
    INPUT_STARTING_CHIP_COUNT_NONPOSITIVE_ERROR     = "Starting chip count must be a positive number"
    INPUT_STARTING_CHIP_COUNT_EVEN_ERROR            = "Starting chip count must be an even number"
    INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR         = "Starting chip count must be a valid integer"

    ### Starting Big Blind ###
    INPUT_STARTING_BIG_BLIND_STR                    = "Enter the starting big blind amount: "
    INPUT_STARTING_BIG_BLIND_NONPOSITIVE_ERROR      = "Starting big blind must be a positive number"
    INPUT_STARTING_BIG_BLIND_EVEN_ERROR             = "Starting big blind must be an even number"
    INPUT_STARTING_BIG_BLIND_INTEGER_ERROR          = "Starting big blind must be a valid integer"
    INPUT_STARTING_BIG_BLIND_SIZE_ERROR             = "Starting big blind must be smaller than the starting chip count"

    ### Blind Timer Interval Prompt ###
    INPUT_BIG_BLIND_INTERVAL_STR                    = "Enter the blig blind increase time interval (in minutes): "
    INPUT_BIG_BLIND_INTERVAL_NONPOSITIVE_ERROR      = "Blind increase time interval must be a positive number"
    INPUT_BIG_BLIND_INTERVAL_FLOAT_ERROR            = "Blind increase time interval must be a valid decimal or whole number"

    """
    Blind Timer Progress Strings
    """
    DISPLAY_TIME_EXPIRED                            = "\r\rTime is up! Increasing the blinds next round"
    DISPLAY_TIMER_SET                               = "Round %d! Big blind set to %d and timer has been reset to %s\n"
    DISPLAY_TIMER_CURRENT_VALUE                     = "Time remaning in round %d is %s"
    DISPLAY_TIMER_BLINDS_MAXED_OUT                  = "Big blind is at the maximum of %d and will not be raised any higher\n"

    """
    Player Data Strings
    """
    DISPLAY_PLAYER_DATA_CHIP_COUNT          = "%s has %d chips\n"
    DISPLAY_PLAYER_DATA_IS_DEALER           = "%s is the dealer\n"
    DISPLAY_PLAYER_DATA_CHIPS_IN_ACTION     = "Player has %d chips in action\n"
    DISPLAY_PLAYER_DATA_IS_NOT_DEALER       = "%s is not the dealer\n"
    DISPLAY_PLAYER_DATA_PLAYER_HAND_CARDS   = "%s has %s\n"
    
    """
    Pot Strings
    """
    DISPLAY_POT_SIZE = "The pot is currently at %d"
    
    """
    Player Move Strings
    """
    ### Pre-Move Display Data ###
    DISPLAY_PLAYER_MOVE_CARDS_AND_STACK_SIZE        = "%s is holding %s and has %d chips remaining"
    DISPLAY_PLAYER_MOVE_REQUIRED_ACTION_RAISE_AMT   = "Required bet/raise is %d to raise the action"
    DISPLAY_PLAYER_MOVE_CURRENT_ACTION              = "%s currently has %d chips in action"
    DISPLAY_PLAYER_MOVE_MAKE_MOVE                   = "Make a move, %s!\n"
    DISPLAY_PLAYER_MOVE_AVAILABLE_MOVES             = "Available Moves:"
    DISPLAY_PLAYER_MOVE_AVAILABLE_MOVE              = "\t%s"

    ### Prompt Move ###
    INPUT_PLAYER_MOVE_STR                           = "%s move: "
    INPUT_PLAYER_MOVE_NOT_RECOGNIZED_ERROR          = "Move not recognized. Please enter one of the moves above"
    INPUT_PLAYER_MOVE_UNAVAIL_MOVE_ERROR            = "You cannot make this move at this time. Please make a valid move"
    INPUT_PLAYER_MOVE_INSUFFICIENT_AMT_ERROR        = "The amount you have entered is insufficient. Bet must be at least %d"
    INPUT_PLAYER_MOVE_MOVE_INTEGER_ERROR            = "Please enter an numeric amount to bet"

    ### Move Confirmation ###
    DISPLAY_MOVE_SELECTED                           = "%s has elected to %s"
    DISPLAY_MOVE_AMOUNT                             = " %d"
    DISPLAY_MOVE_NONE_AVAILABLE                     = "%s is out of chips and cannot make any moves...."

    """
    All-in Player Strings
    """
    DISPLAY_ALL_IN                  = "A player is all in. No betting round can take place"

    """
    Post-Hand Strings
    """
    ### Showdown ###
    DISPLAY_HAND_WINNER         = "%s wins with %s!"
    DISPLAY_HAND_SPLIT_WINNER   = "%s has tied and takes a piece of the pot with %s!"
    DISPLAY_HAND_PLAYER_RANK    = "%s had %s"

    ### Pot Folded to Winner ###
    DISPLAY_FOLDED_POT_WINNER   = "%s wins the pot with %s as the only player remaining"

    """
    Game Winner Strings
    """
    DISPLAY_GAME_WINNER = "%s wins the match!"
    DISPLAY_GAME_OVER   = "GAME OVER\n"

    """
    Game History Playback Strings
    """
    ### Playback Game Setup ###
    DISPLAY_STARTING_CHIP_COUNT         = "Each player begins with %d chips"
    DISPLAY_STARTING_BIG_BLIND          = "Starting big blind is %d"
    DISPLAY_BIG_BLIND_INCREASE_INTERVAL = "Blinds increase every %d minutes"
    
    ### Playback Hand ###
    DISPLAY_HAND_ACTIONS_HEADER = "Hand Actions:"
    DISPLAY_HAND_ACTION         = "%s elected to %s"

    """
    User Acknowledgement Strings
    """
    DISPLAY_ACKNOWLEDGEMENT_PROMPT = "Press enter to continue..."

    """
    Round Border Constants
    """
    BORDER_LENGTH   = 10
    BORDER_CHAR     = '='

    """
    Game Board Constants
    """
    GAME_BOARD_NAMES    = [ "Flop", "Turn", "River" ]
    GAME_BOARD_TITLE    = "Board:"
    GAME_BOARD_SUBTITLE = "%s:"

    """
    Character Wrapper Constants
    """
    NEWLINE = '\n'
    SPACE   = ' '
    TAB     = '\t'

    """
    Boolean String Constants
    """
    BOOL_YES    = 'y'
    BOOL_NO     = 'n'

    """
    Constructor
    """
    def __init__(self):
        self._input = GameInput() ### User input manager object

    """
    Private methods
    """
    def _clear_screen(self):
        """
        Clear the command window/terminal using the proper clear command
        """
        if os_name == GameUI.CLEAR_COMMAND_WINDOWS_NAME:
            os_system(GameUI.CLEAR_COMMAND_WINDOWS)
        else:
            os_system(GameUI.CLEAR_COMMAND_OTHER)

    def _is_valid_bool_str(self, val):
        """
        Check if the given string is parseable as a boolean
        """
        return val.lower() in { GameUI.BOOL_YES, GameUI.BOOL_NO }

    def _eval_bool_str(self, val):
        """
        Convert a yes/no string into a boolean

        Ignore casing
        """
        res = None
        val_lower = val.lower()

        """
        Check for valid boolean string values
        """
        if val_lower == GameUI.BOOL_YES:
            res = True
        elif val_lower == GameUI.BOOL_NO:
            res = False
        
        """
        Return Result
        """
        return res

    def _get_hole_cards_as_str(self, player):
        """
        Display the plyer's hole cards
        """
        cards_str = ""

        """
        Get the hole cards and sort them by value
        """
        hole_cards = player.get_hole_cards()
        hole_cards.sort(reverse=True)

        """
        Construct the card string
        """
        cards_str = GameUI.SPACE.join(map(str, hole_cards))

        """
        Return Result
        """
        return cards_str

    def _prompt_value(self, prompt_str, cond_func_str_map, wrapper_function=lambda val: tuple([val]), except_str="", clear_screen=True):
        """
        Local Variables
        """
        current_value = None
        valid_value = False

        while not valid_value:

            current_value = self._input.get_input(prompt_str)
            current_value = wrapper_function(current_value)

            """
            Test every condition and if one fails output its corresponding string
            """
            try:

                valid_value = True

                for cond_func in cond_func_str_map:
                    if not cond_func(*current_value):
                        print( cond_func_str_map[cond_func] )
                        valid_value = False
                        break

            except:
                """
                If an exception occurrs, print the exception string and try again
                """
                print(except_str)
                valid_value = False

        """
        Clear the screen if specified
        """
        if clear_screen:
            self._clear_screen()

        """
        Return Result
        """
        return current_value

    def _setup_command(self, callback, hot_key):
        """
        Create a hot key combo - callback function pair
        """
        if hot_key is not None:
            self._input.pair_hot_key_to_command(hot_key, callback)
        else:
            raise Exception(GameUI.DISPLAY_HOT_KEY_COMMAND_NOT_RECOGNIZED)

    """
    Public Methods
    """
    
    """
    Hot Key Setup Methods
    """
    def setup_save_command(self, callback):
        """
        Hotkey:
            Pair given callback function to the SAVE hot key
        """
        self._setup_command(callback, GameInput.GAME_SAVE)

    def listen_for_hot_keys(self):
        """
        Listen for all installed hotkeys
        """
        self._input.listen_for_hot_keys()

    """
    Game Title Methods
    """
    def display_title(self):
        """
        Show the game title
        """
        print(GameUI.DISPLAY_TITLE)

    """
    Hot Key Display Methods
    """
    def display_hot_key_commands(self):
        """
        Get the name and description of all installed hotkeys and display them
        """
        for hotkey in self._input.get_installed_hotkey_strings():
            hotkey_name, description = hotkey
            print(GameUI.DISPLAY_HOT_KEY_COMMAND % (hotkey_name, description))
        print()

    """
    Game Save Methods
    """
    def get_game_save_name(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: val.isalnum()        :   GameUI.INPUT_GAME_SAVE_NAME_NONALNUM
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_GAME_SAVE_NAME_STR, cond_func_str_map, clear_screen=False)
        return result

    def display_game_save_confirm(self, save_successful, name):
        """
        Display a confirmation message to the user about the status of saving a current game
        """
        if save_successful:
            print(GameUI.DISPLAY_GAME_SAVE_SUCCESSFUL % (name, GameSave.GAME_SAVE_FILE_EXT))
        else:
            print(GameUI.DISPLAY_GAME_SAVE_FAILURE)

    def prompt_save_game_history(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: self._is_valid_bool_str(val)  :   GameUI.INPUT_ENDGAME_SAVE_INVALID_RESPONSE % ( GameUI.BOOL_YES, GameUI.BOOL_NO )
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_ENDGAME_SAVE_STR, cond_func_str_map, clear_screen=False)

        """
        Convert user response to a boolean value
        """
        result = self._eval_bool_str(result)

        return result

    def display_game_history_save_status(self, save_chosen, save_name):
        """
        Confirm the name of the save if the history was saved
        Otherwise display that the game history was not saved
        """
        if save_chosen and save_name:
            print(GameUI.INPUT_ENDGAME_SAVE_CONFIRM % (save_name, GameSave.GAME_SAVE_FILE_EXT))
        elif not save_chosen:
            print(GameUI.INPUT_ENDGAME_SAVE_DENY)
        else:
            print(GameUI.INPUT_ENDGAME_SAVE_PROBLEM)

    """
    Game Load Methods
    """
    def prompt_load_game(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: self._is_valid_bool_str(val)  :   GameUI.INPUT_LOAD_GAME_INVALID_RESPONSE % ( GameUI.BOOL_YES, GameUI.BOOL_NO )
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_LOAD_GAME_STR, cond_func_str_map)

        """
        Convert user response to a boolean value
        """
        result = self._eval_bool_str(result)

        return result

    def display_overwrite_warning(self):
        """
        Warn user of overwriting a saved game with a new game
        """
        print(GameUI.DISPLAY_GAME_SAVE_OVERWRITE_WARNING)

    def prompt_load_game_history(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: self._is_valid_bool_str(val) :   GameUI.INPUT_LOAD_GAME_HISTORY_INVALID_RESPONSE % ( GameUI.BOOL_YES, GameUI.BOOL_NO )
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_LOAD_GAME_HISTORY_STR, cond_func_str_map)

        """
        Convert user response to a boolean value
        """
        result = self._eval_bool_str(result)

        return result

    def display_load_game_history_cancellation(self):
        """
        Show acknoledgement to the user's decision not to save a completed game
        """
        print(GameUI.DISPLAY_GAME_SAVE_HISTORY_CANCELLATION)

    """
    Set Up New Game Methods
    """
    def get_starting_chip_count(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: int(val) > 0        :   GameUI.INPUT_STARTING_CHIP_COUNT_NONPOSITIVE_ERROR,
            lambda val: int(val) % 2 == 0   :   GameUI.INPUT_STARTING_CHIP_COUNT_EVEN_ERROR
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_STARTING_CHIP_COUNT_STR, cond_func_str_map, except_str=GameUI.INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR, clear_screen=False)
        return int( result )

    def get_starting_big_blind(self, starting_chip_count):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: int(val) > 0                    :   GameUI.INPUT_STARTING_BIG_BLIND_NONPOSITIVE_ERROR,
            lambda val: int(val) % 2 == 0               :   GameUI.INPUT_STARTING_BIG_BLIND_EVEN_ERROR,
            lambda val: int(val) <= starting_chip_count :   GameUI.INPUT_STARTING_BIG_BLIND_SIZE_ERROR
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_STARTING_BIG_BLIND_STR, cond_func_str_map, except_str=GameUI.INPUT_STARTING_BIG_BLIND_INTEGER_ERROR, clear_screen=False)
        return int( result )

    def get_blind_increase_interval(self):
        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda val: float(val) > 0    :   GameUI.INPUT_BIG_BLIND_INTERVAL_NONPOSITIVE_ERROR,
        }

        """
        Prompt user for a valid value
        """
        result, = self._prompt_value(GameUI.INPUT_BIG_BLIND_INTERVAL_STR, cond_func_str_map, except_str=GameUI.INPUT_BIG_BLIND_INTERVAL_FLOAT_ERROR, clear_screen=False)
        return float( result )

    """
    Blind Timer Progress Methods
    """
    def display_time_expired(self):
        print(GameUI.DISPLAY_TIME_EXPIRED)

    def display_timer_set(self, round_num, blind_amt, time_amt):
        time_str = GameTimer.minutes_to_str(time_amt)
        print(GameUI.DISPLAY_TIMER_SET % (round_num, blind_amt, time_str))

    def display_current_timer_value(self, round_num, timer_value):
        timer_str = GameTimer.minutes_to_str(timer_value)
        print(GameUI.DISPLAY_TIMER_CURRENT_VALUE % (round_num, timer_str))

    def display_blinds_maxed_out(self, amount):
        print(GameUI.DISPLAY_TIMER_BLINDS_MAXED_OUT % amount)

    """
    Player Data Methods
    """
    def display_player_data(self, players):
        """
        Local Variables
        """
        player_str = ""
        dealer_player = True

        for player in players:
            """
            Display the player's chip count
            """
            player_str += GameUI.DISPLAY_PLAYER_DATA_CHIP_COUNT % (player, player.get_stack_size())

            """
            Display whether or not the player is the current dealer
            """
            if dealer_player:
                player_str += GameUI.DISPLAY_PLAYER_DATA_IS_DEALER % player
                dealer_player = False
            else:
                player_str += GameUI.DISPLAY_PLAYER_DATA_IS_NOT_DEALER % player

            """
            Disaplay the player's chips currently in action
            """
            player_str += GameUI.DISPLAY_PLAYER_DATA_CHIPS_IN_ACTION % player.get_action()
            
            """
            Display the player's hole cards
            """
            cards_str = self._get_hole_cards_as_str(player)
            player_str += GameUI.DISPLAY_PLAYER_DATA_PLAYER_HAND_CARDS % (player, cards_str)

        """
        Print the result
        """
        print(player_str)

    """
    Pot Methods
    """
    def display_pot(self, pot):
        print(GameUI.DISPLAY_POT_SIZE % pot)

    """
    Player Move Methods
    """
    def display_player_move_data(self, player, action_to_play):
        """
        Get the player's hole cards as a string
        """
        cards_str = self._get_hole_cards_as_str(player)

        """
        Display some quick information to the player and prompt for a move
        """
        print(GameUI.DISPLAY_PLAYER_MOVE_CARDS_AND_STACK_SIZE       % ( player, cards_str, player.get_stack_size() )    )
        print(GameUI.DISPLAY_PLAYER_MOVE_CURRENT_ACTION             % ( player, player.get_action() )                   )
        print(GameUI.DISPLAY_PLAYER_MOVE_REQUIRED_ACTION_RAISE_AMT  % action_to_play                                    )
        print(GameUI.DISPLAY_PLAYER_MOVE_MAKE_MOVE                  % player                                            )

    def prompt_available_moves(self, player, moves, action_to_play):
        """
        Display some useful information for the player to see when deciding on a move
        """
        self.display_player_move_data(player, action_to_play)

        """
        Display each available move
        """
        print(GameUI.DISPLAY_PLAYER_MOVE_AVAILABLE_MOVES)
        for move in moves:
            print(GameUI.DISPLAY_PLAYER_MOVE_AVAILABLE_MOVE % GameMove.get_move_str(move, long_desc=True))
        print()

        """
        Create Constraints -> Error Message Map
        """
        cond_func_str_map = {
            lambda move, amt: move  is not None and move in moves               :   GameUI.INPUT_PLAYER_MOVE_NOT_RECOGNIZED_ERROR,
            lambda move, amt: move  in moves                                    :   GameUI.INPUT_PLAYER_MOVE_UNAVAIL_MOVE_ERROR,
            lambda move, amt: amt   is None or int(amt) >= action_to_play       :   GameUI.INPUT_PLAYER_MOVE_INSUFFICIENT_AMT_ERROR % action_to_play
        }

        """
        Prompt user for a valid value
        """
        chosen_move, chosen_amount = self._prompt_value(GameUI.INPUT_PLAYER_MOVE_STR % player, cond_func_str_map, wrapper_function=GameMove.parse_input_as_move, except_str=GameUI.INPUT_PLAYER_MOVE_MOVE_INTEGER_ERROR)

        """
        Get the chosen amount as an integer now that it is confirmed to be one if specified
        """
        if chosen_amount is not None:
            chosen_amount = int(chosen_amount)

        """
        Return result
        """
        return (chosen_move, chosen_amount)

    def display_move_made(self, player, chosen_move, chosen_amount):
        """
        Construct player made move string
        """
        display_str = GameUI.DISPLAY_MOVE_SELECTED % (player, GameMove.get_move_str(chosen_move))
        
        """
        Add an amount if there is one
        """
        if chosen_amount is not None:
            display_str += GameUI.DISPLAY_MOVE_AMOUNT % chosen_amount
        
        """
        Display constructed string
        """
        print(display_str + GameUI.NEWLINE)

    def display_no_moves_available(self, player):
        print(GameUI.DISPLAY_MOVE_NONE_AVAILABLE % player)
        self.get_user_acknowledgement()
        print()

    """
    Player All-In Methods
    """
    def display_no_bet_from_all_in(self):
        print(GameUI.DISPLAY_ALL_IN)
        self.get_user_acknowledgement()
        print()

    """
    Post-Hand Methods
    """
    def show_results(self, player_hand_triples, num_winners):
        """
        Determine singular or split winner message based on the number of hand winners
        """
        winner_message = GameUI.DISPLAY_HAND_WINNER if num_winners == 1 else GameUI.DISPLAY_HAND_SPLIT_WINNER

        for i in range(len(player_hand_triples)):
            """
            Get the player and hand from the hand triple
            """
            _, player, hand = player_hand_triples[i]

            """
            The triples are ordered from best hand to worst, so all players with an index
            smaller than the number of winners have won the hand
            All other players are displayed normally
            """
            if i < num_winners:
                print(winner_message % (player, hand))
            else:
                print(GameUI.DISPLAY_HAND_PLAYER_RANK % (player, hand))

    def show_folded_round(self, player):
        cards_str = self._get_hole_cards_as_str(player)
        print(GameUI.DISPLAY_FOLDED_POT_WINNER % (player, cards_str))

    """
    Game Winner Methods
    """
    def display_winner(self, winner):
        print(GameUI.DISPLAY_GAME_WINNER % winner)
        print(GameUI.DISPLAY_GAME_OVER)

    """
    Game History Playback Methods
    """
    def display_game_setup(self, starting_chip_count, starting_big_blind, big_blind_increase_interval):
        """
        Show the completed game's setup data
        """
        print(GameUI.DISPLAY_STARTING_CHIP_COUNT            % starting_chip_count)
        print(GameUI.DISPLAY_STARTING_BIG_BLIND             % starting_big_blind)
        print(GameUI.DISPLAY_BIG_BLIND_INCREASE_INTERVAL    % big_blind_increase_interval)

    def show_actions(self, actions):
        """
        Display all given hand actions
        """
        print(GameUI.DISPLAY_HAND_ACTIONS_HEADER)

        for action in actions:
            
            """
            Get the selected move, amount tied to it (if there is one), and convert them to a string
            """
            player, chosen_move, adjusted_amount    = action
            chosen_move                             = GameMove.get_move_str(chosen_move)
            action_str                              = GameUI.DISPLAY_HAND_ACTION % (player, chosen_move)

            """
            Add the amount to the action string if there is an amount tied to the move
            """
            if adjusted_amount is not None:
                action_str += GameUI.DISPLAY_MOVE_AMOUNT % adjusted_amount

            """
            Display hand string
            """
            print(GameUI.DISPLAY_PLAYER_MOVE_AVAILABLE_MOVE % action_str)

    """
    User Acknowledgement Methods
    """
    def get_user_acknowledgement(self):
        self._input.get_input(GameUI.DISPLAY_ACKNOWLEDGEMENT_PROMPT)

    """
    Round Border Methods
    """
    def display_round_border(self):
        """
        Construct the border string
        """
        border_str = ( GameUI.BORDER_CHAR * GameUI.BORDER_LENGTH ) + GameUI.NEWLINE

        """
        Print constructed border
        """
        print(border_str)


    """
    Game Board Methods
    """
    def show_board(self, board_cards, board_idx=None):
        """
        Show the proper board round name
        """
        if board_idx is not None:
            print(GameUI.GAME_BOARD_SUBTITLE % GameUI.GAME_BOARD_NAMES[ board_idx ])
        else:
            print(GameUI.GAME_BOARD_TITLE)

        """
        Construct the board cards as a string
        """
        board_str = GameUI.TAB + GameUI.SPACE.join(map(str, board_cards)) + GameUI.NEWLINE

        """
        Display the board cards
        """
        print(board_str)
