from gamedata   import GameData
from gameui     import GameUI

class Game:
    NUM_HOLE_CARDS  = 2
    BOARD_ROUNDS = [ 3, 1, 1 ]

    def __init__(self):
        self._ui = GameUI()
        self._game_data = GameData()

    def setup(self):
        starting_chip_count = self._ui.get_starting_chip_count()
        starting_big_blind = self._ui.get_starting_big_blind(starting_chip_count)

        self._game_data.setup_players(starting_chip_count, starting_big_blind)
        self._game_data.setup_cards()

    def play_game(self):
        game_over = False

        while not game_over:
            self._ui.display_round_border()

            # Set up round
            players_preflop = self._game_data.pass_cards(Game.NUM_HOLE_CARDS)
            self._ui.display_player_data(players_preflop)

            # Preflop
            self._ui.start_betting_round()

            # Postflop streets
            board = []
            for board_name_idx in range(len(Game.BOARD_ROUNDS)):
                board += self._game_data.get_board_cards(Game.BOARD_ROUNDS[board_name_idx])
                self._ui.show_board(board_name_idx, board)
                self._ui.start_betting_round()

            # Showdown
            ordered_player_hand_pairs  = self._game_data.evaluate_hands(board)
            self._ui.show_results(ordered_player_hand_pairs )
            WINNER_INDEX = PLAYER_INDEX = 0 # Players are ordered from best hand to worst
            self._game_data.pass_pot_to_winner(ordered_player_hand_pairs [WINNER_INDEX][PLAYER_INDEX])

            # Cleanup
            self._game_data.eliminate_busted_players()
            winner = self._game_data.get_winner()

            if winner is None:
                self._game_data.rotate_dealer()
                self._game_data.reset_cards(board)
            else:
                game_over = True

        self._ui.display_winner(winner)
