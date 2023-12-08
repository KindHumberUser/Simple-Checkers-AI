import random

class AIPlayer:
    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color
        self.numMoves = 0

    def select_move(self, board):
        self.numMoves += 1
        if self.difficulty == 'beginner':
            return self.select_move_beginner(board)
        elif self.difficulty == 'intermediate':
            return self.select_move_intermediate(board)
        elif self.difficulty == 'advanced':
            move = self.select_move_advanced(board)
            if move==None:
                #Just return a random move
                return self.select_move_beginner(board)
            return move

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
        ops = []
        mine = []
        #Get a list of opponent and self pieces
        for tile in board.tile_list:
            piece = tile.occupying_piece
            if piece:
                if piece.color!=self.color:
                    ops.append(piece)
                else:
                    mine.append(piece)

        #Evaluate pieces and positions
        for piece in ops:
            piece_value = 20 if piece.notation == 'k' else 10
            score -= piece_value

        for piece in mine:
            piece_value = 20 if piece.notation == 'k' else 10
            score += piece_value

            if piece.notation == 'p':
                if self.color=='red':
                    score += 1 * (7 - piece.y)  # Move pawns closer to the top for red
                    if piece.y==7 and self.numMoves>10:
                        score -= 10
                else:
                    score += 1 * piece.y # Move pawns closer to the bottom for black
                    if piece.y==0 and self.numMoves>10:
                        score -= 10
                
                # Bonus for pawns controlling the center
                score += 1 * (3 - abs(3 - tile.x))
            elif piece.notation == 'k':
                # Move towards the closest opponent piece
                closest_opponent_distance = float('inf')
                for opponent_piece in ops:
                    distance_to_opponent = self.distance(piece, opponent_piece)
                    closest_opponent_distance = min(closest_opponent_distance, distance_to_opponent)
                score -= closest_opponent_distance

        for opponent_piece in ops:
            for self_piece in mine:
                if self.is_neighbor(self_piece, opponent_piece):
                    if self_piece.notation == 'p':
                        score -= 20
                    else:
                        score -= 50

        # Evaluate pawn structure
        for x in range(0, 7):
            for y in range(0, 7):
                tile = board.get_tile_from_pos((x,y))
                if tile.occupying_piece and tile.occupying_piece.notation == 'p' and tile.occupying_piece.color == self.color:
                    # Bonus for connected pawns
                    connected_pawns = self.count_connected_pawns(board, x, y, self.color)
                    score += 0.1 * connected_pawns

        print(score)
        return score
    
    def distance(self, piece1, piece2):
        return abs(piece1.x - piece2.x) + abs(piece1.y - piece2.y)
    
    def is_neighbor(self, piece1, piece2):
        positions = []
        positions.append((piece2.x + 1, piece2.y + 1))
        positions.append((piece2.x + 1, piece2.y - 1))
        positions.append((piece2.x - 1, piece2.y + 1))
        positions.append((piece2.x - 1, piece2.y - 1))
        return piece1.pos in positions


    def count_connected_pawns(self, board, x, y, color):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 1 <= nx <= 6 and 1 <= ny <= 6:
                    neighbor_tile = board.get_tile_from_pos((nx,ny))
                    if neighbor_tile.occupying_piece and neighbor_tile.occupying_piece.notation == 'p' and neighbor_tile.occupying_piece.color == color:
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