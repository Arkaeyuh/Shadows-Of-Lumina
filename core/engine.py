import pygame
from core.state_manager import StateManager
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Engine:
    def __init__(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, fps=FPS):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.clock = pygame.time.Clock()
        
        # Initialize Pygame display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("The Cursed Kingdom: Shadows of Lumina")
        
        # Initialize the state manager
        self.state_manager = StateManager()
        self.is_running = True

    def handle_events(self):
        """Handles events like input, mouse, etc."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            self.state_manager.handle_events(event)

    def update(self, delta_time):
        """Updates the game logic."""
        self.state_manager.update(delta_time)

    def render(self):
        """Renders the current game state."""
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.state_manager.render(self.screen)
        pygame.display.flip()  # Swap buffers to update the screen

    def run(self):
        """Main game loop."""
        while self.is_running:
            delta_time = self.clock.tick(self.fps) / 1000  # Calculate frame time
            self.handle_events()
            self.update(delta_time)
            self.render()

        pygame.quit()

