from tkinter import *
from itertools import cycle
from player import Player, Move, DEFAULT_PLAYERS, BOARD_SIZE

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
                button.config(bg="green", fg="white")


