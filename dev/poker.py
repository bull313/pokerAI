"""
Driver file
"""

"""
Imports
"""
from game import Game

"""
Constants
"""
EXCEPTION_MSG = "Poker has crashed..."

"""
Driver function
"""
def main():
    try:
        game = Game()
        game.setup()
        game.play_game()
        
    except Exception as e:
        print(EXCEPTION_MSG)
        print(str(e))

"""
Run driver function
"""
if __name__ == "__main__":
    main()
