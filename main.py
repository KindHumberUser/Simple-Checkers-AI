import pygame
import sys
from board import Board
from game import Game
from button import Button
from ai_player import AIPlayer

WIDTH, HEIGHT = 640, 640
FPS = pygame.time.Clock()


def draw(screen, board):
    board.draw(screen)
    pygame.display.update()


# def title_screen(screen):
#     start_button = Button(220, 270, 200, 50, "images/start.png", second_screen, screen)
#     quit_button = Button(220, 420, 200, 50, "images/quit.png", sys.exit)

#     buttons = [start_button, quit_button]

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button
#                     for button in buttons:
#                         if button.is_clicked(event.pos):
#                             if button.action:
#                                 button.perform_action()

#         for button in buttons:
#             button.draw(screen)

#         pygame.display.update()
#         FPS.tick(60)


# def second_screen(screen):
#     easy_difficulty = Button(220, 270, 200, 50, "images/easy.png", set_diff, (0, screen))
#     medium_difficulty = Button(220, 420, 200, 50, "images/medium.png", set_diff, (1, screen))
#     hard_difficulty = Button(220, 420, 200, 50, "images/hard.png", set_diff, (2, screen))

#     buttons = [easy_difficulty, medium_difficulty, hard_difficulty]

#     for button in buttons:
#         button.change_background("images/choose_difficulty.png")

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button
#                     for button in buttons:
#                         if button.is_clicked(event.pos):
#                             if button.action:
#                                 button.perform_action()

#         for button in buttons:
#             button.draw(screen)

#         pygame.display.update()
#         FPS.tick(60)


# def set_diff(diff, screen):
#     if diff == 0:
#         AI_DIFFICULTY = "beginner"
#     elif diff == 1:
#         AI_DIFFICULTY = "intermediate"
#     else:
#         AI_DIFFICULTY = "advanced"

#     third_screen(screen)

#     return None


# def third_screen(screen):
#     red_side = Button(220, 270, 200, 50, "images/red.png", set_turn, (0, screen))
#     black_side = Button(220, 420, 200, 50, "images/black.png", set_turn, (1, screen))

#     buttons = [red_side, black_side]

#     for button in buttons:
#         button.change_background("images/choose_side.png")

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button
#                     for button in buttons:
#                         if button.is_clicked(event.pos):
#                             if button.action:
#                                 button.perform_action()

#         for button in buttons:
#             button.draw(screen)

#         pygame.display.update()
#         FPS.tick(60)


# def set_turn(col, screen):
#     print(f"Entering set_turn with col={col}")
#     if col == 0:
#         AI_COLOR = "black"
#         USER_COLOR = "red"
#     else:
#         AI_COLOR = "red"
#         USER_COLOR = "black"

#     game_loop(screen)


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
                    print(f"AI selected piece {ai_piece} to move to {ai_tile}")
                    board.handle_move(ai_piece, ai_tile)
                    print("AI move completed")
            else:
                game.message()
                restart()
                running = False

            draw(screen, board)
            FPS.tick(60)

def restart(screen):
    difficulty = input("What difficulty do you want to play on? Choose from beginner, intermediate and advanced. \n")
    user_color = input("What color do you want to start with? Choose from red or black. \n")

    ai_color = 'red' if user_color=="black" else 'black'

    game_loop(screen, difficulty, ai_color, user_color)


# def end_screen(screen, winner):
#     print(f"Entering end_screen with winner={winner}")
#     retry_button = Button(220, 270, 200, 50, "images/retry.png", title_screen, screen)
#     quit_button = Button(220, 420, 200, 50, "images/quit.png", sys.exit)

#     buttons = [retry_button, quit_button]

#     if winner == USER_COLOR:
#         back_img = "images/game_win.png"
#     else:
#         back_img = "images/game_lose.png"

#     for button in buttons:
#         button.change_background(back_img)

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button
#                     for button in buttons:
#                         if button.is_clicked(event.pos):
#                             if button.action:
#                                 button.perform_action()

#         for button in buttons:
#             button.draw(screen)

#         pygame.display.update()
#         FPS.tick(60)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Checkers Game")

    difficulty = input("What difficulty do you want to play on? Choose from beginner, intermediate and advanced. \n")
    user_color = input("What color do you want to start with? Choose from red or black. \n")

    ai_color = 'red' if user_color=="black" else 'black'

    # title_screen(screen)
    game_loop(screen, difficulty, ai_color, user_color)

if __name__ == "__main__":
    main()
