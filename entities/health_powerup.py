from .powerup import Powerup
import pygame
import os

# Setup asset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

class HealthPowerup(Powerup):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        # Load the sprite image for the health powerup
        self.image = pygame.image.load(ASSETS_DIR + '/images/items/health_power.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))  # Adjust size if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def apply(self, player) -> None:
        """Increases the player's max health."""
        player.max_health += 20  # Adjust this value as needed
        player.health = player.max_health  # Heal the player fully
        print("Max Health increased!")

    def draw(self, screen):
        """Draw the powerup on the screen."""
        screen.blit(self.image, self.rect)