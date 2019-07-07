from deck import Deck
from player import Player

def main():
	starting_chip_count = 0
	valid_starting_chip_count = False

	starting_chip_count = input("Enter starting chip count: ")

	starting_big_blind = 0
	valid_big_blind = False

	while not valid_big_blind:
		starting_big_blind = input("Enter the starting big blind amount: ")
		if starting_big_blind % 2 != 0:
			print("Big blind must be an even number")
		elif starting_big_blind > starting_chip_count:
			print("Big blind must be less than the starting chip count")
		else:
			valid_big_blind = True

	player1 = Player(starting_chip_count)
	player2 = Player(starting_chip_count)

if __name__ == "__main__":
	main()
