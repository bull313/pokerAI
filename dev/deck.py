"""
Deck:
    Represents a workable deck of standard playing cards
"""

"""
Imports
"""
from random import shuffle

from card 	import Card

class Deck:
    """
    Constructor
    """
    def __init__(self):
        """
        Properties
        """
        self._cards = list()    ### Collection of card objects

        self.reset()

    """
    Public Methods
    """
    def reset(self):
        """
        Create a card for each suit and each value and add them to the list (deck)
        """
        self._cards.clear()

        for suit in range(len(Card.SUIT_NAMES)):

            for value in Card.VALUES:
                self._cards.append( Card(suit, value) )

    def shuffle(self):
        """
        Randomize the order of the cards
        """
        shuffle(self._cards)

    def draw_card(self):
        """
        Remove a card from the deck and return it
        Return None if there are no available cards
        """
        card = None

        if len(self._cards) > 0:
            card = self._cards.pop(0)

        """
        Return Result
        """
        return card
