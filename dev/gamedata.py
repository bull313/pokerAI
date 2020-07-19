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
    DEALER_IDX              = 0     ### Designated position of the dealer
    HEADS_UP_PLAYER_COUNT   = 2     ### Number of players in a heads-up game
    INITIAL_POT             = [ 0 ] ### Default initial state of the pot (one main pot with no chips in)
    INITIAL_ROUND_NUMBER    = 1     ### Round number for the first round
    LEFT_POS_OF_PLAYER      = 1     ### Relative position to the left of a player

    """
    Constructor
    """
    def __init__(self):
        """
        Game setup properies
        """
        self._big_blind_amt             = 0                     ### Current big blind size
        self._game_setup                = None                  ### Holds setup data for the game
        self._game_timer                = None                  ### Game timer to track the interval of increasing the big blind
        self._players                   = None                  ### List of players in the game (to be initialized later)

        """
        Current hand properies
        """
        self._aggressor_pos             = 0                     ### Position of the player with the highest bet on the table
        self._board                     = list()                ### List of community cards
        self._hand_players_played_move  = None                  ### Tracks if a player 
        self._pot                       = GameData.INITIAL_POT  ### List of sizes of all pots (main and side)
        self._pot_contenders            = list()                ### Corrsponding list containing all players contending for each pot
        self._prev_action_folded        = False                 ### Was the last action a fold?             

    """
    Private Methods
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
        Determine the small blind position: Dealer if the game is heads-up, player after dealer otherwise
        """
        if len(self._players) == GameData.HEADS_UP_PLAYER_COUNT:
            small_blind = GameData.DEALER_IDX
        else:
            small_blind = self.get_next_player_pos(GameData.DEALER_IDX, only_in_hand=False)

        """
        Find the big blind relative to the small blind
        """
        big_blind = self.get_next_player_pos(small_blind, only_in_hand=False)

        """
        Return Result
        """
        return (small_blind, big_blind)
    
    def get_button_positions(self):
        """
        Get the dealer and blind positions
        """
        small_blind_pos, big_blind_pos  = self.get_blind_positions()
        dealer_pos                      = GameData.DEALER_IDX
        positions                       = None

        """
        Include small blind only if this is not a heads-up game
        """
        if len(self._players) == GameData.HEADS_UP_PLAYER_COUNT:
            positions = ( dealer_pos, big_blind_pos )
        else:
            positions = ( dealer_pos, small_blind_pos, big_blind_pos )

        """
        Return Result
        """
        return positions

    def get_players(self):
        """
        Get a copy of every player as a list
        """
        return deepcopy(self._players)

    def get_hand_player(self, pot_idx=-1, player_idx=None):
        """
        Get a copy of a player at a specificed index
        """
        player = deepcopy(self._pot_contenders[pot_idx][player_idx]) if player_idx is not None else None

        if player is None:
            """
            If the index was not specified, get the first non-None player
            """
            for contender in self._pot_contenders[pot_idx]:

                if contender is not None:
                    player = contender
                    break

        """
        Return Result
        """
        return player

    def get_num_players_in_hand(self):
        """
        Get the number of remaining players in the hand
        """
        remaining_players = list()

        """
        Remove folded players
        """
        for contender in self._pot_contenders[-1]:
            
            if contender is not None:
                remaining_players.append(contender)

        """
        Return Result
        """
        return len(remaining_players)

    def get_num_players_all_in(self):
        """
        Get the number of players in the hand who are all-in
        """
        return len([ player for player in self._pot_contenders[-1] if player is not None and player.get_stack_size() == 0 ])

    def get_pot(self):
        """
        Create a pot list buffer
        """
        pots = list()

        """
        For every pot (main and side) add up the total current action with the value of center chips
        to get each actual pot value
        """
        for i in range(len(self._pot)):
            center_pot      = self._pot[i]
            total_action    = sum([ player.get_action() for player in self._pot_contenders[i] if player is not None ])
            pots.append(center_pot + total_action)

        """
        Return Result
        """
        return pots

    def get_num_pots(self):
        """
        Get the number of pots (main + side pots)
        """
        return len(self._pot)

    def get_board(self):
        """
        Get a copy of the community cards
        """
        return deepcopy(self._board)

    def get_next_player_pos(self, pos, only_in_hand=True):
        """
        Get the position of the player located to the left of the given player position
        Since the table is circular, moving out of bounds goes to the other side of the list
        parameter only_in_hand: Do we count all players or just those who are still in the hand?

        Local Variables
        """
        players         = self._pot_contenders[-1] if only_in_hand else self._players
        num_players     = len(players)
        offset          = GameData.LEFT_POS_OF_PLAYER
        next_player_pos = ( pos + offset ) % num_players

        """
        Rotate to the next non-folded player
        """
        while players[ next_player_pos ] is None:
            offset          += GameData.LEFT_POS_OF_PLAYER
            next_player_pos = ( pos + offset ) % len(players)

        """
        Return Result
        """
        return next_player_pos
        
    def get_max_action(self):
        """
        Get the size of the maximum bet that is currently in play
        """
        player_actions = [ player.get_action() for player in self._pot_contenders[-1] if player is not None ]
        return max(player_actions)

    def get_big_blind_amt(self):
        """
        Get the current size of the big blind
        """
        return self._big_blind_amt

    def get_winner(self):
        """
        Get a copy of the winning player if there is one (i.e. only 1 player left in the game)
        """
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

            self._players = [ Player() for _ in range(self._game_setup.starting_num_players) ]

            for player in self._players:
                player.collect_chips(self._game_setup.starting_chip_count)

            first_dealer = randint(0, self._game_setup.starting_num_players - 1)

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
        self._pot_contenders.clear()
        self._pot_contenders.append( self._players[:] )
        self._hand_players_played_move  = [ False ] * self.get_num_players_in_hand()

    def setup_pot(self):
        self._pot = deepcopy( GameData.INITIAL_POT )

    def raise_blinds(self):
        """
        Use the established blind raising scheme to raise the blinds
        """
        self._big_blind_amt = self._game_setup.blind_increase_scheme(self._big_blind_amt, self._game_setup.starting_big_blind)

    def blinds_maxed_out(self):
        """
        Determine if the current big blind should not be raised any higher
        This is done by checking if the big blind meets or exceeds half of the value of every single chip in the game
        """
        return self._big_blind_amt >= ( self._game_setup.starting_chip_count * self._game_setup.starting_num_players ) / 2

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
            for player in self._players:
                card = self._deck.draw_card()
                player.take_hole_card(card)

    def make_blind_bets(self):
        """
        Find the small and big blind players
        """
        small_idx, big_idx  = self.get_blind_positions() 
        small_blind         = self._players[small_idx]
        big_blind           = self._players[big_idx]
        
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
        return len([ player for player in self._pot_contenders[-1] if player is not None and player.get_stack_size() > 0 ])

    def move_action_to_pot(self):
        """
        Add all player's action (chips bet) to the pot and reset all player action
        ALWAYS select the last pot in the list: new chips ALWAYS go to the newest side
        pot if there are any
        """
        initial_pot_idx         = len(self._pot) - 1
        remaining_action_exists = True

        while remaining_action_exists:
            """
            Get the minimum action in play
            """
            min_action = min( [ player.get_action() for player in self._pot_contenders[-1] if player is not None ] )

            """
            Take the minimum action from each player and add to the current pot
            """
            for player in self._pot_contenders[-1]:

                if player is not None:
                    self._pot[-1] += player.release_action(amount=min_action)

            """
            Check if any player has any remaining action
            """
            remaining_action_exists = any([ player.get_action() > 0 for player in self._pot_contenders[-1] if player is not None ])

            """
            Create a side pot if any remaining action exists
            """
            if remaining_action_exists:
                self._create_side_pot()

        """
        Create an additional side pot if any of the remaining pot contenders is all in
        """
        any_player_all_in           = any( [ player.get_stack_size() == 0 for player in self._pot_contenders[-1] if player is not None ] )
        multiple_available_betters  = self.get_num_available_betters() > 1

        if any_player_all_in and multiple_available_betters:
            self._create_side_pot()

        """
        Add action of folded players to the initial pot (pot before side pots were created)
        """
        for player in self._players:
            self._pot[initial_pot_idx] += player.release_action()
        
        """
        Reset the last aggressor to no one
        """
        self._aggressor_pos = None

    def _create_side_pot(self):
        """
        Create a side pot that is initially empty
        """
        self._pot.append(0)

        """
        Add a list of all players contending for this side pot (any players who still have chips)
        """
        new_pot_contenders = list()

        for player in self._pot_contenders[-1]:

            if player is None or ( player.get_stack_size() + player.get_action() ) > 0:
                """
                Add element directly if it is already None or has a stack size of 0
                """
                new_pot_contenders.append(player)
            else:
                """
                Add a "None" placeholder to preserve table order
                """
                new_pot_contenders.append(None)

        self._pot_contenders.append(new_pot_contenders)

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

    def evaluate_hands(self, pot_idx):
        player_hand_triple_list = list()

        """
        Create a triple for each player in the hand:
            * First value is the player's position (relative to the dealer)
            * Second value is a copy of the player instance
            * Third value is the best possible hand that can be made with the player's hole cards and the board
        """
        for player_idx in range(len(self._pot_contenders[-1])):
            """
            Find all combinations of hole and board cards and find the one with the maximum value
            """
            player = self._pot_contenders[pot_idx][player_idx]

            if player is not None:
                hole_cards          = player.get_hole_cards()
                hand_cards          = hole_cards + self._board
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
        winner_positions            = list()
        winner_pos, _, best_hand    = player_hand_triple_list[0]

        winner_positions.append(winner_pos)

        for i in range(1, len(player_hand_triple_list)):

            hand_pos, _, hand = player_hand_triple_list[i]

            if hand == best_hand:
                winner_positions.append(hand_pos)
            else:
                break

        """
        Return the sorted triples and the number of winners
        """
        return (player_hand_triple_list, winner_positions)

    def pass_pot_to_winners(self, pot_idx, player_pos_list=None):
        """
        Give the winning players (at given indices) the number of chips in the pot and reset the pot
        divided by the number of ways to split (default 1 player wins so no split)
        """
        # TODO: when all players but 2 fold then the last player folds on the flop, seems like 5 small blind chips are not moved?
        if player_pos_list is None:
            """
            If no position list was given, pass the pot to all remaining players (contenders)
            """
            remaining_players   = [ player for player in self._pot_contenders[pot_idx] if player is not None ]
            split               = len(remaining_players)
            
            for player in remaining_players:
                player.collect_chips( self._pot[pot_idx] / split )

        else:
            """
            Only give the pot to the specified positions
            """
            split = len(player_pos_list)

            for player_idx in player_pos_list:
                self._pot_contenders[pot_idx][player_idx].collect_chips( self._pot[pot_idx] / split )
    
    def add_board_cards(self, board_cards):
        """
        Add cards to the game board
        """
        self._board += board_cards

    """
    Betting Round Methods
    """
    def init_betting_round(self):
        """
        Indicate that no players have played a turn yet
        """
        num_contenders                  = len(self._pot_contenders[-1])
        self._hand_players_played_move  = [ False ] * num_contenders

        """
        Assume all folded players have played (in order to be skipped)
        """
        for i in range(num_contenders):

            contender = self._pot_contenders[-1][i]

            if contender is None:
                self._hand_players_played_move[i] = True

    def play_move(self, player_idx, move, amount):
        """
        Local Variables
        """
        player      = self._pot_contenders[-1][player_idx]
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
            Adjust the amount to call to be the current player's stack at max
            """
            if amount_to_call > stack:
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
            This includes contention in all pots (main and side)
            """
            self._pot_contenders[-1][player_idx] = None
            self._prev_action_folded             = True

            for pot_contenders in self._pot_contenders:
                
                for i in range(len(pot_contenders)):

                    if pot_contenders[i] == player:
                        pot_contenders[i] = None

            self._hand_players_played_move[player_idx] = True

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
        for player in self._pot_contenders[-1]:

            if player is not None:
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
        (exception: a player can have less than maixmum action if the player is all-in)
        """
        if self.get_num_players_in_hand() > 1:
            all_players_played          = all(self._hand_players_played_move)
            max_action                  = self.get_max_action()
            player_sufficient_actions   = [ player.get_action() == max_action or player.get_stack_size() == 0 for player in self._pot_contenders[-1] if player is not None ]
            action_is_sufficient        = all(player_sufficient_actions)
            round_over                  = all_players_played and action_is_sufficient
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
        And return a copy of all eliminated players
        """
        eliminated_players  = [ deepcopy(player)    for player in self._players if player.get_stack_size() ==   0 ]
        self._players       = [ player              for player in self._players if player.get_stack_size() >    0 ]

        """
        Return Result
        """
        return eliminated_players

    def rotate_dealer(self):
        """
        Set the new dealer to the player left of the current dealer and re-order players by dealer
        """
        new_dealer_idx = self.get_next_player_pos(GameData.DEALER_IDX, only_in_hand=False)
        self._order_players(new_dealer_idx)
    
    def clear_board(self):
        """
        Clear the list of board cards
        """
        self._board.clear()

    def reset_cards(self):
        """
        Remove hole cards from each player and reset/shuffle the deck
        """
        for player in self._players:
            player.pass_hole_cards()
        
        self._deck.reset()
        self._deck.shuffle()
