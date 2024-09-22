from .powerup import Powerup
import pygame

class HealthPowerup(Powerup):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, color=(255, 0, 0), width=30, height=30)  # Red color for Health

    def apply(self, player) -> None:
        """Increases the player's max health."""
        
        player.max_health += 20  # Adjust this value as needed
        player.health = player.max_health  # Heal the player fully
        print("Max Health increased!")