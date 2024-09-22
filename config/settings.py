# Game configuration settings

# Screen dimensions
SCREEN_WIDTH = 1280 
SCREEN_HEIGHT = 720

# Frames per second
FPS = 60

# Sound settings
VOLUME_MUSIC = 0.7
VOLUME_SFX = 0.8

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
GOLD = (255, 215, 0)


sfx_volume = 0.5  # Default SFX volume

def get_sfx_volume():
    global sfx_volume
    return sfx_volume

def set_sfx_volume(volume):
    global sfx_volume
    sfx_volume = volume