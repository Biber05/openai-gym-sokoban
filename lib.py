import os

BASE_URL = "/Users/philipp/Git/sokoban"

# data
DATA_DIR = os.path.join(BASE_URL, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "0_raw")

# gan
MODEL_DIR = os.path.join(BASE_URL, "model")

# gym
GAME_DIR = os.path.join(BASE_URL, "gym-sokoban", "gym_sokoban")
GAME_IMAGE_DIR = os.path.join(GAME_DIR, "logic", "images")

# test
TEST_DIR = os.path.join(BASE_URL, "test/")

# level
LEVEL_DIR = os.path.join(BASE_URL, "levels")
