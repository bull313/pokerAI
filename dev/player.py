"""
Player:
    Represents a player in the game and all data pertaining to an individual player
"""

"""
Imports
"""
from copy import deepcopy

class Player:
    """
    Static Variables
    """
    _count = 0

    """
    Constructor
    """
    def __init__(self):
        """
        Increment the number of players created counter
        """
        Player._count += 1

        """
        Public Constant Properties
        """
        self.ID = Player._count     ### Player's unique unchanging identification value

        """
        Private Properties
        """
        self._action = 0            ### Money placed directly in front of the player ("bet" money)
        self._hole_cards = list()   ### Received cards for a hand
        self._stack = 0             ### Current chip count

    """
    String Overrides
    """
    def __str__(self):
        return "Player %d" % self.ID

    """
    Hole Card Setters
    """
    def take_hole_card(self, card):
        self._hole_cards.append(card)

    def pass_hole_cards(self):
        self._hole_cards = list()

    """
    Chip Stack and Action Setter Methods
    """
    def bet(self, num_to_bet):
        """
        Adjust the bet amount to never exceed the player's stack size
        """
        if num_to_bet > self._stack:
            num_to_bet = self._stack

        """
        Move specified number of chips from player's stack to the player's action
        """   
        self._stack -= num_to_bet
        self._action += num_to_bet

        return num_to_bet

    def release_action(self, amount=None):
        """
        Get the number of chips to release from action
        If the amount is specified, cap it at player's total action
        Default to player's total action
        """
        action_released = amount if amount is not None and amount <= self._action else self._action

        """
        Update remaining action
        """    
        self._action -= action_released

        """
        Return Result
        """
        return action_released

    def collect_chips(self, num_received):
        """
        Add the passed value into the stack
        """
        self._stack += num_received

    """
    Getter Methods
    """
    def get_action(self):
        return self._action

    def get_hole_cards(self):
        return deepcopy(self._hole_cards)

    def get_stack_size(self):
        return self._stack
