import pygame
from config import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()

        # Load the sprite sheet
        spritesheet = SpriteSheet('assets/spritesheets/elysia_spritesheet.png')

        # Walk right frames (4 frames)
        self.walk_right_frames = [
            spritesheet.get_sprite(0, 704, 64, 64),
            spritesheet.get_sprite(64, 704, 64, 64),
            spritesheet.get_sprite(128, 704, 64, 64),
            spritesheet.get_sprite(192, 704, 64, 64),
            spritesheet.get_sprite(256, 704, 64, 64),
            spritesheet.get_sprite(320, 704, 64, 64),
            spritesheet.get_sprite(384, 704, 64, 64),
            spritesheet.get_sprite(448, 704, 64, 64),
            spritesheet.get_sprite(512, 704, 64, 64)
        ]

        # Walk left frames (4 frames)
        self.walk_left_frames = [
            spritesheet.get_sprite(0, 576, 64, 64),
            spritesheet.get_sprite(64, 576, 64, 64),
            spritesheet.get_sprite(128, 576, 64, 64),
            spritesheet.get_sprite(192, 576, 64, 64),
            spritesheet.get_sprite(256, 576, 64, 64),
            spritesheet.get_sprite(320, 576, 64, 64),
            spritesheet.get_sprite(384, 576, 64, 64),
            spritesheet.get_sprite(448, 576, 64, 64),
            spritesheet.get_sprite(512, 576, 64, 64)
        ]

        # Walk up frames (4 frames)
        self.walk_up_frames = [
            spritesheet.get_sprite(0, 512, 64, 64),
            spritesheet.get_sprite(64, 512, 64, 64),
            spritesheet.get_sprite(128, 512, 64, 64),
            spritesheet.get_sprite(192, 512, 64, 64),
            spritesheet.get_sprite(256, 512, 64, 64),
            spritesheet.get_sprite(320, 512, 64, 64),
            spritesheet.get_sprite(384, 512, 64, 64),
            spritesheet.get_sprite(448, 512, 64, 64),
            spritesheet.get_sprite(512, 512, 64, 64)
        ]

        # Walk down frames (4 frames)
        self.walk_down_frames = [
            spritesheet.get_sprite(0, 640, 64, 64),
            spritesheet.get_sprite(64, 640, 64, 64),
            spritesheet.get_sprite(128, 640, 64, 64),
            spritesheet.get_sprite(192, 640, 64, 64),
            spritesheet.get_sprite(256, 640, 64, 64),
            spritesheet.get_sprite(320, 640, 64, 64),
            spritesheet.get_sprite(384, 640, 64, 64),
            spritesheet.get_sprite(448, 640, 64, 64),
            spritesheet.get_sprite(512, 640, 64, 64)
        ]

        # Initial animation state
        self.current_frame = 0
        self.animation_speed = 0.15  # Adjust animation speed (lower = faster)
        self.animation_timer = 0
        self.is_walking = False
        self.direction = "down"  # Start by facing down

        # Set the initial image and rect
        self.image = self.walk_down_frames[self.current_frame]
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
            self.direction = "up"  # Walking up
        if keys_pressed[pygame.K_s]:
            dy = self.speed
            self.is_walking = True
            self.direction = "down"  # Walking down
        if keys_pressed[pygame.K_a]:
            dx = -self.speed
            self.is_walking = True
            self.direction = "left"  # Walking left
        if keys_pressed[pygame.K_d]:
            dx = self.speed
            self.is_walking = True
            self.direction = "right"  # Walking right

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
            self.current_frame = (self.current_frame + 1) % 9  # 4 frames

            # Choose frames based on walking state and direction
            if self.is_walking:
                if self.direction == "right":
                    self.image = self.walk_right_frames[self.current_frame]
                elif self.direction == "left":
                    self.image = self.walk_left_frames[self.current_frame]
                elif self.direction == "up":
                    self.image = self.walk_up_frames[self.current_frame]
                elif self.direction == "down":
                    self.image = self.walk_down_frames[self.current_frame]
            else:
                # Keep the last frame based on the last direction
                if self.direction == "right":
                    self.image = self.walk_right_frames[0]  # Idle pose facing right
                elif self.direction == "left":
                    self.image = self.walk_left_frames[0]  # Idle pose facing left
                elif self.direction == "up":
                    self.image = self.walk_up_frames[0]  # Idle pose facing up
                elif self.direction == "down":
                    self.image = self.walk_down_frames[0]  # Idle pose facing down
    def draw(self, screen):
        """Draw the player sprite on the screen."""
        screen.blit(self.image, self.rect)
