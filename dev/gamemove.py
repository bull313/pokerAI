"""
GameMove:
    Represents a move that can be made in poker
    This class contains:
        * Universal move codes
        * String versions of each move
        * Static methods to convert a string to a move code and vice versa
"""

class GameMove:
    """
    Constants
    """
    CHECK = 0
    BET = 1
    RAISE = 2
    CALL = 3
    FOLD = 4

    MOVE_INPUT_NAMES = {
        "check"          : CHECK,
        "bet #"          : BET,
        "raise #"        : RAISE,
        "call"           : CALL,
        "fold"           : FOLD
    }

    MOVE_DESC_SHORT_STRINGS = {
        CHECK   :   "Check",
        BET     :   "Bet",
        RAISE   :   "Raise to",
        CALL    :   "Call",
        FOLD    :   "Fold"
    }

    MOVE_DESC_LONG_STRINGS = {
        CHECK   :   "Check -> pass your turn",
        BET     :   "Bet -> Add action to the round",
        RAISE   :   "Raise -> Bet more than the current highest bet",
        CALL    :   "Call -> match the current highest bet",
        FOLD    :   "Fold -> Forfeight the round"
    }

    """
    Static methods
    """
    @staticmethod
    def parse_input_as_move(move_str):
        """
        Convert an input string into the appropriate move
        """
        move_amount_split = move_str.split(' ')
        move = move_amount_split[0].lower()
        amount = None
        has_amt = len(move_amount_split) > 1

        """
        Store the amount as a separate variable if there is one
        """
        if has_amt:
            amount = move_amount_split[1]
            move += " #"

        """
        Lookup the move in teh move dictionary
        """
        if move in GameMove.MOVE_INPUT_NAMES:
            move = GameMove.MOVE_INPUT_NAMES[move]
        else:
            move = None
        
        """
        Return Result
        """
        return (move, amount)

    @staticmethod
    def get_move_str(move, long_desc=False):
        """
        Convert a move code to an output string
        """
        move_cmd = ""

        """
        Iteratively search for the matching move name
        """
        for avail_move in GameMove.MOVE_INPUT_NAMES.keys():
            if move == GameMove.MOVE_INPUT_NAMES[avail_move]:
                move_cmd = avail_move
        
        return_str = ""

        """
        Return the move name and description (long/short depending on parameter)
        """
        if long_desc:
            return_str = "%s: %s" % (  move_cmd, GameMove.MOVE_DESC_LONG_STRINGS[move] )
        else:
            return_str = "%s: %s" % (  move_cmd, GameMove.MOVE_DESC_SHORT_STRINGS[move] )

        return return_str
