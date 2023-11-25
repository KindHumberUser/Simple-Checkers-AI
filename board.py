import pygame
from tile import Tile
from pawn import Pawn

class Board:
    def __init__(self, tile_width, tile_height, board_size):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.board_size = board_size
        self.selected_piece = None
        self.is_jump = False
        self.turn = "black"

        self.config = [
            ['', 'bp', '', 'bp', '', 'bp', '', 'bp'],
            ['bp', '', 'bp', '', 'bp', '', 'bp', ''],
            ['', 'bp', '', 'bp', '', 'bp', '', 'bp'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['rp', '', 'rp', '', 'rp', '', 'rp', ''],
            ['', 'rp', '', 'rp', '', 'rp', '', 'rp'],
            ['rp', '', 'rp', '', 'rp', '', 'rp', '']
        ]

        self.tile_list = self.generate_tiles()
        self.setup()

    def generate_tiles(self):
        output = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                output.append(
                    Tile(x,  y, self.tile_width, self.tile_height)
                )
        return output
    
    def get_tile_from_pos(self, pos):
        for tile in self.tile_list:
            if (tile.x, tile.y) == (pos[0], pos[1]):
                return tile
            
    def setup(self):
        for y_ind, row in enumerate(self.config):
            for x_ind, x in enumerate(row):
                tile = self.get_tile_from_pos((x_ind, y_ind))
                if x != '':
                    color = 'red' if x[0] == 'r' else 'black'
                    tile.occupying_piece = Pawn(x_ind, y_ind, color, self)

    def handle_click(self, pos):
        x, y = pos[0], pos[-1]

        #Get the tile position from pixel coords
        if x >= self.board_size or y >= self.board_size:
            x = x // self.tile_width
            y = y // self.tile_height

        clicked_tile = self.get_tile_from_pos((x, y))

        #If piece is not selected, check if a piece exists on tile and select it
        if self.selected_piece is None:
            if clicked_tile.occupying_piece is not None:
                #Check the clicked tile color belongs to player with current turn
                if clicked_tile.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_tile.occupying_piece
        #Checks if selected piece can move to current tile
        elif self.selected_piece.move(clicked_tile):
            #If not a jump then ends turn
            if not self.is_jump:
                self.turn = 'red' if self.turn == 'black' else 'black'
            else:
                #Checks if additional followup jumps can be made before ending turn
                if len(clicked_tile.occupying_piece.valid_jumps()) == 0:
                    self.turn = 'red' if self.turn == 'black' else 'black'
        #Selects piece if it belongs to color of current player
        elif clicked_tile.occupying_piece is not None:
            if clicked_tile.occupying_piece.color == self.turn:
                self.selected_piece = clicked_tile.occupying_piece

    def draw(self, display):
        #Highlights selected piece
        if self.selected_piece is not None:
            self.get_tile_from_pos(self.selected_piece.pos).highlight = True
            #Highlights moves or jumps
            if not self.is_jump:
                for tile in self.selected_piece.valid_moves():
                    tile.highlight = True
            else:
                for tile in self.selected_piece.valid_jumps():
                    tile[0].highlight = True

        #Draws every tile to display
        for tile in self.tile_list:
            tile.draw(display)