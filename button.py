import pygame

WIDTH, HEIGHT = 640, 640

class Button:
    def __init__(self, x, y, width, height, img, action=None, params=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.img = img
        self.params = params
        self.background = "images/title.png"

    def draw(self, screen):
        back_img = pygame.image.load(self.background)
        back_img = pygame.transform.scale(back_img, (WIDTH, HEIGHT))
        screen.blit(back_img, (0, 0))

        pygame.draw.rect(screen, (0, 0, 0), self.rect)

        img = pygame.image.load(self.img)
        img = pygame.transform.scale(img, (self.rect.width, self.rect.height))
        screen.blit(img, self.rect.topleft)

        pygame.display.update()

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def perform_action(self):
        if self.action:
            if self.params is not None:
                self.action(*self.params)
            else:
                self.action()

    def change_background(self, back_str):
        self.background = back_str