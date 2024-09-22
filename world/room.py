from config.settings import SCREEN_WIDTH,SCREEN_HEIGHT
import pygame

class Room:
    def __init__(self, room_id, is_boss_room=False):
        self.room_id = room_id  # Unique identifier for the room
        self.is_boss_room = is_boss_room  # Whether this room contains the boss
        self.enemies = pygame.sprite.Group()  # Group for enemies in the room
        self.doors = []  # List of doors leading to other rooms
        self.powerups = pygame.sprite.Group()  # Group for powerups or items

    def add_enemy(self, enemy):
        self.enemies.add(enemy)

    def add_door(self, door):
        self.doors.append(door)

    def add_powerup(self, powerup):
        self.powerups.add(powerup)

    def draw(self, screen):
        """Draw the room layout, enemies, and items."""
        # You could draw room boundaries or background here
        for door in self.doors:
            door.draw(screen)
        self.enemies.draw(screen)
        self.powerups.draw(screen)

    def update(self, delta_time, player):
        """Update all room objects (enemies, items)."""
        self.enemies.update(delta_time, player)
        self.powerups.update(delta_time)

        for spell in player.spells:
            enemies_hit = pygame.sprite.spritecollide(spell, self.enemies, False)
            if enemies_hit:
                for enemy in enemies_hit:
                    enemy.take_damage(25)  # Adjust damage value as needed
                spell.kill()  # Remove the spell after collision

class Door:
    def __init__(self, x, y, width, height, leads_to):
        self.rect = pygame.Rect(x, y, width, height)  # Door's position and size
        self.leads_to = leads_to  # The ID of the room this door leads to

    def draw(self, screen):
        """Draw the door."""
        pygame.draw.rect(screen, (255, 255, 0), self.rect)  # Yellow door

    def check_collision(self, player):
        """Check if the player collides with the door."""
        return self.rect.colliderect(player.rect)

class RoomManager:
    def __init__(self):
        self.current_room = None  # Start in the first room
        self.rooms = {}  # Dictionary of rooms by room_id
        self.transition_cooldown = 0

    def add_room(self, room):
        self.rooms[room.room_id] = room
        print(f"Room {room.room_id} added")
        print(self.rooms)

    def change_room(self, room_id, player=None, entering_door=None):
        """Transition to a different room."""
        print(self.rooms)
        if room_id in self.rooms:
            print(f"Changing to room: {room_id}")  # Debug message
            self.current_room = self.rooms[room_id]

            # Find the door in the new room that leads back to the current room
            for door in self.current_room.doors:
                if door.leads_to == entering_door and player != None:
                    # Place the player outside the door based on door position
                    if door.rect.x == 0:  # Left side of the room
                        player.rect.x = door.rect.x + door.rect.width + 10
                    elif door.rect.right == SCREEN_WIDTH:  # Right side of the room
                        player.rect.x = door.rect.x - player.rect.width - 10
                    elif door.rect.y == 0:  # Top side of the room
                        player.rect.y = door.rect.y + door.rect.height + 10
                    elif door.rect.bottom == SCREEN_HEIGHT:  # Bottom side of the room
                        player.rect.y = door.rect.y - player.rect.height - 10

                    self.transition_cooldown = 1.0  # Set cooldown for 1 second
                    break


        else:
            print(f"Room {room_id} not found!")  # Handle missing room

    def update(self, player, delta_time):
        """Update the current room and check for transitions."""
        if self.current_room:
            self.current_room.update(delta_time, player)
            # Reduce cooldown over time
            if self.transition_cooldown > 0:
                self.transition_cooldown -= delta_time

            # Only check for door collisions if cooldown is over
            if self.transition_cooldown <= 0:
                for door in self.current_room.doors:
                    if door.check_collision(player):
                        self.change_room(door.leads_to, player, self.current_room.room_id)

    def draw(self, screen):
        """Draw the current room."""
        if self.current_room:
            self.current_room.draw(screen)