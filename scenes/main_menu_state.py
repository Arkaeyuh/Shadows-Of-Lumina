import pygame
import sys

from config.settings import *

# Load necessary assets and sounds in the constructor
pygame.mixer.init()

class MainMenu:
    def __init__(self):
        self.options = ["New Game", "Continue", "Settings", "Exit"]
        self.selected_index = 0
        
        # Scale the title font dynamically based on screen width
        self.title_font_size = SCREEN_WIDTH // 15  # Make the title font relative to the screen width
        self.option_font_size = SCREEN_WIDTH // 40  # Adjust menu option font similarly

        self.title_font = pygame.font.SysFont('Arial', self.title_font_size)
        self.font = pygame.font.SysFont('Arial', self.option_font_size)

        # Load background image
        self.background_image = pygame.image.load('assets/images/star_background.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load sounds
        self.menu_sound = pygame.mixer.Sound('assets/audio/menu_select.mp3')
        self.menu_move_sound = pygame.mixer.Sound('assets/audio/menu_move.mp3')
        pygame.mixer.music.load('assets/audio/Hollow Knight OST - Title Theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

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

    def update_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.menu_move_sound.play()  # Play sound effect when moving through options
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.menu_move_sound.play()  # Play sound effect when moving through options

    def select_option(self):
        self.menu_sound.play()  # Play sound effect when selecting an option
        if self.selected_index == 0:
            return "new_game"
        elif self.selected_index == 1:
            return "continue"
        elif self.selected_index == 2:
            return "settings"
        elif self.selected_index == 3:
            return "exit"
            

class MainMenuState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.menu = MainMenu()  # Initialize the MainMenu
        print("MainMenuState initialized")  # Debugging output

    def handle_events(self, event):
        self.menu.update_selection(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            selection = self.menu.select_option()
            print(f"User selected: {selection}")  # Debugging output
            if selection == "new_game":
                print("Switching to 'game' state")  # Debugging output
                self.state_manager.set_state("game")  # Switch to GameState
            elif selection == "settings":
                print("Switching to 'settings' state")  # Debugging output
                self.state_manager.set_state("settings")  # Switch to SettingsState
            elif selection == "exit":
                pygame.quit()
                sys.exit()

    def update(self, delta_time):
        pass  # No need to update the main menu

    def render(self, screen):
        self.menu.draw(screen)