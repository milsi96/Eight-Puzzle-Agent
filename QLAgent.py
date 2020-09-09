import numpy as np
import random 
from GenericSlidingPuzzle import Puzzle
import time
from collections import deque
from Logger import Logger
from collections import defaultdict
from GenericSlidingPuzzle import copy_matrix
from datetime import datetime

EPISODES = 10_000
ALFA = 0.4
GAMMA = 0.8
EPSILON = 0.7

FOLDER_NAME = "TrainingEightPuzzle"
EPISODE_FILE_NAME = "./" + FOLDER_NAME + "/episode_{}.txt"
Q_VALUES_FILE = "./" + FOLDER_NAME + "/q_values.txt"
STATS_FILE = "./" + FOLDER_NAME + "/stats.txt"
VISITS_FILE = "./" + FOLDER_NAME + "/visits.txt"

# 
# key(state) returns a string sequence of the numbers that compose the state
#       so that it can be used as a key of the dictionary
#
def key(state):
    result = ""
    for i in range(len(state)):
        for j in range(len(state)):
            result += str(int(state[i][j]))
    return result

def backup_table(q_values, q_values_file=Q_VALUES_FILE):
    logger = Logger()
    q_values_file = logger.create(q_values_file)
    for state in q_values:
        actions = ""
        for action in q_values[state]:
            actions = actions + str(action) + " "
        logger.append(q_values_file, state + ":" + actions)
    logger.append(q_values_file, "TOTAL ANALYZED STATES: " + str(len(q_values)))
    logger.close(q_values_file)

def backup_visits(visits, visits_file=VISITS_FILE):
    logger = Logger()
    visit_file = logger.create(visits_file)
    for state in visits:
        logger.append(visit_file, state + ":" + str(visits[state]))
    logger.close(visit_file)


class QLAgent:
    def __init__(self, epsilon=EPSILON, puzzle=Puzzle(preload_states=True)):
        self.puzzle = puzzle
        self.epsilon = epsilon
        self.q_values = defaultdict(lambda: np.zeros(self.puzzle.action_dim))
        self.visits = defaultdict(int)
    
    def next_action(self, state):
        if random.random() <= self.epsilon:
            return self.puzzle.sample()
        else:
            return np.argmax(self.get_action_values(state))

    def get_action_values(self, state):
        return self.q_values[key(state)]

def q_learning(gamma=GAMMA, alfa=ALFA, episodes=EPISODES):
    agent = QLAgent()
    logger = Logger()

    stats = logger.create(STATS_FILE)
    logger.append(stats, "total: " + str(episodes))
    logger.append(stats, "episode, timesteps, time_elapsed, wrong_moves")

    episode = 0
    while episode < episodes:
        episode += 1
        timestep = 0
        wrong_moves = 0

        start = int(round(time.time() * 1000))

        # if episode & 1000 == 0 and agent.epsilon > 0.1:
        #     agent.epsilon -= 0.1

        agent.puzzle.reset()

        print("Episode: {} started at {}".format(episode, datetime.now()))
        # file = logger.create(EPISODE_FILE_NAME.format(episode))

        done = False
        while not done:
            current_state = copy_matrix(agent.puzzle.state, np.zeros((agent.puzzle.rows, agent.puzzle.columns)))

            action = agent.next_action(current_state)

            next_state, reward, done = agent.puzzle.step(action)
            if reward == -10:
                wrong_moves += 1 

            
            # logger.append(file, "TIMESTEP -> " + str(timestep))
            # logger.append(file, "CURRENT STATE ->\n" + str(current_state))
            # logger.append(file, "ACTION -> " + str(action))
            # logger.append(file, "NEXT_STATE -> \n" + str(next_state))
            # logger.append(file, "REWARD -> " + str(reward))
            # logger.append(file, "\n")


            timestep += 1
            if not done:
                current_q_value = agent.get_action_values(current_state)[action]
                next_q_values = agent.get_action_values(next_state)

                agent.q_values[key(current_state)][action] = current_q_value + alfa * (reward + gamma * np.max(next_q_values) - current_q_value)
            else:
                agent.q_values[key(current_state)][action] = current_q_value + alfa * (reward - current_q_value)
                break

            agent.visits[key(current_state)] = agent.visits[key(current_state)] + 1

        end = int(round(time.time() * 1000))

        # logger.append(file, "FINAL STATE: \n" + str(agent.puzzle.state) + "\n")
        # logger.close(file)

        logger.append(stats, str(episode))
        logger.append(stats, str(timestep))
        logger.append(stats, str(end-start))
        logger.append(stats, str(wrong_moves))
    
    logger.close(stats)

    backup_table(agent.q_values)
    backup_visits(agent.visits)

q_learning()

