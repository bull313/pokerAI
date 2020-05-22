"""
Hand:
    Represents a set of cards that make up a poker hand
"""

"""
Imports
"""
from collections    import Counter

from card           import Card

class Hand:
    """
    Constants
    """
    TYPE_UNKNOWN = -1
    TYPE_HIGH_CARD = 0
    TYPE_PAIR = 1
    TYPE_TWO_PAIR = 2
    TYPE_THREE_OF_A_KIND = 3
    TYPE_STRAIGHT = 4
    TYPE_FLUSH = 5
    TYPE_FULL_HOUSE = 6
    TYPE_FOUR_OF_A_KIND = 7
    TYPE_STRAIGHT_FLUSH = 8

    HAND_STRINGS = {
        TYPE_HIGH_CARD         : "%s high",
        TYPE_PAIR              : "a pair of %ss, %s high",
        TYPE_TWO_PAIR          : "two pair of %ss and %ss, %s high",
        TYPE_THREE_OF_A_KIND   : "trip %ss, %s high",
        TYPE_STRAIGHT          : "a %s-high straight",
        TYPE_FLUSH             : "a %s-high flush",
        TYPE_FULL_HOUSE        : "a full house, %ss full of %ss",
        TYPE_FOUR_OF_A_KIND    : "quad %ss, %s high",
        TYPE_STRAIGHT_FLUSH    : "a %s-high straight flush"
    }

    HAND_SIZE = 5

    EXCEPTION_UNKNOWN_HAND_TYPE = "Unrecognized hand [%s]"
    EXCEPTION_PROBLEM_DECIPHERING = "Hand cannot be deciphered between two types"

    """
    Constructor
    """
    def __init__(self, cards):
        self._cards = cards

    """
    Operator Overloads
    """
    def __lt__(self, other):
        """
        < if the type is a lower value than the other
            OR the types are the same and the best card is lower
            OR the types are the saem and the best card is the same and the secnod best card is lower...
                and so on
        """
        result = False

        """
        Get the hand rankings of both hands
        """
        self_type, self_values = self.get_hand_ranking()
        other_type, other_values = other.get_hand_ranking()

        """
        Compare by type first
        Compare values if the types are equivalent
        """
        if self_type == other_type:

            """
            Default to false (equivalent is not less than)
            """
            result = False
            
            for i in range( len( self_values ) ):

                if self_values[i] != other_values[i]:
                    result = self_values[i] < other_values[i]
                    break

        else:
            result = self_type < other_type

        """
        Return Result
        """
        return result

    def __eq__(self, other):
        """
        = If one is not less than or greater than the other
        """
        return ( not (self < other) ) and ( not (self > other ) )

    """
    String representation of the hand
    """
    def __str__(self):
        """
        Local Variables
        """
        ret_val = ""
        hand_type, values = self.get_hand_ranking()
        value_strings = [ Card.get_value_str(value) for value in values ]

        if hand_type in Hand.HAND_STRINGS:
            """
            Find the number of card parameters in the hand string
            """
            PARAMETER_TOKEN = "%"
            num_params = Hand.HAND_STRINGS[hand_type].count(PARAMETER_TOKEN)
            ret_val = Hand.HAND_STRINGS[hand_type]

            """
            Populate the parameters with card values if there are any
            """
            if num_params > 0:
                ret_val = Hand.HAND_STRINGS[hand_type] % (tuple(value_strings[:num_params]))

        else:
            """
            Hand is not recongized: this should never happen
            """
            raise Exception(Hand.EXCEPTION_UNKNOWN_HAND_TYPE % values)

        """
        Return Result
        """
        return ret_val

    """
    Private Methods
    """
    def _get_values_and_frequencies(self):
        """
        Get a list of each card value in the hand paired with its number of occurrences
        """
        VALUE = 0
        FREQUENCY = 1

        """
        Get the list of raw values and build the pair list
        """
        raw_values = [ card.get_value() for card in self._cards ]
        most_common = Counter(raw_values).most_common()

        """
        Sort first by most frequent, then by value
        """
        most_common.sort(key=lambda value_freq: (value_freq[FREQUENCY], value_freq[VALUE]), reverse=True)

        """
        Return Result
        """
        return most_common

    def _get_ordered_hand_list(self, most_common):
        """
        Get unique hand values in a list sorted by frequency then by value

        Create a buffer to prevent inserting the same value twice
        """
        seen_values = set()
        seen_add = seen_values.add

        """
        Build hand list
        """
        hand_values = [ value for value, _ in most_common if not (value in seen_values or seen_add(value)) ]

        """
        Return Result
        """
        return hand_values

    def _get_hand_type_by_highest_freq(self, highest_frequency, freq_to_type_table):
        """
        Determine the type of hand by the number of occurrences of the most frequent value
        """
        hand_type = Hand.TYPE_UNKNOWN

        if highest_frequency in freq_to_type_table:
            """
            Use given lookup table to determine type
            """
            hand_type = freq_to_type_table[highest_frequency]
        else:
            """
            Frequency count is not 3 or 2, which should be impossible by the parent if condition
            """
            raise Exception(Hand.EXCEPTION_PROBLEM_DECIPHERING)

        return hand_type

    def _evaluate_between_hands_by_max_freq(self, freq_to_type_table):
        """
        Local Variables
        """
        hand_values = list()
        most_common = self._get_values_and_frequencies()
        hand_type = Hand.TYPE_UNKNOWN
        _, highest_frequency = most_common[0]

        """
        Check the frequency of the most common card to determine the hand type
        """
        hand_type = self._get_hand_type_by_highest_freq(highest_frequency, freq_to_type_table)

        """
        Get the appropriately-ordered list of values
        """
        hand_values = self._get_ordered_hand_list(most_common)

        """
        Store results in return variable
        """
        hand = (hand_type, hand_values)

        """
        Return Result
        """
        return hand

    """
    Public Methods
    """
    def get_hand_ranking(self):
        """
        Evaluate the strength of the hand
        
        Local Variables
        """
        unique_values = set([ card.get_value() for card in self._cards])
        num_unique_values = len(unique_values)
        hand = None

        if num_unique_values == Hand.HAND_SIZE:
            """
            All card values are unique: Hand must be Straight Flush, Straigh, Flush, or High Card

            Test hand for Straight
            """
            straight = True

            """
            Sort values from highest to lowest
            """
            sorted_values = list(unique_values)
            sorted_values.sort(reverse=True)
            
            """
            Check if sorted values are consecutive
            """
            for i in range(1, len(sorted_values)): # Test consecutive
                if sorted_values[i - 1] - sorted_values[i] != 1:
                    straight = False
                    break

            """
            Check for exception: A, 2, 3, 4, 5
            """
            MIN_STRAIGHT = [ Card.ACE_HIGH_VALUE, 5, 4, 3, 2 ]

            if straight == False and sorted_values == MIN_STRAIGHT:
                sorted_values = MIN_STRAIGHT

                """
                In this case, Ace is treated as a low value
                """
                sorted_values.pop(0)
                sorted_values.append(Card.ACE_LOW_VALUE)

                straight = True

            """
            Test hand for Flush
            """
            flush = False

            """
            Hand is a flush if there is only one unique suit
            """
            num_unique_suits = len(set([ card.get_suit() for card in self._cards]))

            if num_unique_suits == 1:
                flush = True

            """
            Hand Evaluation:

            -------------------------------------------
            | Straight  | Flush     | Hand            |  
            ------------------------------------------
            | No        | No        | High Card       |
            | No        | Yes       | Flush           |
            | Yes       | No        | Straight        |
            | Yes       | Yes       | Straight Flush  |
            -------------------------------------------
            """
            if straight and flush:
                hand = (Hand.TYPE_STRAIGHT_FLUSH, sorted_values)
            elif straight:
                hand = (Hand.TYPE_STRAIGHT, sorted_values)
            elif flush:
                hand = (Hand.TYPE_FLUSH, sorted_values)
            else:
                hand = (Hand.TYPE_HIGH_CARD, sorted_values)

        elif num_unique_values == Hand.HAND_SIZE - 1:
            """
            Only 1 nonunique value: hand must be a pair

            Local Variables
            """
            most_common = self._get_values_and_frequencies()
            hand_values = self._get_ordered_hand_list(most_common)
            hand = (Hand.TYPE_PAIR, hand_values)

        elif num_unique_values == Hand.HAND_SIZE - 2:
            """
            Only 2 nonunique values: hand must either be a Two Pair or Three of a Kind
            """
            freq_to_type_table = {
                2: Hand.TYPE_TWO_PAIR,
                3 : Hand.TYPE_THREE_OF_A_KIND
            }

            hand = self._evaluate_between_hands_by_max_freq(freq_to_type_table)

        elif num_unique_values == Hand.HAND_SIZE - 3:
            """
            Only 3 nonunique values: hand must either be a Full House or Four of a Kind
            """
            freq_to_type_table = {
                3: Hand.TYPE_FULL_HOUSE,
                4 : Hand.TYPE_FOUR_OF_A_KIND
            }

            hand = self._evaluate_between_hands_by_max_freq(freq_to_type_table)

        else:
            hand = (Hand.TYPE_UNKNOWN, [ card.get_value() for card in self._cards ])

        return hand
