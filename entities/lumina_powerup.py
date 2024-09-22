from .powerup import Powerup
import pygame

class LuminaPowerup(Powerup):
    def __init__(self, x, y) -> None:
        super().__init__(x, y, color=(0, 0, 255), width=30, height=30)  # Blue color for Lumina

    def apply(self, player) -> None:
        """Increases the player's max lumina energy."""

        player.max_lumina_energy += 20  # Adjust this value as needed
        player.lumina_regen_rate += 5
        player.lumina_energy = player.max_lumina_energy
        print("Max Lumina increased!")