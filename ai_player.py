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
        depth = 4  # Depth can be adjusted for difficulty

        valid_moves = self.get_all_valid_moves(board)
        

        for move in valid_moves:
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

        # Evaluate piece values and positions
        for tile in board.tile_list:
            piece = tile.occupying_piece
            if piece:
                piece_value = 1.5 if piece.notation == 'k' else 1
                if piece.color == self.color:
                    score += piece_value
                else:
                    score -= piece_value

                # Add positional evaluation
                if piece.color == self.color:
                    if piece.notation == 'p':
                        # Bonus for pawns controlling the center
                        score += 0.1 * (3 - abs(3 - tile.x))
                    # elif piece.notation == 'k':
                    #     # Penalty for the king being exposed
                    #     if self.is_king_in_check(self.color, board):
                    #         score -= 0.5
                else:
                    if piece.notation == 'p':
                        # Bonus for opponent's pawns controlling the center
                        score -= 0.1 * (3 - abs(3 - tile.x))
                    # elif piece.notation == 'k':
                    #     # Penalty for the opponent's king being exposed
                    #     if board.is_king_in_check(self.get_opponent_color()):
                    #         score += 0.5

        # Evaluate pawn structure
        for x in range(1, 7):
            for y in range(1, 7):
                tile = board.get_tile_from_pos((x,y))
                if tile.occupying_piece and tile.occupying_piece.notation == 'p':
                    # Bonus for connected pawns
                    connected_pawns = self.count_connected_pawns(board, x, y)
                    score += 0.2 * connected_pawns

        return score
    
    # def is_king_in_check(self, color, board):
    #     king_position = None

    #     # Find the position of the king of the specified color
    #     for tile in board.tile_list:
    #         piece = tile.occupying_piece
    #         if piece and piece.notation == 'k' and piece.color == color:
    #             king_position = (tile.x, tile.y)
    #             break

    #     if king_position is None:
    #         # King not found, something is wrong with the board state
    #         raise ValueError("King not found on the board")

    #     # Check if any opponent's piece threatens the king
    #     for tile in board.tile_list:
    #         piece = tile.occupying_piece
    #         if piece and piece.color != color:
    #             valid_moves = self.get_valid_moves(tile.x, tile.y, board)
    #             if king_position in valid_moves:
    #                 return True

    #     return False


    def count_connected_pawns(self, board, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 1 <= nx <= 6 and 1 <= ny <= 6:
                    neighbor_tile = board.get_tile_from_pos((nx,ny))
                    if neighbor_tile.occupying_piece and neighbor_tile.occupying_piece.notation == 'p':
                        count += 1
        return count

    def get_all_valid_moves(self, board):
        valid_moves = []
        if (board.is_jump):
            for tile in board.tile_list:
                if tile.occupying_piece != None:
                    piece = tile.occupying_piece
                    if piece.color == self.color:
                        for jump in piece.valid_jumps():
                            valid_moves.append((piece, jump[0]))
        else:
            for tile in board.tile_list:
                piece = tile.occupying_piece
                if piece and piece.color == self.color:
                    for move in piece.valid_moves():
                        valid_moves.append((piece, move))
                    for jump in piece.valid_jumps():
                        valid_moves.append((piece, jump[0]))
        
        return valid_moves