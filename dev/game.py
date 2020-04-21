"""
Game:
    Manges the rules and executes the actual game
"""

"""
Imports
"""
from gamedata   import GameData
from gamemove   import GameMove
from gameui     import GameUI

class Game:
    """
    Constants
    """
    BOARD_ROUNDS            = [ 3, 1, 1 ]   ### Number of cards to turn on each street
    NUM_HOLE_CARDS          = 2             ### Number of hole cards per player
    NUM_PLAYERS             = 2             ### Number of players in the game
    REQUIRED_RAISE_MULTIPLE = 2             ### Required raise is this value times the current bet

    """
    Constructor
    """
    def __init__(self):
        self._ui = GameUI()
        self._game_data = GameData(Game.NUM_PLAYERS)
        self._timer_on = False
        self._blinds_maxed_out = False

    """
    Public methods
    """
    def setup(self):
        """
        Get the starting stack, big blind amount, and blind increase time interval from the user
        """
        starting_chip_count     = self._ui.get_starting_chip_count()
        starting_big_blind      = self._ui.get_starting_big_blind(starting_chip_count)
        blind_increase_interval = self._ui.get_blind_increase_interval()

        """
        Set up the game data's stack, big blind, and timer modules
        """
        self._game_data.set_starting_chip_count(starting_chip_count)
        self._game_data.set_starting_big_blind(starting_big_blind)
        self._game_data.set_big_blind_increase_interval(blind_increase_interval, self._handle_time_expired)

        """
        Set up players and cards
        """
        self._game_data.setup_players()
        self._game_data.setup_cards()

    def play_game(self):
        game_over = False
        self._game_data.mark_next_round()

        while not game_over:
            """
            Separate each hand
            """
            self._ui.display_round_border()

            """
            Set up hand
            """
            self._game_data.setup_hand_players()
            self._manage_timer()
            self._game_data.make_blind_bets()
            players_preflop = self._game_data.pass_cards(Game.NUM_HOLE_CARDS)
            self._ui.display_player_data(players_preflop)

            """
            Preflop
            """
            end_hand_before_showdown = self._open_for_betting(preflop=True)
            board = list()

            if not end_hand_before_showdown:
                """
                Postflop streets
                """
                for board_name_idx in range(len(Game.BOARD_ROUNDS)):
                    board += self._game_data.flip_board_cards(Game.BOARD_ROUNDS[board_name_idx])
                    self._ui.show_board(board_name_idx, board)

                    end_hand_before_showdown = self._open_for_betting()

                    if end_hand_before_showdown:
                        break

            
            if end_hand_before_showdown:
                """
                Pass pot to the only remaining player
                """
                self._game_data.pass_pot_to_winners()
                remaining_player = self._game_data.get_hand_player()
                self._ui.show_folded_round(remaining_player)

            else:
                """
                Showdown
                """
                ordered_player_hand_pairs, num_winners = self._game_data.evaluate_hands(board)
                self._ui.show_results(ordered_player_hand_pairs, num_winners)
                winner_positions = list()

                for winner_idx in range(num_winners):
                    pos, _, _ = ordered_player_hand_pairs[winner_idx]
                    winner_positions.append(pos)
                
                self._game_data.pass_pot_to_winners(player_pos_list=winner_positions)

            """
            Cleanup
            """
            self._game_data.eliminate_busted_players()
            winner = self._game_data.get_winner()

            if winner is None:
                self._game_data.rotate_dealer()
                self._game_data.reset_cards(board)
            else:
                game_over = True

        self._ui.display_winner(winner)

    """
    Private methods
    """
    def _manage_timer(self):
        """
        Reset the timer and increase the blinds if the timer has been turned off
        """
        round_number = self._game_data.get_round_number()

        if not self._timer_on:

            if not self._blinds_maxed_out:
                
                """
                Do not raise the blinds on the first round
                """
                if round_number != GameData.INITIAL_ROUND_NUMBER:
                    self._game_data.raise_blinds()

                """
                Determine if the blinds are at the maximum
                """
                if self._game_data.blinds_maxed_out():
                    self._blinds_maxed_out = True

                """
                Set the timer and display a confirmation message
                """
                big_blind = self._game_data.get_big_blind_amt()
                interval_time = self._game_data.start_timer()
                self._timer_on = True
                self._ui.display_timer_set(round_number, big_blind, interval_time)

            else:
                """
                Display that the current big blind amount will not be raised
                Do not restart the timer
                """
                self._ui.display_blinds_maxed_out(self._game_data.get_big_blind_amt())

        else:
            """
            If the timer is currently on, display the remaining time
            """
            remaining_time = self._game_data.get_remaining_time()
            self._ui.display_current_timer_value(round_number, remaining_time)

    def _handle_time_expired(self):
        self._ui.display_time_expired()
        self._game_data.mark_next_round()
        self._timer_on = False

    def _has_multiple_available_betters(self):
        return self._game_data.get_num_available_betters() > 1

    def _open_for_betting(self, preflop=False):
        """
        Start a betting round if more than one player is able to bet
        """
        if preflop or self._has_multiple_available_betters():
            self._start_betting_round(preflop=preflop)
        else:
            self._ui.display_no_bet_from_all_in()

        """
        Move all player action to the pot and display it
        """
        self._game_data.move_action_to_pot()
        self._ui.display_pot(self._game_data.get_pot())

        """
        Determine if the hand has ended prematurely and return it
        """
        return self._is_hand_over()

    def _start_betting_round(self, preflop=False):
        """
        Local Variables
        """
        _, big_blind_idx = self._game_data.get_blind_positions()
        current_player_idx = None
        round_over = False

        """
        Get the position of the first player to act
        """
        if preflop:
            current_player_idx = self._game_data.get_next_player_pos(big_blind_idx)
        else:
            current_player_idx = self._game_data.get_next_player_pos(GameData.DEALER_IDX)

        """
        Game Data setup for a betting round
        """
        self._game_data.start_betting_round()

        """
        Round loop: keep cycling turns until the round is over
        """
        while not round_over:
            """
            Setup: Get a copy of the acting player for UI puproses
            """
            player = self._game_data.get_hand_player(current_player_idx)
            num_players_in_hand_before_move = self._game_data.get_num_players_in_hand()

            """
            Play: Determine, prompt, and play a legal move
            """
            available_moves, action_to_play = self._get_available_moves(player, preflop=preflop)

            if len(available_moves) > 0:
                chosen_move, chosen_amount = self._ui.prompt_available_moves(player, available_moves, action_to_play)
                adjusted_amount = self._game_data.play_move(current_player_idx, chosen_move, chosen_amount)
                self._ui.display_move_made(player, chosen_move, adjusted_amount)
            else:
                """
                Player has no available moves: Skip player and move on
                """
                self._ui.display_no_moves_available(player)
                self._game_data.skip_player(current_player_idx)

            """
            If this player is still in the hand but the player's
            action is lower than the current highest adjust the action to this amount
            """
            still_in_hand = self._game_data.get_num_players_in_hand() == num_players_in_hand_before_move

            if still_in_hand:

                player = self._game_data.get_hand_player(current_player_idx)
                player_action = player.get_action()

                if player_action < self._game_data.get_max_action():
                    self._game_data.set_action_for_all_players(player_action)

            """
            Cleanup: Find the next player to act and determine if the round is over
            """
            current_player_idx = self._game_data.get_next_player_pos(current_player_idx)
            round_over = self._game_data.is_round_over()

    def _get_available_moves(self, player, preflop=False):
        """
        Local Variables
        """
        available_moves         = list()
        action_to_play          = 0
        max_action              = self._game_data.get_max_action()
        player_stack            = player.get_stack_size()
        player_action           = player.get_action()
        player_can_afford_raise = player_stack + player_action >= max_action

        """
        If the player does not have any chips left, there are no options available
        """
        if player_stack > 0:
            """
            Available moves are dependent on the player's action relative to the current highest action
            (and one exception in the preflop round)
            """
            if player_action < max_action:
                available_moves.append(GameMove.CALL)

                """
                If all other players are all-in or this player cannot afford to raise the action 
                Then the player cannot raise the action
                """
                if self._has_multiple_available_betters() and player_can_afford_raise:
                    available_moves.append(GameMove.RAISE)

                """
                Minimum raise is a multiple of the current maximum bet in play
                """
                action_to_play = min(player_stack, Game.REQUIRED_RAISE_MULTIPLE * max_action)

            else:
                available_moves.append(GameMove.CHECK)

                """
                If all other players are all-in, this player cannot raise the action even higher
                """
                if self._has_multiple_available_betters():

                    if preflop and player_can_afford_raise:
                        available_moves.append(GameMove.RAISE)
                    else:
                        available_moves.append(GameMove.BET)
                
                """
                Minimum amount to introduce betting with is the size of the big blind
                EXCEPTION: On preflop, the big blind may raise the big blind
                """
                if preflop:
                    action_to_play = min(player_stack, Game.REQUIRED_RAISE_MULTIPLE * self._game_data.get_big_blind_amt())
                else:
                    action_to_play = min(player_stack, self._game_data.get_big_blind_amt())
            
            """
            Folding is always an option if the player has chips left
            """
            available_moves.append(GameMove.FOLD)

        """
        Return result
        """
        return (available_moves, action_to_play)

    """
    Determine if the hand is over by detecting if there are fewer than 2 players left in the hand
    """
    def _is_hand_over(self):
        return self._game_data.get_num_players_in_hand() < 2
