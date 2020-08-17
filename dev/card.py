"""
Card:
    Represents a standard playing card
"""

class Card:
    """
    Contants
    """
    SUIT_NAMES          = [ "Clubs", "Diamonds", "Hearts", "Spades" ]
    VALUES              = [ value for value in range(2, 15) ]

    FACE_CARD_NAMES     = {
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace"
    }

    ACE_HIGH_VALUE      = 14
    ACE_LOW_VALUE       = 14

    """
    Constructor
    """
    def __init__(self, suit, value):
        """
        Properties
        """
        self._suit  = suit  ### Card's suit
        self._value = value ### Card's numeric value

    """
    Static Methods
    """
    @staticmethod
    def get_value_str(value):
        """
        Get a card's value as a string
        """
        value_str = str()

        """
        Lookup non-numeric card name
        Otherwise use the numerical value
        """
        if value in Card.FACE_CARD_NAMES:
            value_str = Card.FACE_CARD_NAMES[value][0].upper()
        else:
            value_str = value

        """
        Return Result
        """
        return value_str

    """
    Override Methods
    """
    def __lt__(self, other):
        """
        < operator overload based off of the value of the card
        """
        return self._value < other._value

    def __str__(self):
        """
        String representation of the card
        """
        ret_val = ""

        """
        Construct the value as a string
        """
        ret_val += str( Card.get_value_str(self._value) )

        """
        Construct the suit as a string
        """
        ret_val += Card.SUIT_NAMES[self._suit][0].upper()

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
