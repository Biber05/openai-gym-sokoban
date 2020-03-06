import os
import random

import gym
import numpy as np
import pandas as pd

from gym_sokoban.contants import REWARDS, GAME_DIR
from gym_sokoban.game.game_state import GameState
from gym_sokoban.game.level_selector import read_levels_from_file
from gym_sokoban.params import game_state_size, epsilon_decay, max_steps, epsilon_min, epsilon, alpha, gamma, \
    episodes


class Agent:
    def __init__(self, level_file, state_size=game_state_size,
                 eps=epsilon, eps_min=epsilon_min, eps_dec=epsilon_decay,
                 al=alpha, g=gamma, epi=episodes, steps=max_steps, rewards=REWARDS):

        self._epsilon = float(eps)
        self._epsilon_min = float(eps_min)
        self._epsilon_decay = float(eps_dec)
        self._alpha = float(al)
        self._gamma = float(g)
        self._episodes = int(epi)
        self._max_steps = int(steps)
        self.debug = False
        self.levels = read_levels_from_file(level_file)

        print("Start Training with {} different Levels, GameStateSize of {}x{} and the following parameters: \n"
              "_epsilon: {} \n"
              "epsilon_min: {} \n"
              "epsilon_decay: {} \n"
              "alpha: {} \n"
              "gamma {} \n"
              "over {} episodes with maximum of {} steps".format(len(self.levels), state_size, state_size,
                                                                 eps, eps_min, eps_dec,
                                                                 al, g, epi, steps))

        print(rewards)

        self._env = gym.make("Sokoban-v1", state_size=state_size, levels=self.levels, rewards=rewards)
        self._env.reset()

        # q-table size = matrix * number of elements possible
        self._action_table = np.zeros(self._env.action_space.n)
        self._table_filename = os.path.join(GAME_DIR, "q-table.csv")

        self._q_table = self._load_from_file()

    def train(self):
        for l in range(len(self.levels)):
            for i in range(self._episodes):
                state: GameState = self._env.reset()

                while state.steps <= self._max_steps:
                    q_state = state.get_q_state()

                    # initial action space per state
                    if q_state not in self._q_table.keys():
                        self._q_table[q_state] = self._action_table.copy()

                    if random.uniform(0, 1) < self._epsilon:
                        action = self._env.action_space.sample()  # Explore action space
                    else:
                        action = np.argmax(self._q_table[q_state])  # Exploit learned values

                    _, reward, done, info = self._env.step(action)
                    if self.debug:
                        print("{} - {} - {} ".format(reward, done, info))

                    # Calculation of q-value : see "Reinforcement Learning - Sutton"
                    old_value = self._q_table[q_state][action]
                    next_max = np.max(self._q_table[q_state])
                    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)

                    if self.debug:
                        print("action: {}, q_state: {}, q_value: {}".format(action, q_state, new_value))

                    self._q_table[q_state][action] = new_value
                if self.debug:
                    print(f"Episode: {i} finished")
            print(f"Level: {l + 1} finished")
            self._env.next_level()
            if l >= 99:
                break
        self._save_to_file()
        print("Training finished!")

    def evaluate(self):
        total_epochs, total_penalties = 0, 0
        import math
        test_episodes = math.floor(episodes / 5)

        for _ in range(test_episodes):
            self._env.current_level = random.randint(0, len(self.levels) - 1)
            state: GameState = self._env.reset()
            epochs, penalties, reward = 0, 0, 0

            done = False

            while not done:
                q_state = state.get_q_state()
                action = np.argmax(self._q_table[q_state])
                next_state, reward, done, info = self._env.step(action)
                if self.debug:
                    print("next_state: {}, reward: {}, done: {}, info: {}".format(next_state, reward, done, info))

                if reward == -10:
                    penalties += 1

                epochs += 1

            total_penalties += penalties
            total_epochs += epochs

        print(f"Results after {episodes} episodes:")
        print(f"Average timesteps per episode: {total_epochs / episodes}")
        print(f"Average penalties per episode: {total_penalties / episodes}")

    def _get_stage_key(self):
        level = self._env.state.level
        string = ""
        for i in range(len(level)):
            for j in range(len(level[0])):
                string += level[i][j]
        return string

    def _save_to_file(self):
        pd.DataFrame.from_dict(self._q_table, orient='index') \
            .to_csv(self._table_filename, header=False)
        print("Saved Q-Table to {}".format(self._table_filename))

    def _load_from_file(self):
        try:
            return pd.read_csv(self._table_filename, index_col=0) \
                .apply(lambda x: list([x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]]), axis=1) \
                .to_dict()
        except FileNotFoundError:
            return {}
