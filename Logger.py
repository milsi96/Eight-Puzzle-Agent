from collections import defaultdict
import numpy as np
from GenericSlidingPuzzle import Puzzle
from GenericSlidingPuzzle import copy_matrix
import math

class Logger:
    def create(self, name):
        return open(name, "a")

    def open(self, name):
        return open(name, "r")

    def append(self, file, line):
        file.write(line + "\n")

    def close(self, file):
        file.close()

    def read(self, file):
        return file.readline()


# q_values = load_q_values()

# puzzle = Puzzle()

# test = [[5, 3, 6], [7, 4, 8], [2, 1, 0]]
# test = [[7, 5, 6], [1, 4, 3], [2, 8, 0]]

# print(q_values["756143280"])

# copy_matrix(test, puzzle.state)

# def key(state):
#     result = ""
#     for i in range(len(state)):
#         for j in range(len(state)):
#             result += str(int(state[i][j]))
#     return result

# def next_action(state):
#     action_values = q_values[key(state)]
#     return np.argmax(action_values)

# step = 1
# while not puzzle.gameover(puzzle.state):
#     print("Step: {}".format(step))
#     print("Current state: {}".format(puzzle.state))
    
#     action = next_action(puzzle.state)
#     print("Action: {}".format(action))

#     puzzle.step(action)
#     step += 1

# print("WIN took {} steps".format(step))
