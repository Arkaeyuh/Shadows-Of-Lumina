import pygame

class HUD:
    def __init__(self, player, screen_width, screen_height) -> None:
        """Initialize the HUD with the player data."""

        self.player = player  # Reference to the player object
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Define bar dimensions and colors
        self.bar_width = 200
        self.bar_height = 20
        self.health_color = (255, 0, 0)  # Red for health
        self.lumina_color = (0, 0, 255)  # Blue for lumina
        self.border_color = (255, 255, 255)  # White border

        # Padding and positions
        self.padding = 10
        self.health_bar_pos = (self.padding, self.padding)
        self.lumina_bar_pos = (self.padding, self.padding + self.bar_height + self.padding)

    def draw_health_bar(self, screen) -> None:
        """Draw the health bar."""

        # Calculate health percentage
        health_percentage = self.player.health / 100
        current_health_width = self.bar_width * health_percentage

        # Draw health bar background (border)
        pygame.draw.rect(screen, self.border_color, (self.health_bar_pos[0], self.health_bar_pos[1], self.bar_width, self.bar_height), 2)

        # Draw the filled part of the health bar
        pygame.draw.rect(screen, self.health_color, (self.health_bar_pos[0], self.health_bar_pos[1], current_health_width, self.bar_height))

    def draw_lumina_bar(self, screen) -> None:
        """Draw the lumina energy bar."""

        # Calculate lumina percentage
        lumina_percentage = self.player.lumina_energy / 100
        current_lumina_width = self.bar_width * lumina_percentage

        # Draw lumina bar background (border)
        pygame.draw.rect(screen, self.border_color, (self.lumina_bar_pos[0], self.lumina_bar_pos[1], self.bar_width, self.bar_height), 2)

        # Draw the filled part of the lumina energy bar
        pygame.draw.rect(screen, self.lumina_color, (self.lumina_bar_pos[0], self.lumina_bar_pos[1], current_lumina_width, self.bar_height))

    def draw(self, screen) -> None:
        """Draw all elements of the HUD."""
        
        self.draw_health_bar(screen)
        self.draw_lumina_bar(screen)
