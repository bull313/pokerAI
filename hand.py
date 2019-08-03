from collections    import Counter

from card           import Card

class Hand:
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

    HAND_SIZE = 5

    def __init__(self, cards):
        self._cards = []

        for i in range(Hand.HAND_SIZE):
            self._cards.append(cards[i])

    def __lt__(self, other):
        self_hand = self.get_hand_ranking()
        other_hand = other.get_hand_ranking()

        HAND_TYPE = 0
        HAND_VALUES = 1
        if self_hand[HAND_TYPE] == other_hand[HAND_TYPE]:
            for i in range( len( self_hand[HAND_VALUES] ) ):                
                if self_hand[HAND_VALUES][i] != other_hand[HAND_VALUES][i]:
                    return self_hand[HAND_VALUES][i] < other_hand[HAND_VALUES][i]
            return False # False due to equivalence

        return self_hand[HAND_TYPE] < other_hand[HAND_TYPE]

    def __str__(self):
        type, values = self.get_hand_ranking()

        if type == Hand.TYPE_HIGH_CARD:
            return "%s high" % tuple([ Card.get_value_str(values[i]) for i in range(1) ])
        elif type == Hand.TYPE_PAIR:
            return "pair of %ss, %s high" % tuple([ Card.get_value_str(values[i]) for i in range(2) ])
        elif type == Hand.TYPE_TWO_PAIR:
            return "pair of %ss and %ss, %s high" % tuple([ Card.get_value_str(values[i]) for i in range(3) ])
        elif type == Hand.TYPE_THREE_OF_A_KIND:
            return "set of %ss, %s high" % tuple([ Card.get_value_str(values[i]) for i in range(2) ])
        elif type == Hand.TYPE_STRAIGHT:
            return "%s-high straight" % tuple([ Card.get_value_str(values[i]) for i in range(1) ])
        elif type == Hand.TYPE_FLUSH:
            return "%s-high flush" % tuple([ Card.get_value_str(values[i]) for i in range(1) ])
        elif type == Hand.TYPE_FULL_HOUSE:
            return "full house, %ss full of %ss" % tuple([ Card.get_value_str(values[i]) for i in range(2) ])
        elif type == Hand.TYPE_FOUR_OF_A_KIND:
            return "quad %ss, %s high" % tuple([ Card.get_value_str(values[i]) for i in range(2) ])
        elif type == Hand.TYPE_STRAIGHT_FLUSH:
            if values[0] == 14:
                return "royal flush"
            return "%s-high straight flush" % tuple([ Card.get_value_str(values[i]) for i in range(1) ])

        else:
            return "unknown hand"

    def get_hand_ranking(self):
        VALUE = 0
        FREQUENCY = 1

        unique_values = set([ card.get_value() for card in self._cards])
        num_unique_values = len(unique_values)

        if num_unique_values == Hand.HAND_SIZE:
            # Straight
            straight = True
            sorted_values = list(unique_values)
            sorted_values.sort(reverse = True)
            MIN_STRAIGHT = [ 14, 5, 4, 3, 2 ] # Exception to consecutive ordeer for straight
            
            for i in range(1, len(sorted_values)): # Test consecutive
                if sorted_values[i - 1] - sorted_values[i] != 1:
                    straight = False
                    break

            if straight == False and sorted_values == MIN_STRAIGHT:
                sorted_values = MIN_STRAIGHT
                sorted_values.pop(0)
                sorted_values.append(1) # 5, 4, 3, 2, 1 (min straight)
                straight = True

            # Flush
            flush = False
            num_unique_suits = len(set([ card.get_suit() for card in self._cards]))
            if num_unique_suits == 1:
                flush = True

            if straight and flush:
                return (Hand.TYPE_STRAIGHT_FLUSH, sorted_values)
            elif straight:
                return (Hand.TYPE_STRAIGHT, sorted_values)
            elif flush:
                return (Hand.TYPE_FLUSH, sorted_values)
            
            # High Card
            else:
                return (Hand.TYPE_HIGH_CARD, sorted_values)

        elif num_unique_values == Hand.HAND_SIZE - 1:
            # Pair
            hand_values = []
            raw_values = [ card.get_value() for card in self._cards ]
            most_common = Counter(raw_values).most_common()

            most_common.sort(key = lambda value_freq: (value_freq[FREQUENCY], value_freq[VALUE]), reverse = True)

            for value, _ in most_common:
                if value not in hand_values:
                    hand_values.append(value)

            return (Hand.TYPE_PAIR, hand_values)

        elif num_unique_values == Hand.HAND_SIZE - 2:
            # Two Pair | Three of a kind
            hand_values = []
            raw_values = [ card.get_value() for card in self._cards]
            most_common = Counter(raw_values).most_common()

            most_common.sort(key = lambda value_freq: (value_freq[FREQUENCY], value_freq[VALUE]), reverse = True)

            hand_type = Hand.TYPE_UNKNOWN
            _, highest_frequency = most_common[0]

            if highest_frequency == 3:
                hand_type = Hand.TYPE_THREE_OF_A_KIND
            elif highest_frequency == 2:
                hand_type = Hand.TYPE_TWO_PAIR
            else:
                hand_values = raw_values
                return (hand_type, hand_values)

            multi_present_vals = []
            non_paired_vals = []

            for value, frequency in most_common:
                if frequency == highest_frequency:
                    multi_present_vals.append(value)
                else:
                    non_paired_vals.append(value)

            multi_present_vals.sort(reverse = True)
            non_paired_vals.sort(reverse = True)

            hand_values = multi_present_vals + non_paired_vals

            return (hand_type, hand_values)

        elif num_unique_values == Hand.HAND_SIZE - 3:
            # Full House | Four of a Kind
            hand_values = []
            raw_values = [ card.get_value() for card in self._cards]
            most_common = Counter(raw_values).most_common()

            most_common.sort(key = lambda value_freq: (value_freq[FREQUENCY], value_freq[VALUE]), reverse = True)

            hand_type = Hand.TYPE_UNKNOWN
            _, highest_frequency = most_common[0]

            if highest_frequency == 4:
                hand_type = Hand.TYPE_FOUR_OF_A_KIND
            elif highest_frequency == 3:
                hand_type = Hand.TYPE_FULL_HOUSE
            else:
                hand_values = raw_values
                return (hand_type, hand_values)

            for value, _ in most_common:
                if value not in hand_values:
                    hand_values.append(value)

            return (hand_type, hand_values)

        else:
            return (Hand.TYPE_UNKNOWN, [ card.get_value() for card in self._cards ])
