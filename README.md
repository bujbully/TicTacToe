The game use OOP to replicate the mechanics of the two player tic tac toe game in the tkinter module
A class exists for the players which is a named tuple with their identifying properties
A named tuple class for the moves with the identifier in the form of the x/o label or a blank space if not played and the position of the particular move on the board with a row and column integer value
A Tk class for the board. the board class sets the board and the basic grid display. Although it's a 3x3 grid the game size can be altered through this class to create a gomoku like experience
A seperate class for the game that controls the game mechanics and toggles the moves between players
