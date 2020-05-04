"""
GameData:
    Contains all of the necesssary information for the game and its players
"""

"""
Imports
"""
from copy       import deepcopy
from itertools  import combinations
from random     import randint

from deck       import Deck
from hand       import Hand
from gamemove   import GameMove
from gamesetup  import GameSetup
from gametimer  import GameTimer
from player     import Player

class GameData:
    """
    Contants
    """
    DEALER_IDX              = 0 ### Designated position of the dealer
    HEADS_UP_PLAYER_COUNT   = 2 ### Number of players in a heads-up game
    INITIAL_ROUND_NUMBER    = 1 ### Round number for the first round
    LEFT_POS_OF_PLAYER      = 1 ### Relative position to the left of a player

    """
    Constructor
    """
    def __init__(self, num_players):
        """
        Game setup properies
        """
        self._game_setup                = None          ### Holds setup data for the game
        self._big_blind_amt             = 0             ### Current big blind size
        self._game_timer                = None          ### Game timer to track the interval of increasing the big blind
        self._players                   = None          ### List of players in the game (to be initialized later)
        self._starting_num_players      = num_players   ### Number of players in the game

        """
        Current hand properies
        """
        self._pot                       = 0             ### Current size of the pot
        self._players_in_hand           = None          ### All players in the current hand
        self._hand_players_played_move  = None          ### Tracks if a player 
        self._agressor_pos              = 0             ### Position of the player with the highest bet on the table

    """
    Helper Methods
    """
    def _order_players(self, dealer_idx):
        """
        Rotate/Cut the list of players so that the player at the dealer index is first on the list
        """
        self._players = self._players[dealer_idx:] + self._players[:dealer_idx]

    """
    Getter Methods
    """
    def get_round_number(self):
        return self._game_setup.round_number

    def get_remaining_time(self):
        return self._game_timer.get_remaining_time()

    def get_blind_positions(self):
        """
        Local Variables
        """
        small_blind = 0
        big_blind   = 0

        """
        Dermine the small blind position: Dealer if the game is heads-up, player after dealer otherwise
        """
        if len(self._players) == GameData.HEADS_UP_PLAYER_COUNT:
            small_blind = GameData.DEALER_IDX
        else:
            small_blind = self.get_next_player_pos(GameData.DEALER_IDX)

        big_blind = self.get_next_player_pos(small_blind)

        return (small_blind, big_blind)

    """
    Get a copy of every player as a list
    """
    def get_players(self):
        return deepcopy(self._players)

    """
    Get a copy of a player at a specificed index
    """
    def get_hand_player(self, player_idx=0):
        return deepcopy(self._players_in_hand[player_idx])

    """
    Get the number of remaining players in the hand
    """
    def get_num_players_in_hand(self):
        return len(self._players_in_hand)

    """
    Get the current pot size
    """
    def get_pot(self):
        return self._pot

    """
    Get the position of the player located to the left of the given player position
    Since the table is circular, moving out of bounds goes to the other side of the list
    parameter only_in_hand: Do we count all players or just those who are still in the hand?
    """
    def get_next_player_pos(self, pos, only_in_hand=True):
        players = self._players_in_hand if only_in_hand else self._players
        return (pos + GameData.LEFT_POS_OF_PLAYER) % len(players)

    """
    Get the size of the maximum bet that is currently in play
    """
    def get_max_action(self):
        player_actions = [ player.get_action() for player in self._players_in_hand ]
        return max(player_actions)

    """
    Get the current size of the big blind
    """
    def get_big_blind_amt(self):
        return self._big_blind_amt

    """
    Get a copy of the winning player if there is one (i.e. only 1 player left in the game)
    """
    def get_winner(self):
        winner = None

        if len(self._players) == 1:
            winner = self._players[0]

        return deepcopy(winner)

    """
    Game Setup Methods
    """
    def setup_game_data(self, game_setup):
        """
        Set the game setup object to the passed value
        """
        self._game_setup = game_setup

        """
        Set the current big blind to the initial big blind
        """
        self._big_blind_amt = self._game_setup.starting_big_blind

        """
        Raise the blinds for every passed round number (to catch up on the blind schedule)
        """
        for _ in range(GameData.INITIAL_ROUND_NUMBER, self._game_setup.round_number):
            self.raise_blinds()

        """
        Create a game timer instance to call the blind increase method at the interval time
        If the initial start time is different from the general interval, include that in the
        construction of the timer
        """
        self._game_timer = GameTimer(
            self._game_setup.blind_increase_interval,
            self._game_setup.handle_time_expired, 
            init_start_time=self._game_setup.init_timestamp
        )

        """
        Set up players and cards (load initial player data if there is any)
        """
        self.setup_players(loaded_players=self._game_setup.init_player_state)
        self.setup_cards()

    def setup_players(self, loaded_players=None):
        """
        Create each player and give each player a starting stack
        """

        if loaded_players is None:

            self._players = [ Player() for _ in range(self._starting_num_players) ]

            for player in self._players:
                player.collect_chips(self._game_setup.starting_chip_count)

            first_dealer = randint(0, self._starting_num_players - 1)

        else:

            self._players = loaded_players

            for player in self._players:
                player.pass_hole_cards()

            first_dealer = 1

        """
        Randomly decide who is the first dealer and order the players to set dealer to first position
        """
        self._order_players(first_dealer)

    """
    Create a deck of cards and shuffle them
    """
    def setup_cards(self, loaded_players=False):
        self._deck = Deck()
        self._deck.shuffle()

    """
    Hand Setup Methods
    """
    def setup_hand_players(self):
        """
        Add each player to a player buffer that manages the current hand
        Also create a list that tracks if each player has played in the current betting round at least once
        """
        self._players_in_hand           = self._players[:]
        self._hand_players_played_move  = [ False ] * self.get_num_players_in_hand()

    def raise_blinds(self):
        """
        Blind raising scheme is to add the starting big blind to the current big blind
        """
        self._big_blind_amt += self._game_setup.starting_big_blind

    def blinds_maxed_out(self):
        """
        Determine if the current big blind should not be raised any higher
        This is done by checking if the big blind meets or exceeds half of the value of every single chip in the game
        """
        return self._big_blind_amt >= ( self._game_setup.starting_chip_count * self._starting_num_players ) / 2

    def start_timer(self):
        """
        Start the game timer and return the amount of time it is set for
        """
        self._game_timer.start()

    def pass_cards(self, num_hole_cards):
        """
        Pass cards to each player
        """
        for _ in range(num_hole_cards):
            for player in self._players_in_hand:
                card = self._deck.draw_card()
                player.take_hole_card(card)
            
        """
        Return a copy of the players
        """
        return deepcopy(self._players)

    def make_blind_bets(self):
        """
        Find the small and big blind players
        """
        small_idx, big_idx  = self.get_blind_positions() 
        small_blind         = self._players_in_hand[small_idx]
        big_blind           = self._players_in_hand[big_idx]
        
        """
        Have the small blind and big blind bet blinds
        """
        small_blind.bet(self._big_blind_amt / 2)
        big_blind.bet(self._big_blind_amt)

        """
        Update the maximum action to the big blind and set the current agressor to the big blind
        """
        self._aggressor_pos = big_idx

    """
    Gameplay Methods
    """
    def mark_next_round(self):
        """
        Initialize or increase the round number
        """
        if not self._game_setup.round_number:
            self._game_setup.round_number = GameData.INITIAL_ROUND_NUMBER
        else:
            self._game_setup.round_number += 1

    def get_num_available_betters(self):
        """
        Find the number of players who are able to bet chips (stack size is not empty)
        """
        num_available_betters = 0

        for player in self._players:
            if player.get_stack_size() > 0:
                num_available_betters += 1
        
        return num_available_betters

    def move_action_to_pot(self):
        """
        Add all player's action (chips bet) to the pot and reset all player action
        """
        for player in self._players:
            self._pot += player.release_action()
        
        """
        Set the maximum action back to zero and reset the last aggressor to no one
        """
        self._aggressor_pos = None

    def flip_board_cards(self, num_board_cards):
        """
        Burn a card
        """
        self._deck.draw_card()

        """
        Draw cards from the deck and add them to the board
        """
        board_cards = list()
        for _ in range(num_board_cards):
            board_card = self._deck.draw_card()
            board_cards.append(board_card)

        """
        Return a copy the board cards
        """
        return deepcopy(board_cards)

    def evaluate_hands(self, board):
        player_hand_triple_list = list()

        """
        Create a triple for each player in the hand:
            * First value is the player's position (relative to the dealer)
            * Second value is a copy of the player instance
            * Third value is the best possible hand that can be made with the player's hole cards and the board
        """
        num_players_in_hand = self.get_num_players_in_hand()

        for player_idx in range(num_players_in_hand):
            """
            Find all combinations of hole and board cards and find the one with the maximum value
            """
            player              = self._players_in_hand[player_idx]
            hole_cards          = player.get_hole_cards()
            hand_cards          = hole_cards + board
            hand_combinations   = combinations(hand_cards, Hand.HAND_SIZE)
            optimal_hand        = max( [ Hand(hand_cards) for hand_cards in hand_combinations ] )

            """
            Create the triple and add it to the list
            """
            player_hand_triple_list.append( ( player_idx, deepcopy(player), optimal_hand ) )

        """
        Sort the position-player-hand triples by the value of the hand (best hand at the beginning of the list)
        """
        PLAYER_HAND = 2
        player_hand_triple_list.sort(key=lambda player_trip: player_trip[PLAYER_HAND], reverse=True)

        """
        Determine the positions of every player with the best hand
        """
        winner_positions    = list()
        _, _, best_hand     = player_hand_triple_list[0]
        num_players_in_hand = self.get_num_players_in_hand()

        for i in range(num_players_in_hand):
            hand_pos, _, hand = player_hand_triple_list[i]
            if hand == best_hand:
                winner_positions.append(hand_pos)
            else:
                break

        """
        Return the sorted triples and the number of winners
        """
        return (player_hand_triple_list, winner_positions)

    def pass_pot_to_winners(self, player_pos_list=[0]):
        """
        Give the winning players (at given indices) the number of chips in the pot and reset the pot
        divided by the number of ways to split (default 1 player wins so no split)
        """
        split = len(player_pos_list)

        for player_idx in player_pos_list:
            self._players_in_hand[player_idx].collect_chips( self._pot / split )
        
        self._pot = 0

    """
    Betting Round Methods
    """
    def init_betting_round(self):
        """
        Indicate that no players have played a turn yet
        """
        for i in range(len(self._hand_players_played_move)):
            self._hand_players_played_move[i] = False

    def play_move(self, player_idx, move, amount):
        """
        Local Variables
        """
        player      = self._players_in_hand[player_idx]
        stack       = player.get_stack_size()
        max_action  = self.get_max_action()

        if move == GameMove.CHECK:
            """
            CHECK: do nothing but mark that the player has had a turn during this round
            """
            self._hand_players_played_move[player_idx] = True

        elif move == GameMove.BET:
            """
            BET: Add remove the bet amount from the player's stack and add it to the player's action
            """
            if amount > stack:
                amount = stack

            player.bet(amount)

            """
            A bet sets the maximum action to the bet size (player's new action) and sets this player to the current aggressor
            """
            self._aggressor_pos = player_idx

            """
            Indicate that the player has had a turn during this betting round
            """
            self._hand_players_played_move[player_idx] = True

        elif move == GameMove.CALL:
            """
            CALL: Player bets to match player's action to the current highest bet
            """
            player_action   = player.get_action()
            amount_to_call  = max_action - player_action

            """
            If the call requires more chips than the player has,
            then each player who has bet this amount takes the chips in their action back to their stack
            and these players re-bet the caller's current action plus the callers remaining stack.
            Then maximum action is set to this amount, then the caller can make the call
            """
            if amount_to_call > stack:
                maximum_call = player_action + stack
                
                """
                The current aggressor and players between the aggressor and caller must re-bet to set their
                action to the caller's maximum call amount
                """
                prev_player_idx = self._agressor_pos

                while prev_player_idx != player_idx:
                    prev_player         = self._players_in_hand[prev_player_idx]
                    prev_player_action  = prev_player.release_action()

                    prev_player.collect_chips(prev_player_action)
                    prev_player.bet(maximum_call)

                    prev_player_idx = self.get_next_player_pos(prev_player_idx)

                """
                Reset the highest action to the maximum call amount
                and set the caller's amount to call equal to the caller's stack size
                (since the action is already in play)
                """
                amount_to_call = stack
            
            """
            Bet the required amount to call
            """
            player.bet(amount_to_call)

            """
            Indicate that the player has had a turn during this betting round
            """
            self._hand_players_played_move[player_idx] = True

        elif move == GameMove.RAISE:
            """
            RAISE: Set the maximum action (highest bet) to the specified amount 
            """
            player_action = player.get_action()
            maximum_raise = stack + player_action

            """
            If the player does not have enough chips to make the given raise,
            reset the raise amount to the players remaining stack plus the number of chips the player
            already has in play
            """
            if amount is not None and amount > maximum_raise:
                amount = maximum_raise

            """
            Bet the raise amount and update the maximum action to this amount, setting this player to the
            current aggressor
            """
            player.bet(amount - player_action)
            self._aggressor_pos = player_idx

            """
            Indicate that the player has had a turn during this betting round
            """
            self._hand_players_played_move[player_idx] = True

        elif move == GameMove.FOLD:
            """
            FOLD: remove the player from the hand entirely (player action will be reset when action is passed to pot)
            """
            self._players_in_hand.pop(player_idx)
            self._hand_players_played_move.pop(player_idx)

        """
        If an amount was set, return the actual amount
        """
        return amount

    def skip_player(self, player_idx):
        """
        Consider the player at the given index to have moved even if a move has not been made
        """
        self._hand_players_played_move[player_idx] = True

    def set_action_for_all_players(self, action):
        """
        Adjust each player's action to the specified amount
        """
        for player in self._players_in_hand:
            """
            Return all action to each player's stack
            """
            player_action = player.release_action()
            player.collect_chips(player_action)

            """
            Each player re-bets the lowest action
            """
            player.bet(action)

    def is_round_over(self):
        """
        Determine if the round is over by checking
        if there is just one player left in the hand
        OR
        if all players have had at least 1 turn 
        and the action is equal amongst all players
        """
        num_players_in_hand = self.get_num_players_in_hand()

        if num_players_in_hand > 1:
            all_players_played  = all(self._hand_players_played_move)
            player_actions      = [ player.get_action() for player in self._players_in_hand ]
            action_is_equal     = player_actions == [ player_actions[0] ] * len(player_actions)
            round_over          = all_players_played and action_is_equal
        else:
            """
            Only one player in hand: the round is automatically over
            """
            round_over = True

        return round_over

    """
    Hand Cleanup Methods
    """
    def eliminate_busted_players(self):
        """
        Remove all players who have no more chips
        """
        self._players = [ player for player in self._players if player.get_stack_size() > 0 ]

    def rotate_dealer(self):
        """
        Set the new dealer to the player left of the current dealer and re-order players by dealer
        """
        new_dealer_idx = self.get_next_player_pos(GameData.DEALER_IDX, only_in_hand=False)
        self._order_players(new_dealer_idx)

    def reset_cards(self, board):
        """
        Remove hole cards from each player and reset/shuffle the deck
        """
        for player in self._players:
            player.pass_hole_cards()
        
        self._deck.reset()
        self._deck.shuffle()
