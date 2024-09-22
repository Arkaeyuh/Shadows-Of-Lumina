from .powerup import Powerup
import pygame
import os

# Setup asset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

class LuminaPowerup(Powerup):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        # Load the sprite image for the health powerup
        self.image = pygame.image.load(ASSETS_DIR + '/images/items/lumina_power.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))  # Adjust size if needed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def apply(self, player) -> None:
        """Increases the player's max lumina energy."""
        player.max_lumina_energy += 20  # Adjust this value as needed
        player.lumina_regen_rate += 5
        player.lumina_energy = player.max_lumina_energy  # Restore lumina energy fully
        print("Max Lumina increased!")


    def draw(self, screen):
        """Draw the powerup on the screen."""
        screen.blit(self.image, self.rect)