from gym_sokoban.game.game_constants import SYMBOL_NUMBER_MAPPING


def calc_distance(p1, p2):
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def calc_point(point, offset):
    import operator
    return tuple(map(operator.add, point, offset))


def calc_state(level: [[]], player_pos: tuple, state_size):
    import math
    import numpy as np

    offset = math.floor(state_size / 2)
    x, y = player_pos

    sub = np.array(level)
    # 3x3 matrix always possible due level design (walls)

    top_offset = 0 if not x - offset < 0 else abs(x - offset)
    bottom_offset = 0 if not x + offset > len(level) - 1 else (x + offset) - (len(level) - 1)
    left_offset = 0 if not y - offset < 0 else abs(y - offset)
    right_offset = 0 if not y + offset > len(level[0]) - 1 else (y + offset) - (len(level[0]) - 1)

    sub = sub[x - (offset - top_offset): x + (offset - bottom_offset + 1),
          y - (offset - left_offset): y + (offset - right_offset + 1)]

    return np.pad(sub, ((top_offset, bottom_offset), (left_offset, right_offset)), "constant", constant_values="#")


def get_q_state_as_numbers(level: [[]], player_pos: tuple, state_size=5):
    q_state = calc_state(level, player_pos, state_size).flatten()
    state_list = list(map(get_number_from_symbol, q_state))
    num = ""
    for i in state_list:
        num += str(i)
    return num


def get_number_from_symbol(symbol: str):
    return SYMBOL_NUMBER_MAPPING[symbol]
