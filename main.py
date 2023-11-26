import pygame
from board import Board
from game import Game

def draw(screen, board):
        board.draw(screen)
        pygame.display.update()

def main():
    pygame.init()

    #Setting game parameters
    width, height = 640, 640
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simple Checkers Game")

    board_size = 8
    tile_width, tile_height = width // board_size, height // board_size
    board = Board(tile_width, tile_height, board_size)

    game = Game()
    FPS = pygame.time.Clock()
    counter = 0
    running = True
    while(running):
        game.check_jump(board)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game.is_game_over(board):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        board.handle_click(event.pos)
                        
            else:
                game.message()
                running = False

            draw(screen, board)
            FPS.tick(60)
            counter += 1

if __name__ == "__main__":
    main()