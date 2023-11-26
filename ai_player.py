import random

class AIPlayer:
    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color

    def select_move(self, board):
        if self.difficulty == 'beginner':
            return self.select_move_beginner(board)
        elif self.difficulty == 'intermediate':
            return self.select_move_intermediate(board)
        elif self.difficulty == 'advanced':
            return self.select_move_advanced(board)

    def select_move_beginner(self, board):
        # Select a random valid move
        moves = self.get_all_valid_moves(board)
        return random.choice(moves) if moves else None

    def select_move_intermediate(self, board):
        # Intermediate logic
        pass

    def select_move_advanced(self, board):
        # Advanced logic
        pass

    def get_all_valid_moves(self, board):
        valid_moves = []
        for tile in board.tile_list:
            piece = tile.occupying_piece
            if piece and piece.color == self.color:
                for move in piece.valid_moves():
                    valid_moves.append((piece, move))
                for jump in piece.valid_jumps():
                    valid_moves.append((piece, jump[0]))
        return valid_moves