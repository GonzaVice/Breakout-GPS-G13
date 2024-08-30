import os
import json
import pygame
from settings import WIDTH

class LevelLoader:
    def __init__(self, filename=None):
        self.filename = "assets/levels/" + filename if filename else None
        self.bricks = []

    def load_level(self):
        """Loads the level as JSON data."""
        if not self.filename:
            print("Error: No filename provided.")
            return None

        try:
            with open(self.filename, 'r') as file:
                level_data = json.load(file)
                return level_data
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file {self.filename} could not be parsed.")
            return None

    def parse_level_data(self, level_data):
        """Parses JSON data into Brick objects."""
        self.bricks = []
        for brick_data in level_data.get("bricks", []):
            x = brick_data["x"]
            y = brick_data["y"]
            hit_points = brick_data["hit_points"]
            has_powerup = brick_data["has_powerup"]

            from brick import Brick  # Ensure this import works in your environment
            brick = Brick(x, y, hit_points, is_powerup_brick=has_powerup)
            self.bricks.append(brick)

    def get_bricks(self):
        return self.bricks

    def save_level(self, level_data, file_name):
        """Saves the level data to a JSON file."""
        file_name = file_name if file_name.endswith('.json') else f"{file_name}.json"
        file_path = "assets/levels/" + file_name
        level_data["level_name"] = file_name
        with open(file_path, 'w') as file:
            json.dump(level_data, file, indent=4)
        print(f"Level saved to {file_path}")
        return file_name


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


