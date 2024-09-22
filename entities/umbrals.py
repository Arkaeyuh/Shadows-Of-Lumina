import pygame
from config import SpriteSheet
from pygame.math import Vector2
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

        self.attack_left_frames = [
            spritesheet.get_sprite(0, 832, 64, 64),
            spritesheet.get_sprite(64, 832, 64, 64),
            spritesheet.get_sprite(128, 832, 64, 64),
            spritesheet.get_sprite(192, 832, 64, 64),
            spritesheet.get_sprite(256, 832, 64, 64),
            spritesheet.get_sprite(320, 832, 64, 64)
        ]

        self.attack_right_frames = [
            spritesheet.get_sprite(0, 960, 64, 64),
            spritesheet.get_sprite(64, 960, 64, 64),
            spritesheet.get_sprite(128, 960, 64, 64),
            spritesheet.get_sprite(192, 960, 64, 64),
            spritesheet.get_sprite(256, 960, 64, 64),
            spritesheet.get_sprite(320, 960, 64, 64)      
        ]

        self.attack_up_frames = [
            spritesheet.get_sprite(0, 768, 64, 64),
            spritesheet.get_sprite(64, 768, 64, 64),
            spritesheet.get_sprite(128, 768, 64, 64),
            spritesheet.get_sprite(192, 768, 64, 64),
            spritesheet.get_sprite(256, 768, 64, 64),
            spritesheet.get_sprite(320, 768, 64, 64),       
        ]

        self.attack_down_frames = [
            spritesheet.get_sprite(0, 896, 64, 64),
            spritesheet.get_sprite(64, 896, 64, 64),
            spritesheet.get_sprite(128, 896, 64, 64),
            spritesheet.get_sprite(192, 896, 64, 64),
            spritesheet.get_sprite(256, 896, 64, 64),
            spritesheet.get_sprite(320, 896, 64, 64)        
        ]

        self.death_frames = [
            spritesheet.get_sprite(0, 1280, 64, 64),
            spritesheet.get_sprite(64, 1280, 64, 64),
            spritesheet.get_sprite(128, 1280, 64, 64),
            spritesheet.get_sprite(192, 1280, 64, 64),
            spritesheet.get_sprite(256, 1280, 64, 64),
            spritesheet.get_sprite(320, 1280, 64, 64)
        ]

        # Initial animation state
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust animation speed (lower = faster)
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
        self.direction = Vector2(1, 0)  # Default direction (right)

        # Screen boundaries to prevent wandering off-screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Wandering cooldown
        self.spawn_position = Vector2(x, y)
        self.wander_timer = 0
        self.wander_interval = random.uniform(1.5, 3.5)  # Every 5 seconds change direction

        # Distance threshold to stop wandering and start chasing
        self.is_attacking = False
        # Cooldown for attacks
        self.attack_cooldown = 1  # 1 second cooldown between attacks
        self.last_attack_time = 0
        self.damage_dealt = False

        self.chase_threshold = 150  # Distance to trigger chase
        self.max_wander_distance = 100  # Max distance from spawn to wander

        self.line_of_sight_blocked = False  # Line of sight detection
        self.is_chasing = False


      # Death state
        self.is_dying = False  # Track if Umbral is in the process of dying
        self.death_animation_done = False  # Track when the death animation has finished


    def update(self, delta_time, player):
        """Update Umbral position and behavior."""
        # Calculate distance to player

        if self.is_dying:
            self.animate(delta_time, player)
            return

        player_position = pygame.Vector2(player.rect.center)
        umbral_position = pygame.Vector2(self.rect.center)
        distance_to_player = umbral_position.distance_to(player_position)

        self.line_of_sight_blocked = self.check_line_of_sight(player)

        if self.is_attacking:
            # If attacking, we won't move
            self.animate(delta_time, player)
            return

        # Stop wandering and chase player if close enough
        if distance_to_player < 50 and self.is_chasing:  # Attack range
            self.is_wandering = False
            self.attack_player(player)

        if self.is_chasing:
            if distance_to_player > self.chase_threshold or self.line_of_sight_blocked:
                # Exit chase if player moves too far or line of sight is broken
                self.is_chasing = False
                self.is_wandering = True
            else:
                self.chase_player(player)
        elif self.is_wandering:
            if distance_to_player < self.chase_threshold and not self.line_of_sight_blocked:
                # Start chasing if player is in range and visible
                self.is_chasing = True
                self.is_wandering = False
            else:
                self.wander(delta_time)

        # Handle animation
        self.animate(delta_time, player)


    def attack_player(self, player):
        """Attack the player if within range."""
        current_time = pygame.time.get_ticks() / 1000  # Get time in seconds

        # Check if we are allowed to attack (based on cooldown)
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time
            player.take_damage(20)  # Deal damage to the player
            self.current_frame = 0
            self.damage_dealt = False
        else:
            self.is_attacking = False

    def wander(self, delta_time):
        """Wandering movement logic for Umbral."""
        self.wander_timer += delta_time

        # Change direction periodically based on the wander interval
        if self.wander_timer >= self.wander_interval:
            self.wander_timer = 0

            distance_from_spawn = Vector2(self.rect.center).distance_to(self.spawn_position)

            if distance_from_spawn > self.max_wander_distance:
                # Return to spawn if wandering too far
                direction = (self.spawn_position - Vector2(self.rect.center)).normalize()
                self.direction = direction  # Set direction to move toward spawn
            else:
                # Choose a new random direction within the allowed radius
                dx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)  # Random step size
                dy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                self.direction = Vector2(dx, dy).normalize()

        # Move continuously in the current direction
        self.rect.x += self.direction.x * self.speed * 0.5  # Increased speed for visibility
        self.rect.y += self.direction.y * self.speed * 0.5

        self.update_direction(self.direction)  # Update animation direction

    def chase_player(self, player):
        """Chase the player if they are nearby."""
        player_position = Vector2(player.rect.center)
        umbral_position = Vector2(self.rect.center)

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

    def check_line_of_sight(self, player):
        """Check if there are obstacles between Umbral and player."""
        player_pos = Vector2(player.rect.center)
        umbral_pos = Vector2(self.rect.center)
        
        # Simple distance check for line of sight (you can add raycasting if needed)
        return player_pos.distance_to(umbral_pos) > self.chase_threshold

    # def change_direction(self):
    #     """Change direction randomly for wandering behavior."""
    #     directions = [
    #         pygame.Vector2(1, 0),   # Right
    #         pygame.Vector2(-1, 0),  # Left
    #         pygame.Vector2(0, 1),   # Down
    #         pygame.Vector2(0, -1)   # Up
    #     ]
    #     self.direction = directions[random.randint(0, len(directions) - 1)]
    
    def update_direction(self, direction):
        """Update the direction for animations."""
        if abs(direction.x) > abs(direction.y):
            if direction.x > 0:
                self.direction = Vector2(1, 0)  # Right
            else:
                self.direction = Vector2(-1, 0)  # Left
        else:
            if direction.y > 0:
                self.direction = Vector2(0, 1)  # Down
            else:
                self.direction = Vector2(0, -1)  # U
                
    def animate(self, delta_time, player):
        """Handles sprite animation."""
        self.animation_timer += delta_time

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.is_dying:
                # Play death animation
                self.current_frame += 1
                if self.current_frame < len(self.death_frames):
                    self.image = self.death_frames[self.current_frame]
                else:
                    self.death_animation_done = True
                    self.kill()  # Remove the sprite after the death animation
                return

            if self.is_attacking:
                # Play attack animation based on direction
                attack_frames = None
                if self.direction.x > 0:
                    attack_frames = self.attack_right_frames
                elif self.direction.x < 0:
                    attack_frames = self.attack_left_frames
                elif self.direction.y > 0:
                    attack_frames = self.attack_down_frames
                elif self.direction.y < 0:
                    attack_frames = self.attack_up_frames

                self.image = attack_frames[self.current_frame]

                # Update attack animation frame
                self.current_frame += 1

                # If at the middle of the attack animation, deal damage
                middle_frame = len(attack_frames) // 2
                if self.current_frame == middle_frame and not self.damage_dealt:
                    player.take_damage(20)  # Deal damage to the player
                    self.damage_dealt = True  # Prevent further damage from this attack

                # After the attack animation completes, stop attacking
                if self.current_frame >= len(attack_frames):
                    self.is_attacking = False  # Reset attack state
                    self.current_frame = 0  # Reset frame counter
            else:
                # Continue normal walking animations
                self.current_frame = (self.current_frame + 1) % len(self.walk_right_frames)

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
            self.is_dying = True
            self.current_frame = 0

    def draw(self, screen):
        """Draw the Umbral sprite on the screen."""
        screen.blit(self.image, self.rect)