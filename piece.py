import pygame

class piece:

    def __init__(self, x, y, color, board):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.board = board
        self.color = color