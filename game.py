from board import Board
from tile import Tile
from piece import Piece

class Game:
    def __init__(self):
        self.winner = None

    def check_piece(self, board):
        #Number of pieces
        red = 0
        black = 0

        #Checks every tile to count every piece color
        for y in range(board.board_size):
            for x in range(board.board_size):
                tile = board.get_tile_from_pos((x, y))
                if tile.occupying_piece != None:
                    if tile.occupying_piece.color == "red":
                        red += 1
                    else:
                        black += 1
        return red, black
    
    def is_game_over(self, board):
        #Game is over if one side loses all pieces
        red_piece, black_piece = self.check_piece(board)
        if red_piece == 0 or black_piece == 0:
            self.winner = "red" if red_piece > black_piece else "black"
            return True
        else:
            return False
        
    def check_jump(self, board):
        #Forces a jump if jump is avalaible. Traditional rules of Checkers
        piece = None
        for tile in board.tile_list:
            if tile.occupying_piece != None:
                piece = tile.occupying_piece
                if len(piece.valid_jumps()) != 0 and board.turn == piece.color:
                    board.is_jump = True
                    break
                else:
                    board.is_jump = False
        # if board.is_jump:
        #     board.selected_piece = piece
        #     board.handle_click(piece.pos)
        return board.is_jump
    
    def message(self):
        print(f"{self.winner} Wins!!")

    