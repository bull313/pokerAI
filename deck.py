from random import shuffle
from card import Card

class Deck:
	def __init__(self):
		self._cards = []
		self._discard_pile = []
		for suit in range(len(Card.SUITS)): # Use numerical values for suits in model
			for value in Card.VALUES:
				self._cards.append( Card(suit, value) )

	def shuffle(self):
		shuffle(self._cards)

	def draw_card(self):
		if len(self._cards) == 0:
			return None

		card = self._cards[0]
		self._cards.pop(0)
		self._discard_pile.append(card)
		return card

	def reset(self):
		while len(self._discard_pile) > 0:
			self._deck.append( self._discard_pile.pop(0) )

