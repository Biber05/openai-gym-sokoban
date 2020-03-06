import imageio
import numpy as np

from gym_sokoban.game.game_constants import *

box = imageio.imread(BOX_IMG)
goal = imageio.imread(GOAL_IMG)
box_on_goal = imageio.imread(BOX_ON_GOAL_IMG)
floor = imageio.imread(FLOOR_IMG)
wall = imageio.imread(WALL_IMG)
player = imageio.imread(PLAYER_IMG)

mapping = {
    'box': box,
    'goal': goal,
    'box_on_goal': box_on_goal,
    'floor': floor,
    'wall': wall,
    'player': player,
}


def update_level(state, action):
    offset_row, offset_column = MOVEMENT[action] if action < 5 else MOVEMENT[action - 4]
    x, y = state.player_pos

    # move player
    state.level[x][y] = "@"

    # set old spot - could be al goal or floor
    if (x - offset_row, y - offset_column) in state.goal_box_pos:
        # player on goal before
        state.level[x - offset_row][y - offset_column] = "."
    else:
        # player on floor before:
        state.level[x - offset_row][y - offset_column] = " "

    # move box
    if action > 4:
        if (x + offset_row, y + offset_column) in state.goal_box_pos:
            # moved to goal
            state.level[x + offset_row][y + offset_column] = "*"
        else:
            # move over floor
            state.level[x + offset_row][y + offset_column] = "$"
        pass
    return state


def get_symbol(level, x, y):
    if level[x][y] == "#":
        return 'wall'
    elif level[x][y] == " ":
        return 'floor'
    elif level[x][y] == "@":
        return 'player'
    elif level[x][y] == "$":
        return 'box'
    elif level[x][y] == ".":
        return 'goal'
    elif level[x][y] == "*":
        return 'box_on_goal'


def read_level(level: [[]]):
    current_box_pos = []
    goal_box_pos = []
    player_pos = []
    for x in range(len(level)):
        for y in range(len(level[0])):
            if level[x][y] == SYMBOL_MAPPING['player']:
                player_pos.append((x, y))
            elif level[x][y] == SYMBOL_MAPPING['goal']:
                goal_box_pos.append((x, y))
            elif level[x][y] == SYMBOL_MAPPING['box']:
                current_box_pos.append((x, y))
            elif level[x][y] == SYMBOL_MAPPING['box_on_goal']:
                goal_box_pos.append((x, y))
                current_box_pos.append((x, y))
    return player_pos[0], current_box_pos, goal_box_pos


def get_positions_of_symbol(level: [[]], symbol: str):
    if symbol not in SYMBOLS:
        assert symbol not in SYMBOLS
    positions = []
    for x in range(level):
        for y in range(level[0]):
            if level[x][y] == symbol:
                positions.append((x, y))
    return positions


def create_img(level_data):
    # create image from level and tiles
    width = len(level_data)
    height = len(level_data[0])

    view = np.zeros(shape=(width * TILE_WIDTH, height * TILE_HEIGHT, 3), dtype=np.uint8)

    for i in range(width):
        x_i = i * TILE_WIDTH
        for j in range(height):
            y_j = j * TILE_HEIGHT
            symbol = get_symbol(level_data, i, j)
            img = mapping[symbol]
            if img.shape[2] == 4:
                img = img[:, :, 0:3]
            view[x_i:(x_i + TILE_WIDTH), y_j:(y_j + TILE_HEIGHT), :] = img

    return view


def im_show(viewer, level):
    img = create_img(level)
    viewer.imshow(img)


def print_level(level):
    [print(x) for x in level]
