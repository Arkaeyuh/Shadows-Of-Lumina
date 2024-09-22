import pygame
import math

class LightSource:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def update(self, x, y):
        """Update the light position."""
        self.x = x
        self.y = y

    def create_light_surface(self):
        """Create a surface that represents the light, with a radial gradient."""
        light_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(light_surface, (255, 255, 255, 180), (self.radius, self.radius), self.radius)
        
        # Optionally add a gradient fade-out by drawing multiple circles with decreasing alpha
        for i in range(self.radius, 0, -5):
            alpha = int(255 * (i / self.radius))  # Gradually reduce the alpha
            pygame.draw.circle(light_surface, (255, 255, 255, alpha), (self.radius, self.radius), i)
        
        return light_surface

class LightManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lights = []  # List of light sources

        # Create a surface to draw the dark overlay and lights onto
        self.dark_surface = pygame.Surface((self.screen_width, self.screen_height))
        self.dark_surface.fill((0, 0, 0))  # Black color to darken the screen
        self.dark_surface.set_alpha(220)  # Adjust the alpha value to control how dark the overlay is

    def add_light_source(self, light):
        """Add a light source to the light manager."""
        self.lights.append(light)

    def update(self, player):
        """Update all light sources (if they move)."""
        # This is handled in the GameState class, but you can extend functionality here if needed.
        pass

    def draw(self, screen):
        """Draw the lights on the screen by applying a dark overlay and adding light sources."""

        # First, fill the dark surface to cover the entire screen
        self.dark_surface.fill((0, 0, 0))
        
        # Now, draw each light source with additive blending
        for light in self.lights:
            light_surface = light.create_light_surface()  # Create the light surface for each light
            # Use Pygame's blending mode to "add" light over the dark surface
            self.dark_surface.blit(light_surface, (light.x - light.radius, light.y - light.radius), special_flags=pygame.BLEND_ADD)

        # Finally, draw the dark surface with the lighting effects on top of the game screen
        screen.blit(self.dark_surface, (0, 0))
