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
        Player._count += 1
        self.ID = Player._count

        self._action = 0
        self._hole_cards = list()
        self._stack = 0

    """
    String Representation of a Player
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

    def release_action(self):
        action_released = self._action
        self._action = 0
        return action_released

    def collect_chips(self, num_received):
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
