import pygame
import sys
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.game_state import GameState
import os

# Setup asset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

class WinState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.options = ["New Game", "Main Menu", "Exit"]
        self.selected_index = 0
        self.option_font_size = SCREEN_WIDTH // 40
        self.title_font_size = SCREEN_WIDTH // 15

        # Load fonts
        self.font = pygame.font.Font(ASSETS_DIR + '/images/Rusillaserif-Regular.ttf', self.option_font_size)
        self.title_font = pygame.font.Font(ASSETS_DIR + '/images/Rusillaserif-Regular.ttf', self.title_font_size)

        # Load sound effects
        self.menu_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_select.mp3')
        self.menu_move_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_move.mp3')

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.menu_move_sound.play()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.menu_move_sound.play()

            if event.key == pygame.K_RETURN:
                selected_option = self.options[self.selected_index]

                if selected_option == "New Game":
                    print("Starting new game...")
                    new_game_state = GameState(self.state_manager)
                    self.state_manager.add_state("game", new_game_state)
                    self.state_manager.set_state("game")

                elif selected_option == "Main Menu":
                    print("Returning to Main Menu...")
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(ASSETS_DIR + '/audio/Hollow Knight OST - Title Theme.mp3')  # Menu music
                    pygame.mixer.music.play(-1)
                    self.state_manager.set_state("main_menu")

                elif selected_option == "Exit":
                    print("Exiting game...")
                    pygame.quit()
                    sys.exit()

    def update(self, delta_time):
        pass  # No updates needed for the win screen

    def render(self, screen):
        # Draw background image or just fill it with a color
        screen.fill((0, 0, 0))

        # Custom color for "You Won" text
        win_color = (0, 255, 0)  # Green color for victory

        # Draw the title with the chosen color
        title_text = self.title_font.render("You Won!", True, win_color)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT * 0.2))

        # Menu option Y-position starts at about 60% of the screen height
        start_y = SCREEN_HEIGHT * 0.6
        option_spacing = self.option_font_size * 1.5  # Dynamically space the menu options

        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (200, 200, 200)
            text = self.font.render(option, True, color)

            # Center the menu options
            text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
            text_y = start_y + i * option_spacing

            # Draw the arrows around the selected option
            if i == self.selected_index:
                arrow = self.font.render("<>", True, (255, 255, 255))
                screen.blit(arrow, (text_x - 60, text_y))
                screen.blit(arrow, (text_x + text.get_width() + 20, text_y))

            screen.blit(text, (text_x, text_y))
