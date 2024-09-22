import pygame

class Powerup(pygame.sprite.Sprite):

    def __init__(self, x, y, color, width, height) -> None:
        super().__init__()
        
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def apply(self, player) -> None:
        """This method will be overridden in the child classes."""
        pass