class Card:
	SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"] # Suit index-name dictionary
	VALUES = [ i for i in range(2, 15) ] # 2 - A true values

	FACE_CARDS = {
		11: "Jack",
		12: "Queen",
		13: "King",
		14: "Ace"
	} # Values that have other names (for UI)

	def __init__(self, suit, value):
		self._suit = suit
		self._value = value

	def __lt__(self, other):
		return self._value < other._value

	def __str__(self):
		ret_val = ""

		# Value
		if self._value in Card.FACE_CARDS:
			ret_val += Card.FACE_CARDS[ self._value ][0].upper()
		else:
			ret_val += str(self._value)

		# Suit
		ret_val += Card.SUITS[ self._suit ][0].upper()

		return ret_val

	def get_suit(self):
		return self._suit

	def get_value(self):
		return self._value
