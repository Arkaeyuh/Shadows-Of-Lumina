import pygame

class MainMenu:
    def __init__(self):
        self.options = ["New Game", "Continue", "Settings", "Exit"]
        self.selected_index = 0

    def draw(self, screen, font):
        screen.fill((0, 0, 0))  # Background color
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (200, 200, 200)
            text = font.render(option, True, color)
            screen.blit(text, (400, 300 + i * 50))
    
    def update_selection(self, keys_pressed):
        if keys_pressed[pygame.K_DOWN]:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        if keys_pressed[pygame.K_UP]:
            self.selected_index = (self.selected_index - 1) % len(self.options)
    
    def select_option(self):
        if self.selected_index == 0:
            return "new_game"
        elif self.selected_index == 1:
            return "continue"
        elif self.selected_index == 2:
            return "settings"
        elif self.selected_index == 3:
            return "exit"
