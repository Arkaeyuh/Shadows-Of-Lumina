from config.settings import SCREEN_WIDTH,SCREEN_HEIGHT
import pygame
class Room:
    def __init__(self, SCREEN_WIDTH = SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_HEIGHT,pos=(0, 0)):
        """
        Initializes a Room object.
        
        :param width: Width of the room in pixels.
        :param height: Height of the room in pixels.
        :param color: Background color of the room. Default is a grey color.
        :param pos: Position of the room in the world (top-left corner). Default is (0, 0).
        """
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.pos = pos
         # Load the background image from the given path
        self.background_image = pygame.image.load('assets/world/test.png')
        
        # Optionally scale the image to fit the room size
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    def draw(self, screen):
        """
        Draws the room on the provided screen.
        
        :param screen: The surface (usually the game screen) where the room will be drawn.
        """
        screen.blit(self.background_image,self.pos)