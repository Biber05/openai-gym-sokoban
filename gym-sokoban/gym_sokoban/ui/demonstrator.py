from tkinter import *
from tkinter import filedialog

from gym_sokoban.agent import Agent
from gym_sokoban.contants import REWARDS, LEVEL_DIR
from gym_sokoban.params import *
from gym_sokoban.ui.helpers import *
from gym_sokoban.ui.params import *


class Demonstrator:
    def __init__(self):
        # build window
        self.window = Tk()
        self.window.title("Sokoban Q-Learning")

        # Training options
        self.epsilon = StringVar()
        self.epsilon_min = StringVar()
        self.epsilon_decay = StringVar()
        self.episodes = StringVar()
        self.max_steps = StringVar()
        self.alpha = StringVar()
        self.gamma = StringVar()
        self.state_size = StringVar()

        # Rewards
        self.move = StringVar()
        self.box_off = StringVar()
        self.box_on = StringVar()
        self.push = StringVar()
        self.finish = StringVar()
        self.locked = StringVar()
        self.invalid = StringVar()

        self.level_file = None

        self.load_default()

        self.training_parameters = {
            "Epsilon": self.epsilon,
            "Epsilon Minimum": self.epsilon_min,
            "Epsilon Decay": self.epsilon_decay,
            "Episodes": self.episodes,
            "Maximum Steps": self.max_steps,
            "Alpha": self.alpha,
            "Gamma": self.gamma,
            "Game State Size": self.state_size
        }

        self.create_params(self.training_parameters)

        self.reward_params = {
            "MOVE": self.move,
            "BOX_OFF_TARGET": self.box_off,
            "BOX_ON_TARGET": self.box_on,
            "PUSH": self.push,
            "FINISH": self.finish,
            "LOCKED": self.locked,
            "INVALID STEP": self.invalid
        }

        self.create_params(self.reward_params, 2)

        create_button(self.window, "Select Level", 2, 9, self.read_level)
        create_button(self.window, "Load Defaults", 3, 9, self.load_default)
        create_button(self.window, "Start", 2, 10, self.start_with_parameter)

        self.window.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.window.mainloop()

    def create_header(self):
        create_text_field(self.window, "Sokoban Q-Learning Demonstrator", 0, 0, font=("Arial Bold", 30))
        create_text_field(self.window, "Add parameter for q-learning here:", 0, 1)

    def create_params(self, params: dict, offset=0):
        i = 2
        for k, v in params.items():
            create_text_field(self.window, k, offset, i)
            create_text_input(self.window, offset + 1, i, v)
            i += 1

    def start_with_parameter(self):
        rewards = {
            "MOVE": float(self.move.get()),
            "BOX_OFF_TARGET": float(self.box_off.get()),
            "BOX_ON_TARGET": float(self.box_on.get()),
            "PUSH_TO_TARGET": float(REWARDS["PUSH_TO_TARGET"]),
            "PUSH": float(self.push.get()),
            "FINISH": float(self.finish.get()),
            "BOX_LOCKED": float(self.locked.get()),
            "INVALID": float(self.invalid.get())
        }

        agent = Agent(
            state_size=int(self.state_size.get()),
            eps=float(self.epsilon.get()),
            eps_min=float(self.epsilon_min.get()),
            eps_dec=float(self.epsilon_decay.get()),
            al=float(self.alpha.get()),
            g=float(self.gamma.get()),
            epi=int(self.episodes.get()),
            steps=int(self.max_steps.get()),
            rewards=rewards,
            level_file=self.level_file)

        agent.train()
        self.window.destroy()

    def load_default(self):
        # training defaults
        self.epsilon.set(epsilon)
        self.epsilon_min.set(epsilon_min)
        self.epsilon_decay.set(epsilon_decay)
        self.episodes.set(episodes)
        self.max_steps.set(max_steps)
        self.alpha.set(alpha)
        self.gamma.set(gamma)
        self.state_size.set(game_state_size)

        # reward default
        self.move.set(REWARDS["MOVE"])
        self.box_off.set(REWARDS["BOX_OFF_TARGET"])
        self.box_on.set(REWARDS["BOX_ON_TARGET"])
        self.push.set(REWARDS["PUSH"])
        self.finish.set(REWARDS["FINISH"])
        self.locked.set(REWARDS["BOX_LOCKED"])
        self.invalid.set(REWARDS["INVALID"])

        # level default
        import os
        self.level_file = os.path.join(LEVEL_DIR, "test_levels.txt")

        self.window.update()

    def read_level(self):
        file = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.level_file = file

        txt = ""
        with open(file, "r") as f:
            txt += f.read()

        create_text_field(self.window, txt, 2, 11)


if __name__ == '__main__':
    app = Demonstrator()
