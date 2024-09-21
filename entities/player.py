import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load('assets/images/characters/elysia.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = 100
        self.lumina_energy = 100
    
    def update(self, keys_pressed):
        dx, dy = 0, 0
        if keys_pressed[pygame.K_w]:
            dy = -self.speed
        if keys_pressed[pygame.K_s]:
            dy = self.speed
        if keys_pressed[pygame.K_a]:
            dx = -self.speed
        if keys_pressed[pygame.K_d]:
            dx = self.speed
        
        self.rect.x += dx
        self.rect.y += dy
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
