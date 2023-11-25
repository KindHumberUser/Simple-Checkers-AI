import pygame
from piece import Piece

class Pawn(Piece):
    def __init__(self, x, y, color, board):
        super().__init__(x, y, color, board)
        self.notation = 'p'

        img_path = f'images/{color}-pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width, board.tile_height))
    
    def possible_moves(self):
        # (x, y) move for left and right
        if self.color == "red":
            possible_moves = ((-1, -1), (+1, -1)) 
        else:
            possible_moves = ((-1, +1), (+1, +1))
        return possible_moves
    
    def valid_moves(self):
        valid_moves = []
        moves = self.possible_moves()
        for move in moves:
            tile_pos = (self.x + move[0], self.y + move[-1])
            if self.is_boundary(tile_pos):
                pass
            else:
                tile = self.board.get_tile_from_pos(tile_pos)
                if tile.occupying_piece == None:
                    valid_moves.append(tile)
        return valid_moves
    
    def valid_jumps(self):
        valid_jumps = []
        moves = self.possible_moves()
        for move in moves:
            tile_pos = (self.x + move[0], self.y + move[-1])
            if self.is_boundary(tile_pos):
                pass
            else:
                tile = self.board.get_tile_from_pos(tile_pos)
                if self.board.turn == self.color:
                    if tile.occupying_piece != None and tile.occupying_piece.color != self.color:
                        next_pos = (tile_pos[0] + move[0], tile_pos[-1] + move[-1])
                        next_tile = self.board.get_tile_from_pos(next_pos)	
                        if self.is_boundary(next_pos):
                            pass
                        else:
                            if next_tile.occupying_piece == None:
                                valid_jumps.append((next_tile, tile))
        return valid_jumps
    
