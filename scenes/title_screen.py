import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TitleScreen:
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager
        self.background = pygame.image.load('assets/images/UI/title_screen.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)  # Default font for smaller text
        self.prompt_text = "Press Enter to Start"

    def handle_events(self, screen=None):
        """Handle key press events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state_manager.set_state("main_menu")  # Switch to the game state

    def update(self, delta_time):
        """Any logic that needs to be updated goes here."""
        pass  # No game logic to update on title screen

    def draw(self):
        """Draw the title screen and text."""
        self.screen.blit(self.background, (0, 0))
        text_surface = self.font.render(self.prompt_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
