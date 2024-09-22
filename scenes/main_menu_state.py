import pygame
import sys
import os

# Get the directory of the current file (main.py is inside ProjectRoot)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one folder up (out of ProjectRoot)
PARENT_DIR = os.path.dirname(BASE_DIR)

# Now construct the path to the assets/images folder
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

# Example of loading the image

from config.settings import *
from scenes.game_state import GameState

# Load necessary assets and sounds in the constructor
pygame.mixer.init()

class MainMenu:
    def __init__(self):
        self.options = ["New Game", "Settings", "Exit"]
        self.selected_index = 0
        
        # Scale the title font dynamically based on screen width
        self.title_font_size = SCREEN_WIDTH // 15  # Make the title font relative to the screen width
        self.option_font_size = SCREEN_WIDTH // 40  # Adjust menu option font similarly

        try:
            self.title_font = pygame.font.Font('assets/images/Rusillaserif-Regular.ttf', self.title_font_size)
            self.font = pygame.font.Font('assets/images/Rusillaserif-Regular.ttf', self.option_font_size)
        except FileNotFoundError:
            # Fallback to default font if custom font is not found
            print("Custom font not found, using default font.")
            self.title_font = pygame.font.SysFont('Arial', self.title_font_size)
            self.font = pygame.font.SysFont('Arial', self.option_font_size)

        # Load background image
        self.background_image = pygame.image.load(ASSETS_DIR + '/images/star_background.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load sounds (effects only)
        self.menu_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_select.mp3')
        self.menu_move_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_move.mp3')
        self.update_sfx_volume()


    def draw(self, screen):
        # Draw background image
        screen.blit(self.background_image, (0, 0))

        # Draw game title near the top, now dynamically scaled
        title_text = self.title_font.render("The Cursed Kingdom", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT * 0.2))

        # Menu option Y-position starts at about 60% of the screen height and moves downwards
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

    def update_sfx_volume(self):
        """Ensure that all sounds use the global SFX volume."""
        self.menu_sound.set_volume(get_sfx_volume())
        self.menu_move_sound.set_volume(get_sfx_volume())

    def update_selection(self, event):
        self.update_sfx_volume()  # Ensure the correct volume is applied
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.menu_move_sound.play()  # Play sound effect when moving through options
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.menu_move_sound.play()  # Play sound effect when moving through options

    def select_option(self):
        self.update_sfx_volume()  # Ensure the correct volume is applied
        self.menu_sound.play()  # Play sound effect when selecting an option
        if self.selected_index == 0:
            return "new_game"
        elif self.selected_index == 1:
            return "settings"
        elif self.selected_index == 2:
            return "exit"

class MainMenuState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.menu = MainMenu()

        # Load and play the main menu music here, AFTER initializing the menu
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(ASSETS_DIR + '/audio/Hollow Knight OST - Title Theme.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop the menu music
        except pygame.error as e:
            print(f"Error loading music: {e}")

    def handle_events(self, event):
        self.menu.update_selection(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            selection = self.menu.select_option()

            if selection == "new_game":
                print("Starting new game...")
                new_game_state = GameState(self.state_manager)
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load(ASSETS_DIR + '/audio/kingdomedgeost.mp3')  # Replace with game music
                    pygame.mixer.music.play(-1)
                except pygame.error as e:
                    print(f"Error loading game music: {e}")

                self.state_manager.add_state("game", new_game_state)
                self.state_manager.set_state("game")

            elif selection == "settings":
                print("Opening settings menu...")  # Debug print
                self.state_manager.set_state("settings")  # Transition to SettingsState

            elif selection == "exit":
                pygame.quit()
                sys.exit()

    def update(self, delta_time):
        pass

    def render(self, screen):
        self.menu.draw(screen)