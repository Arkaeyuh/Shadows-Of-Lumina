import pygame
from config import SpriteSheet
import random

class Umbral(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, screen_width, screen_height):
        super().__init__()

        # Load the sprite sheet for Umbral
        spritesheet = SpriteSheet('assets/spritesheets/umbral_spritesheet.png')

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
        ]  # Flip right frames to get left frames

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
        self.animation_speed = 0.2  # Adjust animation speed (lower = faster)
        self.animation_timer = 0

        # Set the initial image and rect
        self.image = self.walk_right_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Umbral properties
        self.speed = speed
        self.health = 50
        self.is_wandering = True  # Determines if Umbral is wandering or chasing player
        self.direction = pygame.Vector2(1, 0)  # Default direction (right)

        # Screen boundaries to prevent wandering off-screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Wandering cooldown
        self.wander_timer = 0
        self.wander_interval = 5  # Every 5 seconds change direction

        # Distance threshold to stop wandering and start chasing
        self.chase_threshold = 200  # Distance in pixels

    def update(self, delta_time, player):
        """Update Umbral position and behavior."""
        # Calculate distance to player
        player_position = pygame.Vector2(player.rect.center)
        umbral_position = pygame.Vector2(self.rect.center)
        distance_to_player = umbral_position.distance_to(player_position)

        # Stop wandering and chase player if close enough
        if distance_to_player < self.chase_threshold:
            self.is_wandering = False
        else:
            self.is_wandering = True

        if self.is_wandering:
            self.wander(delta_time)
        else:
            self.chase_player(player)

        # Handle animation
        self.animate(delta_time)

    def wander(self, delta_time):
        """Wandering movement logic for Umbral."""
        # Update the wander timer
        self.wander_timer += delta_time

        # Change direction every interval
        if self.wander_timer >= self.wander_interval:
            self.wander_timer = 0
            self.change_direction()

        # Move in the current direction
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Prevent the Umbral from wandering off the screen by reversing direction at boundaries
        if self.rect.x <= 0:
            self.rect.x = 0
            self.direction.x = abs(self.direction.x)  # Move right
        elif self.rect.x >= self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width
            self.direction.x = -abs(self.direction.x)  # Move left

        if self.rect.y <= 0:
            self.rect.y = 0
            self.direction.y = abs(self.direction.y)  # Move down
        elif self.rect.y >= self.screen_height - self.rect.height:
            self.rect.y = self.screen_height - self.rect.height
            self.direction.y = -abs(self.direction.y)  # Move up

    def chase_player(self, player):
        """Chase the player if they are nearby."""
        player_position = pygame.Vector2(player.rect.center)
        umbral_position = pygame.Vector2(self.rect.center)

        direction = player_position - umbral_position

        EPSILON = 1e-6

        # Calculate direction to player
        if (direction.length_squared() > EPSILON):
            direction = (player_position - umbral_position).normalize()

        # Move toward the player
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        # Set the direction for the animation
        if abs(direction.x) > abs(direction.y):
            self.direction = pygame.Vector2(1 if direction.x > 0 else -1, 0)  # Horizontal movement
        else:
            self.direction = pygame.Vector2(0, 1 if direction.y > 0 else -1)  # Vertical movement

    def change_direction(self):
        """Change direction randomly for wandering behavior."""
        directions = [
            pygame.Vector2(1, 0),   # Right
            pygame.Vector2(-1, 0),  # Left
            pygame.Vector2(0, 1),   # Down
            pygame.Vector2(0, -1)   # Up
        ]
        self.direction = directions[random.randint(0, len(directions) - 1)]

    def animate(self, delta_time):
        """Handles sprite animation."""
        self.animation_timer += delta_time

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 9  # 4 frames

            # Choose the correct frames based on the direction
            if self.direction.x > 0:
                self.image = self.walk_right_frames[self.current_frame]
            elif self.direction.x < 0:
                self.image = self.walk_left_frames[self.current_frame]
            elif self.direction.y > 0:
                self.image = self.walk_down_frames[self.current_frame]
            elif self.direction.y < 0:
                self.image = self.walk_up_frames[self.current_frame]

    def take_damage(self, amount):
        """Reduce health when hit."""
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the Umbral from the game when dead

    def draw(self, screen):
        """Draw the Umbral sprite on the screen."""
        screen.blit(self.image, self.rect)
