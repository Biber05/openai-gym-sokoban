import os

from gym_sokoban.contants import IMAGE_DIR

FPS = 30  # frames per second to update the screen
WIN_WIDTH = 600  # width of the program's window, in pixels
WIN_HEIGHT = 450  # height in pixels
HALF_WIN_WIDTH = int(WIN_WIDTH / 2)
HALF_WIN_HEIGHT = int(WIN_HEIGHT / 2)

# The total width and height of each tile in pixels.
TILE_WIDTH = 32
TILE_HEIGHT = 32
TILE_FLOOR_HEIGHT = 32

CAM_MOVE_SPEED = 5  # how many pixels per frame the camera moves

# The percentage of outdoor tiles that have additional
# decoration on them, such as al tree or rock.
OUTSIDE_DECORATION_PCT = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = BLACK
TEXT_COLOR = WHITE

# Movements of player

MOVEMENT = {
    # (row | column)
    0: (0, 0),  # nothing
    1: (-1, 0),  # up
    2: (1, 0),  # down
    3: (0, -1),  # left
    4: (0, 1)  # right
}

# Images

BOX_IMG = os.path.join(IMAGE_DIR, "box.png")
GOAL_IMG = os.path.join(IMAGE_DIR, "dock.png")
BOX_ON_GOAL_IMG = os.path.join(IMAGE_DIR, "box_docked.png")
FLOOR_IMG = os.path.join(IMAGE_DIR, "floor.png")
WALL_IMG = os.path.join(IMAGE_DIR, "wall_uni.png")
PLAYER_IMG = os.path.join(IMAGE_DIR, "player.png")

SYMBOLS = ['#', ' ', '@', '.', '$', '*']

SYMBOL_MAPPING = {
    'wall': '#',
    'floor': ' ',
    'player': '@',
    'goal': '.',
    'box': '$',
    'box_on_goal': '*'
}

SYMBOL_NUMBER_MAPPING = {
    '#': 1,
    ' ': 2,
    '@': 3,
    '.': 4,
    '$': 5,
    '*': 6,
}
