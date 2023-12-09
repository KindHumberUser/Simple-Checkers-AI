import pygame
import sys
import time
from board import Board
from game import Game
from button import Button
from ai_player import AIPlayer

WIDTH, HEIGHT = 640, 640
FPS = pygame.time.Clock()


def draw(screen, board):
    board.draw(screen)
    pygame.display.update()


def game_loop(screen, difficulty, ai_color, user_color):
    print("Entering game_loop")
    board_size = 8
    tile_width, tile_height = WIDTH // board_size, HEIGHT // board_size
    board = Board(tile_width, tile_height, board_size)
    opp = AIPlayer(difficulty, ai_color)
    game = Game()
    while True:
        game.check_jump(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False

            if not game.is_game_over(board):
                if board.get_turn() == user_color:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            board.handle_click(event.pos)
                else:
                    print("AI's turn")
                    ai_piece, ai_tile = opp.select_move(board)
                    print(f"AI selected piece {ai_piece.pos} to move to {ai_tile.pos}")
                    board.handle_move(ai_piece, ai_tile)
                    print("AI move completed")
            else:
                game.message()
                pygame.quit()
                main()
                running = False

            draw(screen, board)
            FPS.tick(60)

def test_loop(screen, ai_color, user_color):
    print("Entering game_loop")
    board_size = 8
    tile_width, tile_height = WIDTH // board_size, HEIGHT // board_size
    board = Board(tile_width, tile_height, board_size)
    opp = AIPlayer('advanced', ai_color)
    user = AIPlayer('intermediate', user_color)
    game = Game()
    numMoves = 0
    while True:
        for event in pygame.event.get():
            game.check_jump(board)
            if event.type == pygame.QUIT:
                sys.exit()
                running = False

            if not game.is_game_over(board):
                if board.get_turn() == user_color:
                    print("Intermediate AI's turn")
                    user_piece, user_tile = user.select_move(board)
                    print(f"AI selected piece {user_piece.pos} to move to {user_tile.pos}")
                    board.handle_move(user_piece, user_tile)
                    print("Intermediate AI move completed")
                else:
                    print("Advanced AI's turn")
                    ai_piece, ai_tile = opp.select_move(board)
                    print(f"AI selected piece {ai_piece.pos} to move to {ai_tile.pos}")
                    board.handle_move(ai_piece, ai_tile)
                    print("AI move completed")
                    numMoves += 1
            else:
                game.message()
                print(f"Number of Moves required to win: {numMoves}")
                pygame.quit()
                main()
                running = False

            #time.sleep(2)
            draw(screen, board)
            FPS.tick(60)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Checkers Game")

    test = input("To enter testing mode, enter \"T\". \n")

    if test == "T":
        ai_color = 'red'
        user_color = 'black'
        test_loop(screen, ai_color, user_color)

    difficulty = input("What difficulty do you want to play on? Choose from beginner, intermediate and advanced. \n")
    user_color = input("What color do you want to start with? Choose from red or black. \n")

    ai_color = 'red' if user_color=="black" else 'black'

    # title_screen(screen)
    game_loop(screen, difficulty, ai_color, user_color)

if __name__ == "__main__":
    main()
