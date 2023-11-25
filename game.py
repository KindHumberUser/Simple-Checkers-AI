from board import board

class game:
    def __init__(self):
        self.winner = None

    def check_piece(self, board):
        #Number of pieces
        red = 0
        black = 0

        for x,y in range(board):

    