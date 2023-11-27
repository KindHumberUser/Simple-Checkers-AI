import pygame
import sys
from board import Board
from game import Game
from button import Button

WIDTH, HEIGHT = 640, 640
FPS = pygame.time.Clock()


def draw(screen, board):
    board.draw(screen)
    pygame.display.update()


def title_screen(screen):
    start_button = Button(220, 270, 200, 50, "images/start.png", second_screen, screen)
    quit_button = Button(220, 420, 200, 50, "images/quit.png", sys.exit)

    buttons = [start_button, quit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.action:
                                button.perform_action()

        for button in buttons:
            button.draw(screen)

        pygame.display.update()
        FPS.tick(60)


def second_screen(screen):
    easy_difficulty = Button(220, 270, 200, 50, "images/easy.png", set_diff, (0, screen))
    medium_difficulty = Button(220, 420, 200, 50, "images/medium.png", set_diff, (1, screen))
    hard_difficulty = Button(220, 420, 200, 50, "images/hard.png", set_diff, (2, screen))

    buttons = [easy_difficulty, medium_difficulty, hard_difficulty]

    for button in buttons:
        button.change_background("images/choose_difficulty.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.action:
                                button.perform_action()

        for button in buttons:
            button.draw(screen)

        pygame.display.update()
        FPS.tick(60)


def set_diff(diff, screen):
    third_screen(screen)

    return None


def third_screen(screen):
    red_side = Button(220, 270, 200, 50, "images/red.png", game_loop, screen)
    black_side = Button(220, 420, 200, 50, "images/black.png", game_loop, screen)

    buttons = [red_side, black_side]

    for button in buttons:
        button.change_background("images/choose_side.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.action:
                                button.perform_action()

        for button in buttons:
            button.draw(screen)

        pygame.display.update()
        FPS.tick(60)


def game_loop(screen):
    board_size = 8
    tile_width, tile_height = WIDTH // board_size, HEIGHT // board_size
    board = Board(tile_width, tile_height, board_size)

    game = Game()
    while True:
        game.check_jump(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game.is_game_over(board):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        board.handle_click(event.pos)

            else:
                end_screen(screen, game.winner())

            draw(screen, board)
            FPS.tick(60)


def end_screen(screen, winner):
    retry_button = Button(220, 270, 200, 50, "images/retry.png", title_screen, screen)
    quit_button = Button(220, 420, 200, 50, "images/quit.png", sys.exit)

    buttons = [retry_button, quit_button]

    if winner == "red":
        back_img = "images/red_wins.png"
    else:
        back_img = "images/black_wins.png"

    for button in buttons:
        button.change_background(back_img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button.is_clicked(event.pos):
                            if button.action:
                                button.perform_action()

        for button in buttons:
            button.draw(screen)

        pygame.display.update()
        FPS.tick(60)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Checkers Game")

    title_screen(screen)


if __name__ == "__main__":
    main()
