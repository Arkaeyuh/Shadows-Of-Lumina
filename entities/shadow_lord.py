import pygame
import random
from config.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Boss(pygame.sprite.Sprite):  # Inherit from pygame.sprite.Sprite
    def __init__(self, x, y, width, height, health):
        super().__init__()  # Initialize the Sprite class
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.projectiles = []
        self.cooldown = 0  # Cooldown time between shots

        # Create a surface for the boss's visual representation
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Fill the boss with red color

        # Create a rect from the surface for positioning and collision
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)  # Set the initial position

    def shoot(self):
        """Boss shoots projectiles at regular intervals."""
        if self.cooldown == 0:
            # Create a projectile coming from the center of the boss
            projectile = pygame.Rect(self.x + self.width // 2, self.y + self.height, 5, 10)
            self.projectiles.append(projectile)
            self.cooldown = 50  # Reset cooldown time (you can adjust this for faster or slower shooting)

    def update_projectiles(self, player):
        """Update projectile movement and check for collisions with the player."""
        for projectile in self.projectiles[:]:
            projectile.y += 5  # Projectiles move downward
            if projectile.colliderect(player.rect):
                player.health -= 10  # Player takes damage if hit
                self.projectiles.remove(projectile)  # Remove projectile on hit
            elif projectile.y > SCREEN_HEIGHT:  # If projectile leaves the screen (assuming screen height is 600)
                self.projectiles.remove(projectile)

    def take_damage(self, damage):
        """Reduce the boss's health when hit by the player."""
        self.health -= damage
        print(f"Took {damage}, {self.health} health remaining")
        if self.health <= 0:
            self.kill()
    
    def draw(self, screen):
        """Draw the boss, its health bar, and its projectiles."""
        # Draw boss rectangle
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
        # Draw projectiles
        for projectile in self.projectiles:
            pygame.draw.rect(screen, (255, 255, 0), projectile)
    
    def draw_health_bar(self, screen):
        """Draw the large, on-screen health bar."""
        health_ratio = self.health / self.max_health  # Calculate health ratio

        # Background bar (red) - the empty part
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))  # Health bar background

        # Foreground bar (green) - the filled part representing remaining health
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 200 * health_ratio, 20))  # Health bar foreground

    def update(self, delta_time, player):
        """Update the boss logic."""
        if self.cooldown > 0:
            self.cooldown -= 1  # Reduce cooldown timer

        self.shoot()  # Shoot projectiles at intervals
        self.update_projectiles(player)  # Check collisions and update projectile positions