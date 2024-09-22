import pygame
import os
# Get the directory of the current file (main.py is inside ProjectRoot)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one folder up (out of ProjectRoot)
PARENT_DIR = os.path.dirname(BASE_DIR)

# Now construct the path to the assets/images folder
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(PARENT_DIR + '/' + filename).convert_alpha()

    def get_sprite(self, x, y, width, height):
        """Extract a specific sprite from the sprite sheet."""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return sprite
