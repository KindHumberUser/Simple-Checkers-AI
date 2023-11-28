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
        print("Running beginner")
        moves = self.get_all_valid_moves(board)
        return random.choice(moves) if moves else None

    def select_move_intermediate(self, board):
        print("Running intermediate")
        moves = self.get_all_valid_moves(board)

        # Prioritize capturing moves
        capturing_moves = [move for move in moves if self.is_capturing_move(move)]
        if capturing_moves:
            return random.choice(capturing_moves)

        # Otherwise, choose a random move
        return random.choice(moves)

    def is_capturing_move(self, move):
        piece, destination = move
        return len(piece.valid_jumps()) > 0


    def select_move_advanced(self, board):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3  # Depth can be adjusted for difficulty

        for move in self.get_all_valid_moves(board):
            score = self.minimax(move, board, depth, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, move, board, depth, is_maximizing, alpha, beta):
        print(f"Running minimax: Depth {depth}, Is Maximizing: {is_maximizing}, Alpha: {alpha}, Beta: {beta}")
        if depth == 0:
            return self.evaluate_board(board)

        if is_maximizing:
            max_eval = float('-inf')
            for child_move in self.get_all_valid_moves(board):
                evaluation = self.minimax(child_move, board, depth-1, False, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child_move in self.get_all_valid_moves(board):
                evaluation = self.minimax(child_move, board, depth-1, True, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        score = 0
        for tile in board.tile_list:
            piece = tile.occupying_piece
            if piece:
                # Assign scores to pieces: Pawn = 1, King = 1.5
                piece_value = 1.5 if piece.notation == 'k' else 1
                if piece.color == self.color:
                    score += piece_value
                else:
                    score -= piece_value

                # Maybe we can add more logic here for evaluating position of the pieces as well

        return score

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