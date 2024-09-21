class LightManager:
    def __init__(self, initial_energy):
        self.lumina_energy = initial_energy
        self.max_energy = initial_energy
        self.light_radius = 100  # Initial light radius
    
    def update(self, delta_time):
        # Decrease energy over time
        if self.lumina_energy > 0:
            self.lumina_energy -= delta_time * 0.1  # Energy drains slowly
    
    def increase_radius(self):
        if self.lumina_energy > 10:
            self.light_radius += 10
            self.lumina_energy -= 10
    
    def decrease_radius(self):
        if self.light_radius > 20:
            self.light_radius -= 10
    
    def draw_light(self, screen, player_position):
        # Draw light around the player
        pygame.draw.circle(screen, (255, 255, 200), player_position, self.light_radius)
