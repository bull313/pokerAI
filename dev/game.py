"""
Game:
    Manges the rules and executes the actual game
"""

"""
Imports
"""
from gamedata       import GameData
from gamemove       import GameMove
from gamesave       import GameSave
from gamesetup      import GameSetup
from gametheater    import GameTheater
from gameui         import GameUI

class Game:
    """
    Constants
    """
    GAME_CODE_NEW_GAME                  = 0             ### Game is set to play a brand new game
    GAME_CODE_PLAY_LOAD_GAME            = 1             ### Game is set to load and continue and existing game
    GAME_CODE_CONTINUE_GAME             = 2             ### Game is ongoing
    GAME_CODE_PLAYBACK_GAME             = 3             ### Game is set to play back a finished game
    GAME_CODE_NO_PLAY                   = 4             ### Game is set not to play or play back any game
    NUM_CARDS_FOR_BOARD_TYPE            = [ 3, 1, 1 ]   ### Number of cards to turn on each street
    NUM_HOLE_CARDS                      = 2             ### Number of hole cards per player
    NUM_PLAYERS_MIN                     = 2             ### Minimum number of players to start the game
    NUM_PLAYERS_MAX                     = 12            ### Maximum number of players to start the game
    REQUIRED_RAISE_MULTIPLE             = 2             ### Required raise is this value times the current bet
    SHOW_FOLDED_HANDS                   = True          ### Show the remaining player's hand if folded to that player?

    """
    Constructor
    """
    def __init__(self):
        """
        Game Properties
        """
        self._blinds_maxed_out      = False         ### Are the blinds at the highest value?
        self._board                 = list()        ### List of community cards
        self._board_idx             = 0             ### List address for the name of the board
        self._game_data             = GameData()    ### Poker Data Interface Object
        self._game_play_code        = False         ### What kind of game are we playing or playing back (new/load)?
        self._game_save             = None          ### Object that manages saving a game finished or in progress
        self._game_theater          = None          ### Plays back a finished game
        self._hand_actions          = list()        ### List of actions that were made in a hand
        self._ui                    = GameUI()      ### User Interface Object
        self._num_remaining_players = 0             ### Number of remaining players in the game

    """
    Public methods
    """
    def setup(self):
        """
        Set up the game structure with user-entered or loaded values
        """
        starting_chip_count     = None
        starting_big_blind      = None
        blind_increase_interval = None

        """
        Get the name of a new game save or the name of a loaded game save
        """
        game_save_name          = self._ui.get_game_save_name()
        self._game_save         = GameSave(game_save_name)
        self._game_play_code    = Game.GAME_CODE_NEW_GAME

        """
        If the save name exists, prompt if the user wants to load an existing game
        """
        if self._game_save.save_exists():
            self._setup_saved_game()

        if self._game_play_code == Game.GAME_CODE_NEW_GAME:
            self._setup_new_game()

        """
        Set up the game's hot key commands
        """
        self._ui.setup_save_command(self._handle_save_game)

    def play_game(self):
        """
        Play a game with the set game protocol
        """
        winner = None

        """
        If the protocol is to play back a game, use the theater to play back the game
        """
        if self._game_play_code == Game.GAME_CODE_PLAYBACK_GAME and self._game_theater is not None:
            self._game_theater.playback_game()
        elif self._game_play_code != Game.GAME_CODE_NO_PLAY:
            """
            Play a new or loaded game

            Begin listening for hot keys
            """
            self._ui.listen_for_hot_keys()

            """
            Initialize the round number if this is a new game
            """
            if self._game_play_code == Game.GAME_CODE_NEW_GAME:
                self._game_data.mark_next_round()

            """
            Welcome user and begin game
            """
            self._welcome()
            game_over = False

            """
            Game Loop
            """
            while not game_over:
                """
                Visually separate each hand
                """
                self._ui.display_round_border()
                self._setup_hand()
                self._play_hand()
                game_over, winner = self._cleanup_hand()

            """
            Game Finished: Display the winner and attempt to save the game's history for playback
            """
            self._ui.display_winner(winner)
            self._attempt_save_game_history()

    """
    Callback Methods
    """
    def _handle_save_game(self):
        """
        Serialize game save data and display a confirmation message to the user
        """
        save_successful = self._game_save.save()
        save_name = self._game_save.get_game_save_name()
        self._ui.display_game_save_confirm(save_successful, save_name)

    def _handle_time_expired(self):
        """
        Alert the user that time is up and increase the round number
        """
        self._ui.display_time_expired()
        self._game_data.mark_next_round()

    """
    Private Methods
    """
    def _setup_hand(self):
        """
        Check the timer, make blind bets, and pass out cards
        """
        current_time = self._manage_timer()
        self._game_data.setup_hand_players()
        self._game_data.setup_pot()
        self._game_data.make_blind_bets()
        players_preflop = self._game_data.pass_cards(Game.NUM_HOLE_CARDS)

        """
        Get notable positions to label them (dealer, small blind, big blind)
        """
        small_blind_pos, big_blind_pos  = self._game_data.get_blind_positions()
        notable_positions               = ( GameData.DEALER_IDX, small_blind_pos, big_blind_pos )
        self._ui.display_player_data(players_preflop, self._game_data.get_button_positions())

        """
        Begin hand save snapshot
        """
        self._hand_actions.clear()
        round_number = self._game_data.get_round_number()
        self._game_save.begin_hand_snapshot(round_number, players_preflop, current_time)

    def _perform_showdown(self):
        num_pots = self._game_data.get_num_pots()

        for pot_idx in range(num_pots):
            ordered_player_hand_triples, winner_positions = self._game_data.evaluate_hands(pot_idx, self._board)
            
            """
            Display winning players and pass the pot to them
            """
            idx = pot_idx if num_pots > 1 else None
            self._ui.display_showdown_results(ordered_player_hand_triples, len(winner_positions), pot_idx=idx)
            self._game_data.pass_pot_to_winners(pot_idx, player_pos_list=winner_positions)

    def _play_hand(self):
        """
        Execute a hand

        Preflop
        """
        round_folded = self._open_for_betting(preflop=True)
        self._board.clear() # TODO: board should be part of game data class?

        if not round_folded:
            """
            Postflop streets
            """
            self._board_idx = 0

            while self._board_idx < len(Game.NUM_CARDS_FOR_BOARD_TYPE) and round_folded is False:
                self._board += self._game_data.flip_board_cards(Game.NUM_CARDS_FOR_BOARD_TYPE[self._board_idx])
                round_folded = self._open_for_betting()
                self._board_idx += 1
        
        if round_folded:
            """
            Pass pot to the only remaining player
            """
            num_pots = self._game_data.get_num_pots()

            for pot_idx in range(num_pots):
                self._game_data.pass_pot_to_winners(pot_idx)

                """
                Display results
                """
                remaining_player = self._game_data.get_hand_player(pot_idx=pot_idx)
                self._ui.display_folded_round(remaining_player, Game.SHOW_FOLDED_HANDS, pot_idx=pot_idx)

        else:
            """
            Showdown
            """
            self._perform_showdown()

    def _cleanup_hand(self):
        """
        Remove any players who are out of chips
        """
        game_over           = False
        winner              = None
        eliminated_players  = self._game_data.eliminate_busted_players()

        """
        Display eliminated players with their ranks
        And update the number of remaining players in the game
        """
        for player in eliminated_players:
            self._ui.display_player_eliminated(player, self._num_remaining_players)
            self._num_remaining_players -= 1

        """
        Get player data and current time stamp to complete hand snapshot
        """
        players     = self._game_data.get_players()
        timestamp   = self._game_data.get_remaining_time()
        self._game_save.end_hand_snapshot(self._hand_actions[:], self._board[:], players, timestamp)
        
        """
        Check if there is a winner of the game and end theg ame if there is one
        """
        winner = self._game_data.get_winner()

        if winner is None:
            """
            If there are multiple players left, rotate the dealer and reset cards
            """
            self._game_data.rotate_dealer()
            self._game_data.reset_cards(self._board)
        else:
            game_over = True

        """
        Set the game code to continue to prevent load values from popping up again
        """
        self._game_play_code = Game.GAME_CODE_CONTINUE_GAME

        """
        Return game over status and winner if there is one
        """
        return ( game_over, winner )

    def _setup_new_game(self):
        """
        Get the starting stack, big blind amount, and blind increase time interval from the user
        """
        game_setup                          = GameSetup()
        game_setup.starting_num_players     = self._ui.get_num_players(Game.NUM_PLAYERS_MIN, Game.NUM_PLAYERS_MAX)
        game_setup.starting_chip_count      = self._ui.get_starting_chip_count()
        game_setup.starting_big_blind       = self._ui.get_starting_big_blind(game_setup.starting_chip_count)
        game_setup.blind_increase_interval  = self._ui.get_blind_increase_interval()
        game_setup.handle_time_expired      = self._handle_time_expired

        """
        Initialize the number of remaining players
        """
        self._num_remaining_players = game_setup.starting_num_players

        """
        Set up the game data with the received values
        """
        self._game_data.setup_game_data(game_setup)

        """
        Save the button positions
        """
        game_setup.button_positions = self._game_data.get_button_positions()

        """
        Save the game setup
        """
        self._game_save.snap_game_setup(game_setup)

    def _setup_saved_game(self):
        """
        If this is a game in progress, prompt user to continue or overwrite
        If this is a complete game, prompt user for playback

        Load the existing game data to see if it is a finished or in-progress game
        """
        self._game_save.load()
        
        if self._game_save.is_game_complete():

            """
            Loaded game is already finished
            Prompt user to play back the completed game
            """
            load_game_history = self._ui.prompt_load_game_history()

            """
            If the user wishes to play back the loaded game, set up the theater
            Otherwise quit the game
            """
            if load_game_history:
                """
                Get the saved game data
                """
                loaded_game = self._game_save.get_game_save()

                """
                Parse the saved game data
                """
                game_setup, game_hands = loaded_game

                """
                Create a game theater and set the play protocol to playback
                """
                self._game_theater = GameTheater(game_setup, game_hands)
                self._game_play_code = Game.GAME_CODE_PLAYBACK_GAME
            else:
                self._ui.display_load_game_history_cancellation()
                self._game_play_code = Game.GAME_CODE_NO_PLAY
            
        else:
            """
            Game is not complete yet
            Prompt user to load and continue this game or continue creating a new game with risk 
            of overwriting this one
            """
            load_existing_game = self._ui.prompt_load_game()

            if load_existing_game:
                """
                Get the loaded game data
                """
                loaded_game = self._game_save.get_game_save()

                """
                Parse loaded game data as setup and player state values
                """
                game_setup, game_hands                                              = loaded_game
                round_number                                                        = GameData.INITIAL_ROUND_NUMBER
                player_state_final                                                  = None
                timestamp_final                                                     = None

                if len(game_hands) > 0:
                    """
                    If at least one hand was saved, load the player data and timestamp saved after the
                    last saved hand
                    Otherwise do not load any player or timestamp data

                    Also set the number of remaining players
                    """
                    last_hand                                                       = game_hands[-1]
                    round_number, _, _, _, _, player_state_final, timestamp_final   = last_hand
                    self._num_remaining_players                                     = len(player_state_final)
                else:
                    """
                    No hands played yet:
                        Set the number of remaining players to the initial number of players specified in setup
                    """
                    self._num_remaining_players = game_setup.starting_num_players
                
                """
                Package the load game values and set up the loaded game
                """
                game_setup.init_timestamp           = timestamp_final
                game_setup.round_number             = round_number
                game_setup.init_player_state        = player_state_final
                game_setup.handle_time_expired      = self._handle_time_expired

                self._game_data.setup_game_data(game_setup)
                self._game_play_code = Game.GAME_CODE_PLAY_LOAD_GAME

            else:
                """
                User decides to create and play a new game under the same name
                This means that if the user saves this new game at any point,
                the old game will be completely overwritten
                """
                self._game_save.clear_hand_history()
                self._ui.display_overwrite_warning()

    def _welcome(self):
        """
        Display the game title and hot key commands
        """
        self._ui.display_round_border()
        self._ui.display_title()
        self._ui.display_hot_key_commands()
        self._ui.display_round_border()

    def _attempt_save_game_history(self):
        """
        Prompt user for saving the game history
        """
        save_game_hist = self._ui.prompt_save_game_history()
        save_name = None

        if save_game_hist:

            """
            Attempt to save the game history, and if successful store the name of the file
            """
            save_success = self._game_save.save()

            if save_success:
                save_name = self._game_save.get_game_save_name()

        """
        Display confirmation message to user
        """
        self._ui.display_game_history_save_status(save_game_hist, save_name)

    def _manage_timer(self):
        """
        If the game is in load mode, set up the timer as if it was already running with the loaded timestamp
        """
        if self._game_play_code == Game.GAME_CODE_PLAY_LOAD_GAME:
            self._game_data.start_timer()

        """
        Get the current round number and timestamp
        """
        round_number    = self._game_data.get_round_number()
        remaining_time  = self._game_data.get_remaining_time()

        """
        Reset the timer and increase the blinds if the timer is off
        """
        if remaining_time == 0:

            """
            Raise the blinds if they are not at their maximum value
            """
            if not self._blinds_maxed_out:
                
                """
                Raise the blinds if this is not the first round
                """
                if round_number != GameData.INITIAL_ROUND_NUMBER:
                    self._game_data.raise_blinds()

                """
                Determine if the blinds are now at the maximum
                """
                if self._game_data.blinds_maxed_out():
                    self._blinds_maxed_out = True

                """
                Set the timer and display a confirmation message
                """
                self._game_data.start_timer()
                remaining_time  = self._game_data.get_remaining_time()
                big_blind       = self._game_data.get_big_blind_amt()
                self._ui.display_timer_set(round_number, big_blind, remaining_time)

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
            self._ui.display_current_timer_value(round_number, remaining_time)

        """
        Return Result (remaining time)
        """
        return remaining_time

    def _get_available_moves(self, player, preflop=False):
        """
        Local Variables
        """
        available_moves         = list()
        action_to_play          = 0
        max_action              = self._game_data.get_max_action()
        player_stack            = player.get_stack_size()
        player_action           = player.get_action()
        player_can_afford_raise = player_stack + player_action > max_action

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

    def _is_hand_over(self):
        """
        Determine if the hand is over
        Check if there is at least one side pot. In this case, the main pot must go to showdown
        Check if there are at least two players contending in the main pot. In this case, betting can still take place
        """
        num_pots            = self._game_data.get_num_pots()
        num_players_in_hand = self._game_data.get_num_players_in_hand()
        return ( num_pots < 2 ) and ( num_players_in_hand < 2 )

    def _has_multiple_available_betters(self):
        """
        Check if there is more than one available better in the current hand
        """
        return self._game_data.get_num_available_betters() > 1

    def _start_betting_round(self, preflop=False):
        """
        Local Variables
        """
        _, big_blind_idx    = self._game_data.get_blind_positions()
        current_player_idx  = None
        round_over          = False

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
        self._game_data.init_betting_round()

        """
        Round loop: keep cycling turns until the round is over
        """
        while not round_over:
            """
            Setup: Get a copy of the acting player for UI puproses
            """
            player = self._game_data.get_hand_player(player_idx=current_player_idx)
            num_players_in_hand_before_move = self._game_data.get_num_players_in_hand()

            """
            Play: Determine, prompt, and play a legal move
            """
            available_moves, action_to_play = self._get_available_moves(player, preflop=preflop)

            if len(available_moves) > 0:

                """
                Show the pot and community cards if postflop
                """
                if preflop is False:
                    self._ui.display_board(self._board, board_idx=self._board_idx)

                chosen_move, chosen_amount = self._ui.prompt_available_moves(player, available_moves, action_to_play)
                adjusted_amount = self._game_data.play_move(current_player_idx, chosen_move, chosen_amount)
                self._ui.display_move_made(player, chosen_move, adjusted_amount)

                """
                Store the action for the save snapshot
                """
                self._hand_actions.append((player.ID, chosen_move, adjusted_amount))

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

            """
            Cleanup: Find the next player to act and determine if the round is over
            """
            current_player_idx  = self._game_data.get_next_player_pos(current_player_idx)
            round_over          = self._game_data.is_round_over()

    def _open_for_betting(self, preflop=False):
        """
        Display the current pot
        """
        self._ui.display_pot(self._game_data.get_pot())

        """
        Start a betting round if more than one player is able to bet
        """
        if preflop or self._has_multiple_available_betters():
            self._start_betting_round(preflop=preflop)
        else:

            if preflop is False:
                self._ui.display_board(self._board, board_idx=self._board_idx)

            self._ui.display_no_bet_from_all_in()

        """
        Move all player action to the pot and display it
        """
        self._game_data.move_action_to_pot()

        """
        Determine if the hand has ended prematurely and return it
        """
        return self._is_hand_over()
