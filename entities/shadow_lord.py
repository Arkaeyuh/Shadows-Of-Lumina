import pygame
from pygame.math import Vector2
from config import SpriteSheet
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, width, height, health):
        super().__init__()

        # Load the sprite sheet for Boss
        spritesheet = SpriteSheet('assets/spritesheets/shadow_lord_spritesheet.png')
        self.projectiles2 = pygame.sprite.Group()

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

        # Set the initial image and rect
        self.image = self.walk_right_frames[0]  # Start with first right frame
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Boss properties
        self.speed = speed
        self.health = health
        self.max_health = health
        self.projectiles = []
        self.cooldown = 0  # Cooldown time between shots
        self.cooldown2 = 0

        # Animation properties
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

        # Direction and chasing logic
        self.direction = Vector2(1, 0)  # Default direction (right)
        self.is_attacking = False
        self.attack_cooldown = 1
        self.last_attack_time = 0

    def shoot(self, player):
        """Boss shoots projectiles toward the player."""
        if self.cooldown == 0:
            # Create a projectile moving toward the player's current position
            player_position = Vector2(player.rect.center)
            boss_position = Vector2(self.rect.center)

            EPSILON = 1e-6

            if (player_position - boss_position).length_squared() > EPSILON:
                direction = (player_position - boss_position).normalize()
            else:
                direction = self.image.get_rect(center=(1, 1))

            # Create a projectile that moves in the direction of the player
            projectile_rect = pygame.Rect(self.rect.centerx - 2, self.rect.centery - 2, 5, 10)
            self.projectiles.append({
                'rect': projectile_rect,
                'direction': direction
            })
            self.cooldown = 50  # Reset cooldown time

    def update_projectiles(self, player):
        """Update projectile movement and check for collisions with the player."""
        for projectile in self.projectiles[:]:
            # Move the projectile in its assigned direction
            projectile['rect'].x += projectile['direction'].x * 5
            projectile['rect'].y += projectile['direction'].y * 5

            # Check if the projectile hits the player
            if projectile['rect'].colliderect(player.rect):
                player.take_damage(10)  # Player takes damage if hit
                self.projectiles.remove(projectile)  # Remove projectile on hit
            # Remove projectile if it leaves the screen
            elif not pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).colliderect(projectile['rect']):
                self.projectiles.remove(projectile)

    def chase_player(self, player):
        """Chase the player at all times."""
        player_position = Vector2(player.rect.center)
        boss_position = Vector2(self.rect.center)

        direction = player_position - boss_position

        EPSILON = 1e-6

        # Normalize direction to get unit vector
        if direction.length_squared() > EPSILON:
            direction = direction.normalize()

        # Move toward the player
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        # Update the animation direction
        self.update_direction(direction)

    def update_direction(self, direction):
        """Update the animation direction based on movement."""
        if abs(direction.x) > abs(direction.y):
            # Horizontal movement
            if direction.x > 0:
                self.image = self.walk_right_frames[self.current_frame]
            else:
                self.image = self.walk_left_frames[self.current_frame]
        else:
            # Vertical movement
            if direction.y > 0:
                self.image = self.walk_down_frames[self.current_frame]
            else:
                self.image = self.walk_up_frames[self.current_frame]

    def update(self, delta_time, player):
        """Update the boss logic, including movement, animations, and shooting."""
        # Chasing the player
        self.chase_player(player)

        # Shooting projectiles
        if self.cooldown > 0:
            self.cooldown -= 1
        self.shoot(player)

    # Call the circular attack at specific intervals (or when desired)
        if self.cooldown2 > 0:
            self.cooldown2 -=1

        if self.cooldown2 == 0:  # Example trigger for shooting circle projectiles
            self.shoot_circle_projectiles()
            self.cooldown2 = 250  # Add a cooldown before shooting the circle again
        # Update projectiles
        self.update_projectiles(player)
        self.projectiles2.update(player)

        # Update animation
        self.animate(delta_time)

    def animate(self, delta_time):
        """Handle animation frames for movement and attacking."""
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_right_frames)  # Cycle frames

    def draw(self, screen):
        """Draw the boss, projectiles, and health bar."""
        screen.blit(self.image, self.rect)

        # Draw projectiles
        for projectile in self.projectiles:
            pygame.draw.rect(screen, (255, 255, 0), projectile['rect'])
        
        self.projectiles2.draw(screen)

        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """Draw the boss health bar at the bottom center of the screen with a black outline."""
        health_ratio = self.health / self.max_health

        # Define dimensions
        bar_width = 400
        bar_height = 30
        outline_thickness = 4

        # Calculate position: bottom center of the screen
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT - bar_height - 20  # 20 pixels above the bottom

        # Draw the black outline
        pygame.draw.rect(screen, (0, 0, 0), (bar_x - outline_thickness, bar_y - outline_thickness, bar_width + outline_thickness * 2, bar_height + outline_thickness * 2))

        # Draw the red background (empty part of the health bar)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Draw the green foreground (filled part of the health bar)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def take_damage(self, damage):
        """Handle boss taking damage."""
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Remove boss from game

    def shoot_circle_projectiles(self):
        """Boss shoots projectiles in a circular pattern."""
        boss_pos = self.rect.center
        num_projectiles = 12  # Number of projectiles in the circle
        angle_increment = 360 / num_projectiles

        for i in range(num_projectiles):
            angle = i * angle_increment
            direction = pygame.math.Vector2(1, 0).rotate(angle)
            projectile = BossProjectile(boss_pos[0], boss_pos[1], direction)
            self.projectiles2.add(projectile)







class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # A simple 10x10 projectile
        self.image.fill((255, 255, 0))  # Yellow color for the projectile
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction.normalize()  # Normalize the direction vector
        self.speed = 5  # Speed of the projectile

    def update(self, player):
        # Move the projectile in its direction
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.rect.colliderect(player.rect):
            player.take_damage(10)  # Player takes damage if hit
            self.kill()  # Remove

        # Remove the projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove projectile from all sprite groups