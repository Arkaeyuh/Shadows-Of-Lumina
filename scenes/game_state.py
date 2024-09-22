import pygame
from entities import Player, Umbral, Boss
from world import Room, Door, RoomManager
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import HUD


class GameState:
    def __init__(self, state_manager):
        
        self.state_manager = state_manager
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        
        # Initialize player
        self.player = Player(self.screen_width // 2, self.screen_height // 2, 2, self.state_manager)  # Define player at screen center

        # Initialize Umbrals and add them to a group
        self.umbrals = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()

        # Initialize HUD for health and Lumina energy display
        self.hud = HUD(self.player, self.screen_width, self.screen_height)

        # Initialize rooms and room manager
        self.room_manager = RoomManager()
        self.initialize_rooms()


    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        
    def update(self, delta_time):
        """Updates the game logic."""
        # Get key input
        keys_pressed = pygame.key.get_pressed()

        # Update player movement and animation
        self.player.update(keys_pressed, delta_time, SCREEN_WIDTH, SCREEN_HEIGHT, self.room_manager.current_room.enemies)

        # Update Umbrals in the current room
        self.room_manager.update(self.player, delta_time)


    def render(self, screen):
        """Renders the current game state."""

        # Draw the current room
        self.room_manager.draw(screen)

        # Draw the player and umbrals
        self.player.draw(screen)

        # Draw the HUD (health, lumina, etc.)
        self.hud.draw(screen)

        # Update the screen (swap buffers)
        pygame.display.flip()

    def initialize_rooms(self):
        """Initialize all rooms and return the starting room."""
        # Create Room 1 and add enemies and a door
        room_1 = Room(room_id="room_1",background_image_path="/world/room1.png")
        room_1.add_enemy(Umbral(200, 200, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_1.add_enemy(Umbral(300, 300, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_1.add_door(Door(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 75, 50, 150, "room_2"))  # Door leading to Room 2
        room_1.add_door(Door(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 50, 150, 50, "room_3"))

        # Create Room 2 with a door leading back to Room 1
        room_2 = Room(room_id="room_2",background_image_path="/world/room2.png")
        room_2.add_enemy(Umbral(400, 200, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_2.add_enemy(Umbral(500, 300, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_2.add_door(Door(0, SCREEN_HEIGHT // 2 - 65, 50, 150, "room_1"))  # Door leading back to Room 1
        room_2.add_door(Door(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 65, 50, 150, "room_4"))

        room_3 = Room(room_id="room_3",background_image_path="/world/room3.png")
        room_3.add_enemy(Umbral(400, 200, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_3.add_enemy(Umbral(500, 300, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_3.add_door(Door(SCREEN_WIDTH // 2 - 65, 0, 150, 50, "room_1"))  # Door leading back to Room 1

        # Create Room 3 (boss room) with a special door leading to it
        room_4 = Room(room_id="room_4",background_image_path="/world/room4.png", is_boss_room=True)
        room_4.add_enemy(Boss(600, 300, 200, 200, 300))  # Boss Umbral here
        room_4.add_enemy(Umbral(400, 200, 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        room_4.add_door(Door(0, SCREEN_HEIGHT // 2 - 65, 50, 150, "room_2"))

        # Create a room manager and add rooms
        self.room_manager.add_room(room_1)
        self.room_manager.add_room(room_2)
        self.room_manager.add_room(room_3)
        self.room_manager.add_room(room_4)

        self.room_manager.change_room("room_1", self.player, )