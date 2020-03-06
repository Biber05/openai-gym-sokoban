import os
import sys

import pygame

from gym_sokoban.contants import LEVEL_DIR
from gym_sokoban.envs import SokobanEnv
from gym_sokoban.game.level_selector import read_levels_from_file
from gym_sokoban.params import game_state_size


def play():
    env = SokobanEnv(game_state_size, read_levels_from_file(os.path.join(LEVEL_DIR, "test_levels.txt")))

    pygame.init()

    env.reset()
    env.render()

    while True:
        action = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    action = 3
                elif event.key == pygame.K_RIGHT:
                    action = 4
                elif event.key == pygame.K_UP:
                    action = 1
                elif event.key == pygame.K_DOWN:
                    action = 2
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not env.state.is_finished() and action > 0:
            if env.state.is_box_in_front(action):
                action += 4

            state, reward, done, info = env.step(action)
            print("{} - {} - {} ".format(reward, done, info))

            if done:
                if env.current_level < len(env.levels):
                    env.next_level()
                    env.reset()
                else:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    play()
