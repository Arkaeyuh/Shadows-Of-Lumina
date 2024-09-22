import pygame

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path=None, color=(255, 255, 255), width=30, height=30):
        super().__init__()
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)