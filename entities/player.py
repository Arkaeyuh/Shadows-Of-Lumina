import pygame
from config import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()

        # Load the sprite sheet
        spritesheet = SpriteSheet('assets/spritesheets/elysia_spritesheet.png')

        # Idle and walking animation frames (4 frames each)
        self.idle_frames = [
            spritesheet.get_sprite(0, 0, 256, 256),
            spritesheet.get_sprite(256, 0, 256, 256),
            spritesheet.get_sprite(512, 0, 256, 256),
            spritesheet.get_sprite(768, 0, 256, 256)
        ]
        self.walk_frames = [
            spritesheet.get_sprite(0, 128, 128, 128),
            spritesheet.get_sprite(128, 128, 128, 128),
            spritesheet.get_sprite(256, 128, 128, 128),
            spritesheet.get_sprite(384, 128, 128, 128)
        ]

        # Initial animation state
        self.current_frame = 0
        self.animation_speed = 0.15  # Adjust animation speed (lower = faster)
        self.animation_timer = 0
        self.is_walking = False

        # Set the initial image and rect
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Player properties
        self.speed = speed
        self.health = 100
        self.lumina_energy = 100

    def update(self, keys_pressed, delta_time):
        """Update the player position and animation based on input."""
        dx, dy = 0, 0
        self.is_walking = False  # Reset walking status

        # Movement controls
        if keys_pressed[pygame.K_w]:
            dy = -self.speed
            self.is_walking = True
        if keys_pressed[pygame.K_s]:
            dy = self.speed
            self.is_walking = True
        if keys_pressed[pygame.K_a]:
            dx = -self.speed
            self.is_walking = True
        if keys_pressed[pygame.K_d]:
            dx = self.speed
            self.is_walking = True

        # Update position
        self.rect.x += dx
        self.rect.y += dy

        # Handle animation
        self.animate(delta_time)

    def animate(self, delta_time):
        """Handles sprite animation based on the player's state."""
        self.animation_timer += delta_time

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4  # 4 frames

            # Choose frames based on walking state
            if self.is_walking:
                self.image = self.walk_frames[self.current_frame]
            else:
                self.image = self.idle_frames[self.current_frame]

    def draw(self, screen):
        """Draw the player sprite on the screen."""
        screen.blit(self.image, self.rect)
