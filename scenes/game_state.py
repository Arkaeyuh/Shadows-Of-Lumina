import pygame
from entities import Player, Umbral
from world import Room
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import HUD

class GameState:
    def __init__(self, state_manager):

        self.state_manager = state_manager
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        # Initialize player
        self.room = Room()
        self.player = Player(self.screen_width // 2, self.screen_height // 2, 2)  # Define player at screen center
        self.umbrals = pygame.sprite.Group()
        self.umbrals.add(
            Umbral(200, 200, 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            Umbral(300, 300, 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.hud = HUD(self.player, self.screen_width, self.screen_height)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        
    def update(self, delta_time):
        """Updates the game logic."""
        # Get key input
        keys_pressed = pygame.key.get_pressed()

        # Update player movement and animation
        self.umbrals.update(delta_time, self.player)
        self.player.update(keys_pressed, delta_time, SCREEN_WIDTH, SCREEN_HEIGHT, self.umbrals)


    def render(self, screen):
        """Renders the current game state."""
        screen.fill((0, 0, 0))  # Clear screen with black

        # Render the player
        self.room.draw(screen)
        self.player.draw(screen)
        self.umbrals.draw(screen)
        self.hud.draw(screen)
        
        pygame.display.flip()  # Swap buffers to update the screen