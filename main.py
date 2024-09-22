import pygame
from core.engine import Engine
from config.settings import *

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create the game engine instance
    engine = Engine(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    
    # Start the main game loop
    engine.run()
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
