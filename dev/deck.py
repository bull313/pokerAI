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
        self.reset()

    """
    Create a card for each suit and each value and add them to the list (deck)
    """
    def reset(self):
        self._cards = list()

        for suit in range(len(Card.SUITS)):

            for value in Card.VALUES:
                self._cards.append( Card(suit, value) )

    """
    Randomize the order of the cards
    """
    def shuffle(self):
        shuffle(self._cards)

    """
    Remove a card from the deck and return it
    """
    def draw_card(self):
        if len(self._cards) == 0:
            return None

        card = self._cards.pop(0)
        return card
