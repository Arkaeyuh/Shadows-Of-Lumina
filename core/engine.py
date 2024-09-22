import pygame
from core.state_manager import StateManager
from scenes import MainMenuState
from scenes import GameState
from scenes import SettingsState
from scenes import PauseState
from scenes import DeathState
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
        self.state_manager.add_state("pause", PauseState(self.state_manager))  # Register pause state
        self.state_manager.add_state("death", DeathState(self.state_manager))
        # self.state_manager.add_state("titlescreen", TitleScreen(self.state_manager))
        
        # Set the initial state to main menu
        self.state_manager.set_state("main_menu")

    def run(self):
        while True:
            delta_time = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                # If the ESC key is pressed, switch to the pause menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state_manager.set_state("pause")
                    pygame.mixer.music.pause()
                    
                self.state_manager.handle_events(event)
            
            self.state_manager.update(delta_time)
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.state_manager.render(self.screen)
            pygame.display.flip()