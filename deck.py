from random import shuffle

from card 	import Card

class Deck:
	def __init__(self):
		self._setup_cards()

	def reset(self):
		self._setup_cards()

	def _setup_cards(self):
		self._cards = []
		for suit in range(len(Card.SUITS)): # Use numerical values for suits in model
			for value in Card.VALUES:
				self._cards.append( Card(suit, value) )

	def shuffle(self):
		shuffle(self._cards)

	def draw_card(self):
		if len(self._cards) == 0:
			return None

		card = self._cards.pop(0)
		return card
