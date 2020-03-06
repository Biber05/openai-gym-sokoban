epsilon = 0.7  # Greed 100%
epsilon_min = 0.005  # Minimum greed 0.05%
epsilon_decay = 0.99993  # Decay multiplied with epsilon after each episode
episodes = 20  # Amount of games
max_steps = 300  # Maximum steps per episode
alpha = 0.65
gamma = 0.65

action_size = 9  # /,r,l,o,u,R,L,O,U - capital letters for PUSHING BOX
field_size = 6  # wall, floor, player, box, box_on_target, box_off_target, goal
game_state_size = 5  # x^2 matrix around player
