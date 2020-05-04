"""
Card:
    Represents a standard playing card
"""

class Card:
    """
    Contants
    """
    SUITS = [ "Clubs", "Diamonds", "Hearts", "Spades" ]
    VALUES = [ value for value in range(2, 15) ]

    FACE_CARD_NAMES = {
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace"
    }

    ACE_HIGH_VALUE = 14
    ACE_LOW_VALUE = 14

    """
    Static method: Get Value String
        Get a card's value as a string
    """
    @staticmethod
    def get_value_str(value):
        if value in Card.FACE_CARD_NAMES:
            return Card.FACE_CARD_NAMES[value][0].upper()
        else:
            return value

    """
    Constructor
    """
    def __init__(self, suit, value):
        self._suit = suit   ### Card's suit
        self._value = value ### Card's numeric value

    """
    < operator overload based off of the value of the card
    """
    def __lt__(self, other):
        return self._value < other._value

    """
    String representation of the card
    """
    def __str__(self):
        ret_val = ""

        """
        Construct the value as a string
        """
        ret_val += str( Card.get_value_str(self._value) )

        """
        Construct the suit as a string
        """
        ret_val += Card.SUITS[ self._suit ][0].upper()

        """
        Return the result
        """
        return ret_val

    """
    Getter Methods
    """
    def get_suit(self):
        return self._suit

    def get_value(self):
        return self._value
