"""
GameUI:
    Interface for the user to see and interact with the game
"""

"""
Imports
"""
from move import GameMove

"""
Wrapper for the input() function:
    This is done to easily switch between Python 2.7 (raw_input) and 3.x (input) if/when necessary
"""
def get_input(input_msg):
    return input(input_msg)

class GameUI:
    """
    Constants
    """

    """
    Starting Chip Count Strings
    """
    INPUT_STARTING_CHIP_COUNT_STR           = "Enter the starting chip count: "
    INPUT_STARTING_CHIP_COUNT_EVEN_ERROR    = "Starting chip count must be an even number"
    INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR = "Starting chip count must be a valid integer"

    """
    Starting Big Blind Strings
    """
    INPUT_STARTING_BIG_BLIND_STR            = "Enter the starting big blind amount: "
    INPUT_STARTING_BIG_BLIND_EVEN_ERROR     = "Starting big blind must be an even number"
    INPUT_STARTING_BIG_BLIND_INTEGER_ERROR  = "Starting chip count must be a valid integer"
    INPUT_STARTING_BIG_BLIND_SIZE_ERROR     = "Starting big blind must be smaller than the starting chip count"

    """
    Display Player Data Strings
    """
    DISPLAY_PLAYER_DATA_CHIP_COUNT          = "%s has %d chips\n"
    DISPLAY_PLAYER_DATA_IS_DEALER           = "%s is the dealer\n"
    DISPLAY_PLAYER_DATA_CHIPS_IN_ACTION     = "Player has %d chips in action\n"
    DISPLAY_PLAYER_DATA_IS_NOT_DEALER       = "%s is not the dealer\n"
    DISPLAY_PLAYER_DATA_PLAYER_HAND_CARDS   = "%s has %s\n"
    
    """
    Display Pot Strings
    """
    DISPLAY_POT_SIZE = "The pot is currently at %d"
    
    """
    Player Move Strings
    """
    DISPLAY_PLAYER_MOVE_CARDS_AND_STACK_SIZE        = "%s is holding %s and has %d chips remaining"
    DISPLAY_PLAYER_MOVE_REQUIRED_ACTION_RAISE_AMT   = "Required bet/raise is %d to raise the action"
    DISPLAY_PLAYER_MOVE_CURRENT_ACTION              = "%s currently has %d chips in action"
    DISPLAY_PLAYER_MOVE_MAKE_MOVE                   = "Make a move, %s!\n"
    DISPLAY_PLAYER_MOVE_AVAILABLE_MOVES             = "Available Moves:"

    INPUT_PLAYER_MOVE_STR                           = "%s move: "
    INPUT_PLAYER_MOVE_NOT_RECOGNIZED_ERROR          = "Move not recognized. Please enter one of the moves above"
    INPUT_PLAYER_MOVE_UNAVAIL_MOVE_ERROR            = "You cannot make this move at this time. Please make a valid move"
    INPUT_PLAYER_MOVE_INSUFFICIENT_AMT_ERROR        = "The amount you have entered is insufficient. Bet must be at least %d"
    INPUT_PLAYER_MOVE_MOVE_INTEGER_ERROR            = "Please enter an numeric amount to bet"

    """
    Player Made Move Confirmation Strings
    """
    DISPLAY_MOVE_SELECTED = "%s has elected to %s"
    DISPLAY_MOVE_NONE_AVAILABLE = "%s is out of chips and cannot make any moves...."

    """
    All-in Player Strings
    """
    DISPLAY_ALL_IN                  = "A player is all in. No betting round can take place"
    DISPLAY_PRESS_ANY_KEY_PROMPT    = "Press any key to continue..."

    """
    Pot Folded to Winner Strings
    """
    DISPLAY_FOLDED_POT_WINNER = "%s wins the pot with %s as the only player remaining"

    """
    Player Hand Strings
    """
    DISPLAY_HAND_WINNER         = "%s wins with %s!"
    DISPLAY_HAND_SPLIT_WINNER   = "%s has tied and takes a piece of the pot with %s!"
    DISPLAY_HAND_PLAYER_RANK    = "%s had %s"

    """
    Game Winner Strings
    """
    DISPLAY_GAME_WINNER = "%s wins!"
    DISPLAY_GAME_OVER   = "GAME OVER"

    """
    Round Border Constants
    """
    BORDER_LENGTH   = 10
    BORDER_CHAR     = '='

    """
    Game Board Constants
    """
    GAME_BOARD_NAMES = [ "Flop", "Turn", "River" ]

    """
    Private methods
    """
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
        cards_str = " ".join(map(str, hole_cards))

        """
        Return Result
        """
        return cards_str

    """
    Public Methods
    """
    def get_starting_chip_count(self):
        """
        Local Variables
        """
        starting_chip_count = 0
        valid_starting_chip_count = False

        while not valid_starting_chip_count:

            starting_chip_count = get_input(GameUI.INPUT_STARTING_CHIP_COUNT_STR)

            """
            Chip count is valid if it is an even integer
            """
            try:

                starting_chip_count = int(starting_chip_count)

                if starting_chip_count % 2 != 0:
                    print(GameUI.INPUT_STARTING_CHIP_COUNT_EVEN_ERROR)
                else:
                    valid_starting_chip_count = True
                
            except:
                print(GameUI.INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR)

        """
        Return Result
        """
        return starting_chip_count

    def get_starting_big_blind(self, starting_chip_count):
        """
        Local Variables
        """
        starting_big_blind = 0
        valid_starting_big_blind = False

        while not valid_starting_big_blind:

            starting_big_blind = get_input(GameUI.INPUT_STARTING_BIG_BLIND_STR)

            """
            Big blind is valid if it is an even integer that is smaller than the starting chip count
            """
            try:

                starting_big_blind = int(starting_big_blind)

                if starting_big_blind % 2 != 0:
                    print(GameUI.INPUT_STARTING_BIG_BLIND_EVEN_ERROR)
                elif starting_big_blind > starting_chip_count:
                    print(GameUI.INPUT_STARTING_BIG_BLIND_SIZE_ERROR)
                else:
                    valid_starting_big_blind = True

            except:
                print(GameUI.INPUT_STARTING_BIG_BLIND_INTEGER_ERROR)

        """
        Return Result
        """
        return starting_big_blind

    def display_round_border(self):
        """
        Construct the border string
        """
        border_str = ( GameUI.BORDER_CHAR * GameUI.BORDER_LENGTH ) + "\n"

        """
        Print constructed border
        """
        print(border_str)

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

    def display_pot(self, pot):
        print(GameUI.DISPLAY_POT_SIZE % pot)

    def prompt_available_moves(self, player, moves, action_to_play):
        """
        Get the player's hole cards as a string
        """
        cards_str = self._get_hole_cards_as_str(player)

        """
        Display some quick information to the player and prompt for a move
        """
        print(GameUI.DISPLAY_PLAYER_MOVE_CARDS_AND_STACK_SIZE % (player, cards_str, player.get_stack_size()))
        print(GameUI.DISPLAY_PLAYER_MOVE_CURRENT_ACTION % (player, player.get_action()))
        print(GameUI.DISPLAY_PLAYER_MOVE_REQUIRED_ACTION_RAISE_AMT % action_to_play)
        print(GameUI.DISPLAY_PLAYER_MOVE_MAKE_MOVE % player)

        """
        Display each available move
        """
        print(GameUI.DISPLAY_PLAYER_MOVE_AVAILABLE_MOVES)
        for move in moves:
            print("\t%s" % GameMove.get_move_str(move, long_desc=True))
        print("")

        """
        Move selection variables
        """
        chosen_move = None
        chosen_amount = 0
        valid_move_given = False

        while not valid_move_given:
            """
            Get and parse a move from the user
            """
            input_string = get_input( GameUI.INPUT_PLAYER_MOVE_STR % player )
            chosen_move, chosen_amount = GameMove.parse_input_as_move(input_string)

            """
            Move must be recognized and available
            If an amount is required, it must be specified as an integer
            and it must be at least the required action to play
            """
            try:

                if chosen_move is None:
                    print(GameUI.INPUT_PLAYER_MOVE_NOT_RECOGNIZED_ERROR)
                elif chosen_move not in moves:
                    print(GameUI.INPUT_PLAYER_MOVE_NOT_RECOGNIZED_ERROR)
                elif chosen_amount is not None and int(chosen_amount) < action_to_play:
                    print(GameUI.INPUT_PLAYER_MOVE_INSUFFICIENT_AMT_ERROR % action_to_play)
                else:
                    valid_move_given = True

            except:
                print()

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
            display_str += " %d" % chosen_amount
        
        """
        Display constructed string
        """
        print(display_str + "\n")

    def display_no_moves_available(self, player):
        print(GameUI.DISPLAY_MOVE_NONE_AVAILABLE % player)
        get_input(GameUI.DISPLAY_PRESS_ANY_KEY_PROMPT)
        print()

    def display_no_bet_from_all_in(self):
        print(GameUI.DISPLAY_ALL_IN)
        get_input(GameUI.DISPLAY_PRESS_ANY_KEY_PROMPT)
        print()

    def show_folded_round(self, player):
        cards_str = self._get_hole_cards_as_str(player)
        print(GameUI.DISPLAY_FOLDED_POT_WINNER % (player, cards_str))

    def show_board(self, board_idx, board_cards):
        """
        Show the proper board round name
        """
        print("%s:" % GameUI.GAME_BOARD_NAMES[ board_idx ])

        """
        Construct the board cards as a string
        """
        board_str = "\t" + " ".join(map(str, board_cards)) + "\n"

        """
        Display the board cards
        """
        print(board_str)

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

    def display_winner(self, winner):
        print(GameUI.DISPLAY_GAME_WINNER % winner)
        print(GameUI.DISPLAY_GAME_OVER)
