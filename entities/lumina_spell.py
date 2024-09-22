import pygame

class LuminaSpell(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=5) -> None:
        super().__init__()

        # Create a white rectangle to represent the spell
        self.image = pygame.Surface((10, 5))  # Width = 10, Height = 5
        self.image.fill((255, 255, 255))  # White color

        # Set the position of the spell
        self.rect = self.image.get_rect(center=(x, y))

        # Spell properties
        self.direction = direction  # Vector2 direction (e.g., (1, 0) for right)
        self.speed = speed
        self.range = 400  # Maximum distance the spell can travel
        self.distance_traveled = 0

    def update(self, delta_time) -> None:
        
        # Move the spell in the specified direction
        move_x = self.direction.x * self.speed 
        move_y = self.direction.y * self.speed  

        # Update position
        self.rect.x += move_x
        self.rect.y += move_y

        # Update distance traveled
        self.distance_traveled += abs(move_x) + abs(move_y)

        # Remove the spell if it has traveled beyond its range
        if self.distance_traveled > self.range:
            self.kill()  # Remove the spell from the sprite group
