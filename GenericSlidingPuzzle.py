import numpy as np
import random 
from collections import defaultdict
import math

FILE_NAME = "./Backup/q_values3.txt"

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

ACTIONS = [UP, RIGHT, DOWN, LEFT]

# default dimensions for puzzle
ROWS = 3
COLUMNS = 3

# to shuffle the puzzle in the .reset() function
MIN_SHUFFLE = 70
MAX_SHUFFLE = 100

# indexes for the rewards array
WIN = 0
PLAYING = 1
WRONG_MOVE = 2

REWARDS = [5, -1, -10]

def load_states(file_name=FILE_NAME):
    file = open(file_name, 'r')
    states = []

    for line in file:
        if line.startswith("TOTAL"):
            break
        else:
            state = line.split(":")[0]
            states.append(get_state(state))
    
    return states

class Puzzle:
    def __init__(self, rows=ROWS, columns=COLUMNS, min_shuffle=MIN_SHUFFLE, max_shuffle=MAX_SHUFFLE, preload_states=False):
        self.rows = rows
        self.columns = columns
        self.state = np.zeros((self.rows, self.columns))
        self.target = self.initialize_target()
        self.action_dim = len(ACTIONS)
        self.rewards = REWARDS
        self.counter = 0
        self.preload_states = preload_states
        self.states = load_states()
    
    # 
    # .sample() returns a random action feasible for the current state
    #
    def sample(self):
        return random.choice(ACTIONS)


    #
    # .reset() returns a random feasible starting state
    #       for a new episode
    #
    def reset(self):
        if self.rows == ROWS and self.columns == COLUMNS and self.preload_states:
            self.state = copy_matrix(random.choice(self.states), self.state)
        else:
            temp = copy_matrix(self.target, np.zeros((self.rows, self.columns)))

            for i in range(MIN_SHUFFLE, MAX_SHUFFLE):
                action = random.choice(ACTIONS)
                self.simulate_action(temp, action)
            
            self.state = copy_matrix(temp, self.state)
    

    #
    # .step(action) executes an action (if feasible) and returns the tuple
    #       (next_state, reward, done)
    #
    def step(self, action):
        previous_state = copy_matrix(self.state, np.zeros((self.rows, self.columns)))
        self.simulate_action(self.state, action)
        
        reward = self.get_reward(previous_state, self.state)

        done = False
        if reward == REWARDS[WIN]:
            done = True

        return (self.state, reward, done)

    #
    # UTILITY 
    #     
    def initialize_target(self):
        temp = np.zeros((self.rows, self.columns))
        number = 0
        for row in range(self.rows):
            for column in range(self.columns):
                temp[row][column] = number
                number += 1
            
        return temp

    def simulate_action(self, state, action):
        row_blank, col_blank = self.get_blank_tile_position(state)

        if action == UP and row_blank > 0:
            state[row_blank][col_blank] = state[row_blank-1][col_blank]
            state[row_blank-1][col_blank] = self.rows * self.columns - 1
        elif action == DOWN and row_blank < self.rows - 1:
            state[row_blank][col_blank] = state[row_blank+1][col_blank]
            state[row_blank+1][col_blank] = self.rows * self.columns - 1
        elif action == LEFT and col_blank > 0:
            state[row_blank][col_blank] = state[row_blank][col_blank-1]
            state[row_blank][col_blank-1] = self.rows * self.columns - 1
        elif action == RIGHT and col_blank < self.columns - 1:
            state[row_blank][col_blank] = state[row_blank][col_blank+1]
            state[row_blank][col_blank+1] = self.rows * self.columns - 1

        return state
    
    def gameover(self, state):
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] != self.target[i][j]:
                    return False

        return True
    
    def get_blank_tile_position(self, state):
        for row in range(len(state)):
            for col in range(len(state)):
                if state[row][col] == self.rows * self.columns - 1:
                    return row, col
    
    def get_reward(self, previous_state, next_state):
        if compare_matrix(previous_state, next_state) == 0:
            return self.rewards[WRONG_MOVE]
        else:
            if self.gameover(next_state):
                return self.rewards[WIN]
            else:
                return self.rewards[PLAYING]

# 
# copy_matrix(m1, m2) copies matrix m1 into matrix m2
#
def copy_matrix(m1, m2):
    if len(m1) != len(m2):
        return

    for i in range(len(m1)):
        for j in range(len(m2)):
            m2[i][j] = m1[i][j]

    return m2

def compare_matrix(a, b):
    if len(a) != len(b):
        return -1

    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] != b[i][j]:
                return -1
    return 0

def load_q_values(file_name=FILE_NAME):
    logger = Logger()
    file = logger.open(file_name)
    q_values = defaultdict(lambda: np.zeros(4))

    for line in file:
        if line.startswith("TOTAL"):
            break
        else:
            state = line.split(":")[0]
            temp = line.split(":")[1].split(" ")[1:5]

            action_values = []
            for i in range(4):
                action_values.append(float(temp[i]))
            
            q_values[state] = np.array(action_values)

    return q_values

def get_state(state_key):
    rows = int(math.sqrt(len(state_key)))
    columns = rows
    state = np.zeros((rows, columns))

    index = 0
    for i in range(rows):
        for j in range(columns):
            state[i][j] = int(state_key[index])
            index += 1
    
    return state