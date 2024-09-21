import pygame
from config.settings import *

class SettingsMenu:
    def __init__(self):
        self.options = ["Music Volume", "SFX Volume", "Back"]
        self.selected_index = 0
        
        # Scale the fonts dynamically based on screen width
        self.title_font_size = SCREEN_WIDTH // 15  # Title font size relative to screen width
        self.option_font_size = SCREEN_WIDTH // 40  # Option font size relative to screen width

        self.title_font = pygame.font.SysFont('Arial', self.title_font_size)
        self.font = pygame.font.SysFont('Arial', self.option_font_size)

        self.music_volume = pygame.mixer.music.get_volume()
        self.sfx_volume = pygame.mixer.Sound('assets/audio/menu_select.mp3').get_volume()
        self.menu_sound = pygame.mixer.Sound('assets/audio/menu_select.mp3')
        self.menu_move_sound = pygame.mixer.Sound('assets/audio/menu_move.mp3')

    def draw(self, screen):
        # Background fill (you can add an image as well)
        screen.fill((0, 0, 0))

        # Draw the title, with dynamic font size and positioning
        title_text = self.title_font.render("Settings", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT * 0.2))

        # Start Y position and spacing, adjusted dynamically
        start_y = SCREEN_HEIGHT * 0.5
        option_spacing = self.option_font_size * 1.5  # Dynamic option spacing

        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (200, 200, 200)
            text = self.font.render(option, True, color)

            # Position menu text dynamically based on screen size
            text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
            text_y = start_y + i * option_spacing

            # Draw the volume sliders for Music and SFX
            if option == "Music Volume":
                volume_bar = self.draw_volume_bar(self.music_volume)
                screen.blit(volume_bar, (text_x + 300, text_y))
            elif option == "SFX Volume":
                volume_bar = self.draw_volume_bar(self.sfx_volume)
                screen.blit(volume_bar, (text_x + 300, text_y))

            screen.blit(text, (text_x, text_y))

    def draw_volume_bar(self, volume):
        """Creates a simple volume bar image based on volume level."""
        # Volume bar size scales with the screen width for better visibility
        volume_bar_width = SCREEN_WIDTH // 8
        volume_bar_height = SCREEN_HEIGHT // 30

        volume_bar = pygame.Surface((volume_bar_width, volume_bar_height))
        volume_bar.fill((200, 200, 200))

        # Fill part of the bar based on volume
        filled_width = int(volume * volume_bar_width)
        filled_bar = pygame.Surface((filled_width, volume_bar_height))
        filled_bar.fill((255, 255, 0))

        volume_bar.blit(filled_bar, (0, 0))
        return volume_bar

    def update_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.menu_move_sound.play()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.menu_move_sound.play()

            if event.key == pygame.K_LEFT:
                if self.selected_index == 0:
                    self.music_volume = max(0, self.music_volume - 0.1)
                    pygame.mixer.music.set_volume(self.music_volume)
                elif self.selected_index == 1:
                    self.sfx_volume = max(0, self.sfx_volume - 0.1)
                    self.menu_sound.set_volume(self.sfx_volume)

            if event.key == pygame.K_RIGHT:
                if self.selected_index == 0:
                    self.music_volume = min(1, self.music_volume + 0.1)
                    pygame.mixer.music.set_volume(self.music_volume)
                elif self.selected_index == 1:
                    self.sfx_volume = min(1, self.sfx_volume + 0.1)
                    self.menu_sound.set_volume(self.sfx_volume)

    def select_option(self):
        """Return the option the player has selected."""
        self.menu_sound.play()
        if self.selected_index == 2:  # "Back" option
            return "back"


#                   STATE

class SettingsState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.settings_menu = SettingsMenu()

    def handle_events(self, event):
        self.settings_menu.update_selection(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.settings_menu.select_option() == "back":
                self.state_manager.set_state("main_menu")

    def update(self, delta_time):
        pass  # No need for dynamic updates here

    def render(self, screen):
        self.settings_menu.draw(screen)