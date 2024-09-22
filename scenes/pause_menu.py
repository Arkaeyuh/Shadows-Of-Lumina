import pygame
from config.settings import SCREEN_WIDTH
from config.settings import *

import sys
from scenes.game_state import GameState

import os
# Get the directory of the current file (main.py is inside ProjectRoot)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one folder up (out of ProjectRoot)
PARENT_DIR = os.path.dirname(BASE_DIR)

# Now construct the path to the assets/images folder
ASSETS_DIR = os.path.join(PARENT_DIR, 'assets')

class PauseMenu:
    def __init__(self):
        self.options = ["Resume", "Restart", "Main Menu", "Exit"]
        self.menu_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_select.mp3')
        self.menu_move_sound = pygame.mixer.Sound(ASSETS_DIR + '/audio/menu_move.mp3')
        self.update_sfx_volume()

        self.option_font_size = 1280 // 40
        self.title_font_size = 1280 // 15
        self.selected_index = 0
        self.font = pygame.font.Font(ASSETS_DIR + '/images/Rusillaserif-Regular.ttf', self.option_font_size)
        self.title_font = pygame.font.Font(ASSETS_DIR + '/images/Rusillaserif-Regular.ttf', self.title_font_size)
        # Define option_font_size to fix the error
      # You can adjust this value based on your screen size

    def draw(self, screen):
        # Draw background image
        screen.fill((0, 0, 0))
                # Draw the title
        title_text = self.title_font.render("Paused", True, (255, 255, 255))
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
                self.menu_move_sound.play()
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.menu_move_sound.play()

    def select_option(self):
        self.update_sfx_volume()  # Ensure the correct volume is applied
        self.menu_sound.play()
        if self.selected_index == 0:
            return "resume"
        elif self.selected_index == 1:
            return "restart"
        elif self.selected_index == 2:
            return "main_menu"
        elif self.selected_index == 3:
            return "exit"



# SATTE 

class PauseState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.pause_menu = PauseMenu()

    def handle_events(self, event):
        self.pause_menu.update_selection(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            selected_option = self.pause_menu.select_option()

            if selected_option == "resume":
                print("Resuming game...")
                pygame.mixer.music.unpause()  # Unpause music when resuming the game
                self.state_manager.set_state("game")  # Resume the game

            elif selected_option == "restart":
                print("Restarting game...")
                new_game_state = GameState(self.state_manager)
                self.state_manager.add_state("game", new_game_state)
                self.state_manager.set_state("game")

            elif selected_option == "main_menu":
                print("Returning to Main Menu...")
                pygame.mixer.music.stop()  # Stop the game music

                # Load and play the main menu music
                try:
                    pygame.mixer.music.load(ASSETS_DIR + '/audio/Hollow Knight OST - Title Theme.mp3')  # Replace with menu music
                    pygame.mixer.music.play(-1)  # Loop the main menu music
                except pygame.error as e:
                    print(f"Error loading main menu music: {e}")

                self.state_manager.set_state("main_menu") 

            elif selected_option == "exit":
                print("Exiting game...")
                pygame.quit()
                sys.exit()

    def update(self, delta_time):
        pass  # No dynamic updates needed for the pause state

    def render(self, screen):
        self.pause_menu.draw(screen)