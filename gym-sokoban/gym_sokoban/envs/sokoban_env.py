import gym
import numpy as np
from gym.spaces import Discrete, Box

from gym_sokoban.contants import ACTIONS, REWARDS
from gym_sokoban.game.game_constants import TILE_HEIGHT, TILE_WIDTH
from gym_sokoban.game.game_state import GameState
from gym_sokoban.game.rendering import im_show


# todo : maybe switch to GoalEnv @see gym.Env


class SokobanEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, state_size: int, levels: [[[]]], rewards=REWARDS):
        self.current_level = 0

        # init viewer
        from gym.envs.classic_control import rendering
        self.viewer = rendering.SimpleImageViewer()
        # init game
        self.game_state_size = state_size
        self.levels = levels
        self.state: GameState = self.reset()

        self.boxes_off_target, self.boxes_on_target = self.state.get_boxes_off_and_on_target()

        # setup spaces for q-learning
        self.action_space = Discrete(len(ACTIONS))
        screen_height, screen_width = (len(self.state.level) * TILE_WIDTH, len(self.state.level[0]) * TILE_HEIGHT)
        self.observation_space = Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)

        self.rewards = rewards

    def step(self, action: int):
        assert action in ACTIONS

        valid = self.state.make_move(action)

        reward = self._calc_reward(action, valid)

        is_done = self.state.is_finished()

        observation = self.render()

        info = {
            "action.name": ACTIONS[action],
            "player_position": self.state.player_pos,
            "step": self.state.steps
        }
        if is_done:
            info["steps_used"] = self.state.steps
            info["all_boxes_on_target"] = self.state.current_box_pos

        return observation, reward, is_done, info

    def reset(self):
        self.state = GameState(self.levels[self.current_level], self.game_state_size)
        return self.state

    def render(self, mode='human', close=False):
        im_show(self.viewer, self.state.level)
        return self.state.level

    def next_level(self):
        if self.current_level + 1 < len(self.levels):
            self.current_level += 1

    def _calc_reward(self, action: int, valid: bool):
        reward = 0
        reward += self.rewards["MOVE"]

        if action > 4 and valid:  # push
            off_target, on_target = self.state.get_boxes_off_and_on_target()

            blocked_boxes = self.state.get_blocked_boxes()
            reward += (self.rewards["BOX_LOCKED"] * blocked_boxes)

            reward += (self.rewards["BOX_OFF_TARGET"] * (self.boxes_off_target - off_target))
            reward += (self.rewards["BOX_ON_TARGET"] * (on_target - self.boxes_on_target))

            if on_target == self.state.number_of_boxes:
                reward += self.rewards["FINISH"]
        if not valid:
            # not supported step
            reward += self.rewards["INVALID"]
        return reward
