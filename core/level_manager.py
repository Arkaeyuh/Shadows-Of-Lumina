import json
import os

class LevelManager:
    def __init__(self, base_level_path):
        """Initializes the level manager with a path to the level files."""
        self.base_level_path = base_level_path
        self.current_level_data = None
        self.current_level_index = 0

    def load_level(self, level_name):
        """Loads a level from a JSON file."""
        level_path = os.path.join(self.base_level_path, f"{level_name}.json")
        try:
            with open(level_path, 'r') as f:
                self.current_level_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Level file {level_name}.json not found!")

    def get_current_level(self):
        """Returns the current level data."""
        return self.current_level_data

    def next_level(self):
        """Loads the next level based on index."""
        self.current_level_index += 1
        self.load_level(f"level_{self.current_level_index}")

    def reset_levels(self):
        """Resets back to the first level."""
        self.current_level_index = 0
        self.load_level(f"level_{self.current_level_index}")
