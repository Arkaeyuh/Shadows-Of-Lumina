import pygame
from core.state_manager import StateManager
from scenes.main_menu_state import MainMenuState
from scenes.game_state import GameState
from scenes.settings_state import SettingsState
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class Engine:
    def __init__(self, screen_width, screen_height, fps):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.fps = FPS
        self.clock = pygame.time.Clock()
        
        # Initialize Pygame display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("The Cursed Kingdom")
        
        # Initialize the state manager
        self.state_manager = StateManager()

        # Register states
        self.state_manager.add_state("main_menu", MainMenuState(self.state_manager))
        self.state_manager.add_state("game", GameState(self.state_manager))
        self.state_manager.add_state("settings", SettingsState(self.state_manager))
        
        # Set the initial state to main menu
        self.state_manager.set_state("main_menu")

    def run(self):
        while True:
            delta_time = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                self.state_manager.handle_events(event)
            
            self.state_manager.update(delta_time)
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.state_manager.render(self.screen)
            pygame.display.flip()