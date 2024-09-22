import pygame
from pygame.math import Vector2
import time
from config import SpriteSheet
from .lumina_spell import LuminaSpell

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()

        # Load the sprite sheet
        spritesheet = SpriteSheet('assets/spritesheets/elysia_spritesheet.png')

        # Walk right frames (9 frames)
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

        # Walk left frames (9 frames)
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

        # Walk down frames (9 frames)
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
        self.max_lumina_energy = 100
        self.lumina_cost = 10
        self.spell_range = 50
        self.spells = pygame.sprite.Group()

        # Cooldown settings
        self.spell_cooldown = 0.5  # Cooldown of 0.5 seconds between spells (2 spells per second)
        self.last_spell_time = 0  # Last time a spell was cast

        # Lumina passive regeneration settings
        self.lumina_regen_rate = 5  # Lumina energy regenerated per second
        self.last_regen_time = time.time()  # Time of last regeneration

        self.damage_cooldown = 1  # 1 second cooldown between taking damage
        self.last_damage_time = 0

    def update(self, keys_pressed, delta_time, screen_width, screen_height, umbrals):
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

        # Ensure player does not walk off the screen (apply boundary checks)
        if 0 <= self.rect.x + dx <= screen_width - self.rect.width:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= screen_height - self.rect.height:
            self.rect.y += dy

        # Handle animation
        self.animate(delta_time)

        # Cast Lumina spell if the spacebar is pressed and player has enough energy
        if keys_pressed[pygame.K_SPACE]:
            self.cast_lumina_spell()

        self.regenerate_lumina(delta_time)
        self.spells.update(delta_time)

        # Check for collisions between spells and Umbrals
        for spell in self.spells:
            # Check if the spell hits any Umbral
            umbrals_hit = pygame.sprite.spritecollide(spell, umbrals, False)

            if umbrals_hit:
                # Damage all Umbrals hit and remove the spell
                for umbral in umbrals_hit:
                    umbral.take_damage(25)  # Deal damage to the Umbral
                spell.kill()  # Ensure the spell is removed after hitting an Umbraiil

        # self.check_umbral_collision(umbrals)

    def take_damage(self, amount):
        """Reduces player's health and checks if the player is still alive."""
        current_time = time.time()

        # Check if the damage cooldown has passed
        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.health -= amount
            self.last_damage_time = current_time

            if self.health <= 0:
                self.health = 0
                self.kill()  # Remove the player from the game if health is depleted
                print("Player has died.")  # Handle death logic here (game over, etc.)

    # def check_umbral_collision(self, umbrals):
    #     """Check for collisions between the player and any umbrals."""
    #     umbrals_hit = pygame.sprite.spritecollide(self, umbrals, False)

    #     # If the player collides with any umbral, take damage
    #     if umbrals_hit:
    #         self.take_damage(20)  # Adjust the damage value as needed


    def regenerate_lumina(self, delta_time):
        """Regenerate Lumina energy over time."""
        current_time = time.time()

        # Check if enough time has passed to regenerate energy
        if current_time - self.last_regen_time >= 1:  # Every second
            # Regenerate lumina energy at the defined rate
            self.lumina_energy += self.lumina_regen_rate * (current_time - self.last_regen_time)
            self.lumina_energy = min(self.lumina_energy, self.max_lumina_energy)  # Clamp to max energy
            self.last_regen_time = current_time  # Update last regen tim

    def cast_lumina_spell(self):
        """Cast a Lumina spell in the direction the player is facing."""

        current_time = time.time()

        if current_time - self.last_spell_time >= self.spell_cooldown:
            if self.lumina_energy >= self.lumina_cost:
                self.lumina_energy -= self.lumina_cost  # Deplete energy

                # Determine direction of the spell
                if self.direction == "right":
                    spell_direction = Vector2(1, 0)
                elif self.direction == "left":
                    spell_direction = Vector2(-1, 0)
                elif self.direction == "up":
                    spell_direction = Vector2(0, -1)
                elif self.direction == "down":
                    spell_direction = Vector2(0, 1)

                spell = LuminaSpell(self.rect.centerx, self.rect.centery, spell_direction)
                self.spells.add(spell)

                self.last_spell_time = current_time

    def animate(self, delta_time):
        """Handles sprite animation based on the player's state."""
        self.animation_timer += delta_time

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 9  # 9 frames

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
        self.spells.draw(screen)
