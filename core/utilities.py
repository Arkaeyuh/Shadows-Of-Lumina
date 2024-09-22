import pygame
import os

def load_image(image_path):
    """Loads an image from the assets/images/ directory."""
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Error loading image: {image_path}\n{e}")
        return None

def load_sound(sound_path):
    """Loads a sound file from the assets/audio/ directory."""
    try:
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except pygame.error as e:
        print(f"Error loading sound: {sound_path}\n{e}")
        return None

def play_sound(sound, volume=1.0):
    """Plays a sound with a given volume."""
    if sound:
        sound.set_volume(volume)
        sound.play()

def clamp(value, min_value, max_value):
    """Clamps a value between a min and max value."""
    return max(min_value, min(value, max_value))
