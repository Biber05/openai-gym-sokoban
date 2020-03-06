import math
import time

import numpy as np

from gym_sokoban.game.game_constants import MOVEMENT
from gym_sokoban.game.helpers import calc_distance, calc_point, calc_state
from gym_sokoban.game.rendering import update_level, read_level, im_show
from gym_sokoban.levels.test_ui_level import test_update_level


class GameState:
    def __init__(self, level_map: [[]], game_state_size: int):
        self.level = np.array(level_map, copy=True)
        self.player_pos, self.current_box_pos, self.goal_box_pos = read_level(self.level)
        self.number_of_boxes = len(self.goal_box_pos)
        self.steps = 0
        self.state_size = game_state_size

    def make_move(self, action):
        self._step()
        if action == 0:
            return False
        else:
            offset = MOVEMENT[action] if action < 5 else MOVEMENT[action - 4]
            position = calc_point(self.player_pos, offset)

            has_moved = False
            has_pushed = False

            if action < 5:
                has_moved = self._move(position)

            elif action < 9:
                has_pushed = self._push(position, action - 4)

            if has_pushed or has_moved:
                self.player_pos = position
                update_level(self, action)
                return True

            return False

    def _move(self, point):
        if self._is_blocked(point):
            return False

        return True

    def _push(self, point, action):
        offset = MOVEMENT[action]
        if self._is_pushable(action):
            # move box
            box_index = self.current_box_pos.index(point)
            self.current_box_pos[box_index] = calc_point(point, offset)
            return True
        return False

    def _step(self):
        self.steps += 1

    def _is_wall(self, point):
        x, y = point
        if self._is_outside_level(point):
            return False
        elif self.level[x][y] == '#':
            return True
        return False

    def _is_blocked(self, point):
        if self._is_wall(point):
            return True

        elif self._is_outside_level(point):
            return True

        elif point in self.current_box_pos:
            return True

        return False

    def _is_outside_level(self, point):
        x, y = point
        if x < 0 or x > len(self.level) or y < 0 or y > len(self.level[x]):
            assert "Coordinates outside of level"
            return True
        return False

    def _is_pushable(self, action):
        player_row, player_column = self.player_pos
        offset_row, offset_column = MOVEMENT[action]

        x = player_row + offset_row
        y = player_column + offset_column

        # Player is not blocked by wall
        if not self._is_wall((x, y)) and not self._is_outside_level((x, y)):
            # is there a box
            if (x, y) in self.current_box_pos:
                # Box is not blocked by another box or wall or outside level
                if not self._is_blocked((x + offset_row, y + offset_column)):
                    return True

        return False

    def is_finished(self):
        if self.get_blocked_boxes() > 0:
            return True

        for box in self.current_box_pos:
            if box not in self.goal_box_pos:
                return False

        return True

    def is_box_in_front(self, action):
        player_row, player_column = self.player_pos
        offset_row, offset_column = MOVEMENT[action]

        return (player_row + offset_row, player_column + offset_column) in self.current_box_pos

    def get_boxes_off_and_on_target(self):
        off_target = 0
        on_target = 0
        for (x, y) in self.current_box_pos:
            if (x, y) in self.goal_box_pos:
                on_target += 1
            else:
                off_target += 1

        return off_target, on_target

    def get_blocked_boxes(self):
        blocked_boxes = 0
        for box in self.current_box_pos:
            for i in (1, 2):
                for j in (3, 4):
                    i_offset = MOVEMENT[i]
                    j_offset = MOVEMENT[j]
                    if self._is_wall(calc_point(box, i_offset)) \
                            and self._is_wall(calc_point(box, j_offset)) \
                            and box not in self.goal_box_pos:
                        blocked_boxes += 1
        return blocked_boxes

    def calc_box_diff_to_goal(self, box):
        min_dist = math.inf
        for goal in self.goal_box_pos:
            dist = calc_distance(box, goal)
            min_dist = dist if dist < min_dist else min_dist
        return min_dist

    def get_q_state(self):
        return "".join(calc_state(self.level, self.player_pos, self.state_size).flatten())