import os

GAME_DIR = os.path.abspath(os.path.pardir)
IMAGE_DIR = os.path.abspath(os.path.join(GAME_DIR, "game", "images"))
LEVEL_DIR = os.path.abspath(os.path.join(GAME_DIR, "levels"))

ACTIONS = {
    0: "NOTHING",
    1: "MOVE_UP",
    2: "MOVE_DOWN",
    3: "MOVE_LEFT",
    4: "MOVE_RIGHT",
    5: "PUSH_UP",
    6: "PUSH_DOWN",
    7: "PUSH_LEFT",
    8: "PUSH_RIGHT"
}

# STATE_SPACE = numberOfFreeFields * (numberOfBoxes + 1 (Player))

REWARDS = {
    "MOVE": -.1,
    "BOX_OFF_TARGET": -1,
    "BOX_ON_TARGET": 10,
    "PUSH_TO_TARGET": 0.5,  # todo
    "PUSH": 0.1,
    "FINISH": 100,
    "BOX_LOCKED": -100,
    "INVALID": -10
}
