class Player:
	_count = 0

	def __init__(self, starting_chips):
		self._is_dealer = False
		self._num_chips = starting_chips
		self._id = Player._count
		Player._count += 1

	def __str__(self):
		return "Player %d" % (self._id + 1) # Add 1 to adjust for 0-indexing

	### Chip Stack Modules ###
	def get_chip_count(self):
		return self._num_chips

	def bet(self, num_to_bet):
		if num_to_bet > self._num_chips:
			actual_bet = self._num_chips
			self._num_chips = 0
			return actual_bet

		self._num_chips -= num_to_bet
		return num_to_bet

	def collect_chips(self, num_received):
		self._num_chips += num_received

	### Dealer Button Modules ###
	def is_dealer(self):
		return self._is_dealer

	def pass_dealer_button(self):
		self._is_dealer = True

	def remove_dealer_button(self):
		self._is_dealer = False
	
