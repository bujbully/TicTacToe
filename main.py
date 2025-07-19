from board import Board
from game import Game
from player import Player, Move

if __name__ == "__main__":
    game = Game()
    board = Board(game)
    board.mainloop()