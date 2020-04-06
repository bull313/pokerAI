def get_input(input_msg): # Wrapper for input function for Python version swapping
    return input(input_msg)

class GameUI:
    INPUT_STARTING_CHIP_COUNT_STR = "Enter the starting chip count: "
    INPUT_STARTING_CHIP_COUNT_EVEN_ERROR = "Starting chip count must be an even number"
    INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR = "Starting chip count must be a valid integer"

    INPUT_STARTING_BIG_BLIND_STR = "Enter the starting big blind amount: "
    INPUT_STARTING_BIG_BLIND_EVEN_ERROR = "Starting big blind must be an even number"
    INPUT_STARTING_BIG_BLIND_INTEGER_ERROR = "Starting chip count must be a valid integer"
    INPUT_STARTING_BIG_BLIND_SIZE_ERROR = "Starting big blind must be smaller than the starting chip count"

    CHIP_COUNT_STR = "%s has %d chips\n"
    IS_DEALER_STR = "%s is the dealer\n"
    IS_NOT_DEALER_STR = "%s is not the dealer\n"
    BETTING_ROUND_PLACEHOLDER_STR = "A betting round would take place here"
    PRESS_ANY_KEY_PROMPT = "Press any key to continue..."
    PLAYER_HAND_CARDS_STR = "%s has %s\n"
    HAND_WINNER_STR = "%s wins with %s!"
    PLAYER_HAND_RANK_STR = "%s had %s"

    GAME_WINNER_STR = "%s wins!"
    GAME_OVER_STR = "GAME OVER"

    BORDER_LENGTH = 10
    BORDER_CHAR = '='

    GAME_BOARD_NAMES = [ "Flop", "Turn", "River" ]

    def get_starting_chip_count(self):
        starting_chip_count = 0
        valid_starting_chip_count = False

        while not valid_starting_chip_count:
            starting_chip_count = get_input(GameUI.INPUT_STARTING_CHIP_COUNT_STR)

            try:
                starting_chip_count = int(starting_chip_count)

                if starting_chip_count % 2 != 0:
                    print(GameUI.INPUT_STARTING_CHIP_COUNT_EVEN_ERROR)
                else:
                    valid_starting_chip_count = True
                
            except:
                print(GameUI.INPUT_STARTING_CHIP_COUNT_INTEGER_ERROR)

        return starting_chip_count

    def get_starting_big_blind(self, starting_chip_count):
        starting_big_blind = 0
        valid_starting_big_blind = False

        while not valid_starting_big_blind:
            starting_big_blind = get_input(GameUI.INPUT_STARTING_BIG_BLIND_STR)

            try:
                starting_big_blind = int(starting_big_blind)

                if starting_big_blind % 2 != 0:
                    print(GameUI.INPUT_STARTING_BIG_BLIND_EVEN_ERROR)
                elif starting_big_blind > starting_chip_count:
                    print(GameUI.INPUT_STARTING_BIG_BLIND_SIZE_ERROR)
                else:
                    valid_starting_big_blind = True

            except:
                print(GameUI.INPUT_STARTING_BIG_BLIND_INTEGER_ERROR)

        return starting_big_blind

    def display_round_border(self):
        border_str = ""
        for _ in range(GameUI.BORDER_LENGTH): border_str += GameUI.BORDER_CHAR
        border_str += "\n"

        print(border_str)

    def display_player_data(self, players):
        player_str = ""
        for player in players:
            player_str += GameUI.CHIP_COUNT_STR % (player, player.get_chip_count())

            if player.is_dealer():
                player_str += GameUI.IS_DEALER_STR % player
            else:
                player_str += GameUI.IS_NOT_DEALER_STR % player
            
            cards_str = ""
            hole_cards = player.get_hole_cards()
            hole_cards.sort(reverse = True)
            for card in hole_cards:
                cards_str += "%s " % card
            
            player_str += GameUI.PLAYER_HAND_CARDS_STR % (player, cards_str)

        print(player_str)

    def start_betting_round(self):
        print(GameUI.BETTING_ROUND_PLACEHOLDER_STR)
        get_input(GameUI.PRESS_ANY_KEY_PROMPT)

    def show_board(self, board_idx, board_cards):
        print("%s:" % GameUI.GAME_BOARD_NAMES[ board_idx ])
        board_str = "\t"
        for card in board_cards:
            board_str += "%s " % card
        board_str += "\n"
        print(board_str)

    def show_results(self, player_hand_pairs):
        first = True
        for player_hand_pair in player_hand_pairs:
            if first:
                print(GameUI.HAND_WINNER_STR % player_hand_pair)
                first = False
            else:
                print(GameUI.PLAYER_HAND_RANK_STR % player_hand_pair)

    def display_winner(self, winner):
        print(GameUI.GAME_WINNER_STR % winner)
        print(GameUI.GAME_OVER_STR)
