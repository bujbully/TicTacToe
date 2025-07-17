from tkinter import *
from itertools import cycle
from typing import NamedTuple

class Board(Tk):
    def __init__(self, game):
        super().__init__()
        self.display = None
        self.title("TicTacToe")
        self.cells={}
        self.game = game
        self.create_board()
        self.create_grid()


    def create_board(self):

        display_frame =Frame(master=self)
        display_frame.pack(fill=X)
        self.display=Label(
            master=display_frame,
            text="Ready?",
            font= ("helvetica", 24, "bold")
        )
        self.display.pack()
        
    def create_grid(self):
        grid= Frame(master=self)
        grid.pack()
        for row in range(self.game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=50)
            for col in range(self.game.board_size):
                box= Button(
                    master=grid,
                    text= "",
                    font= ("arial", 50, "bold"),
                    fg= "black",
                    highlightcolor="lightblue",
                    width=3,
                    height=2,
                    bg="#FDFDFD"
                )
                self.cells[box]=(row, col)
                box.bind("<ButtonPress-1>", self.play)
                box.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def play(self, event):
        clicked= event.widget
        row, col = self.cells[clicked]
        move= Move(row, col, self.game.current_player.label)
        if self.game.valid_move(move):
            self.update_button(clicked)
            self.game.process_move(move)
            if self.game.game_tie():
                self.update_display(msg="GAME TIE!", color="red")
            elif self.game.game_has_winner():
                self.highlight_cells()
                self.update_display(msg=f"Player {self.game.current_player.label} won!", color=self.game.current_player.color)
            else:
                self.game.toggle_players()
                self.update_display(msg=f"{self.game.current_player.label}'s turn")

    def update_button(self, clicked):
        clicked.config(
            text=self.game.current_player.label,
            fg=self.game.current_player.color
        )

    def update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def highlight_cells(self):
        for button, coordinates in self.cells.items():
            if coordinates in self.game.winner_move:
                button.config(highlightbackground="red")


class Player(NamedTuple):
    label : str
    color : str

class Move(NamedTuple):
    row : int
    col : int
    label : str

BOARD_SIZE=3
DEFAULT_PLAYERS=(Player(label="X", color="green"), Player(label="O", color="blue"))

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
        return rows + columns + [diagonal_one, diagonal_two]

    def valid_move(self, move):
        row, col = move.row, move.col
        not_played = self.current_moves[row][col].label==""
        no_winner = not self.has_winner
        return no_winner and not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self.current_moves[row][col] = move
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

game=Game()
board= Board(game=game)
board.mainloop()