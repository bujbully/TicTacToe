from itertools import cycle
from typing import NamedTuple



class Player(NamedTuple):
    label : str
    color : str

class Move(NamedTuple):
    row : int
    col : int
    label : str

BOARD_SIZE=3
DEFAULT_PLAYERS=(Player(label="X", color="red"), Player(label="O", color="blue"))

class Game:
    def __init__(self, player=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.players=cycle(player)
        self.board_size= board_size
        self.current_player=next(self.players)
        self.winner_move= []
        self.current_moves= []
        self.winning_combos= []
        self.has_winner= False
        self.setup_board()

    def setup_board(self):
        label=""
        self.current_moves=[
            [Move(row, col, label) for col in range(self.board_size)] for row in range(self.board_size)
        ]
        self.winning_combos = self.get_winning_combos()

    def get_winning_combos(self):
        rows = [[(move.row, move.col) for move in row] for row in self.current_moves]
        columns = [list(col) for col in zip(*rows)]
        diagonal_one = [row[a]for a, row in enumerate(rows)]
        diagonal_two = [col[b] for  b, col in enumerate(reversed(columns))]
        return rows + columns + diagonal_one + diagonal_two

    def valid_move(self, move):
        row, col = move.row, move.col
        not_played = self.current_moves[row][col].label==""
        no_winner = not self.has_winner
        return no_winner and not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self.current_moves[row][col]=move
        for combo in self.winning_combos:
            results = set(self.current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self.has_winner = True
                self.winner_move = combo
                break

    def game_has_winner(self):
        return self.has_winner

    def game_tie(self):
        no_winner = not self.has_winner
        played =  (move.label for row in self.current_moves for move in row)
        return no_winner and all(played)

    def toggle_players(self):
        self.current_player = next(self.players)


