from copy       import deepcopy
from itertools  import combinations
from random     import randint

from deck       import Deck
from hand       import Hand
from player     import Player

class GameData:
    NUM_PLAYERS = 2

    def setup_players(self, starting_chip_count, starting_big_blind):
        self._starting_chip_count = starting_chip_count
        self._starting_big_blind = starting_big_blind

        self._players = [ Player(self._starting_chip_count) for _ in range(GameData.NUM_PLAYERS) ]

        first_dealer = randint(0, GameData.NUM_PLAYERS - 1)

        for i in range(GameData.NUM_PLAYERS):
            if i == first_dealer:
                self._players[i].give_dealer_button()
            else:
                self._players[i].remove_dealer_button()

        self.order_players(first_dealer)

    def order_players(self, dealer_idx): # Dealer is first value in list
        rotating_players = []
        for _ in range(dealer_idx):
            rotating_players.append(self._players.pop(0))

        for player in rotating_players:
            self._players.append(player)

    def setup_cards(self):
        self._deck = Deck()
        self._deck.shuffle()

    def pass_cards(self, num_hole_cards):
        for _ in range(num_hole_cards):
            for player in self._players:
                card = self._deck.draw_card()
                player.take_hole_card(card)
            
        return self._players[:] # Return a copy of the list

    def get_board_cards(self, num_board_cards):
        self._deck.draw_card() # Burn a card
        board_cards = []
        for _ in range(num_board_cards):
            board_card = self._deck.draw_card()
            board_cards.append(board_card)
        return board_cards

    def evaluate_hands(self, board):
        hands = []

        for player in self._players:
            hole_cards = player.get_hole_cards()
            hand_cards = hole_cards + board

            hand_combinations = combinations(hand_cards, Hand.HAND_SIZE)
            optimal_hand = max( [ Hand(hand_cards) for hand_cards in hand_combinations ] )

            hands.append( ( player, optimal_hand ) )

        HAND_OBJ = 1
        hands.sort(key = lambda x: x[HAND_OBJ], reverse = True) # Sort by best hand value to worst

        return hands

    def pass_pot_to_winner(self, winner):
        pot = 0
        for player in self._players:
            if player is not winner:
                pot += player.bet(self._starting_big_blind)

        winner.collect_chips(pot)

    def eliminate_busted_players(self):
        cleaned_player_list = []
        for player in self._players:
            if player.get_chip_count() > 0:
                cleaned_player_list.append(player)

        self._players = cleaned_player_list

    def get_winner(self):
        if len(self._players) == 1:
            return self._players[0]
        else:
            return None

    def rotate_dealer(self):
        if len(self._players) > 1:
            OLD_DEALER_IDX = 0
            NEW_DEALER_IDX = 1
            self._players[OLD_DEALER_IDX].remove_dealer_button()
            self._players[NEW_DEALER_IDX].give_dealer_button()

        self.order_players(NEW_DEALER_IDX)

    def reset_cards(self, board):
        for player in self._players:
            player.pass_hole_cards()
        
        self._deck.reset()
        self._deck.shuffle()
