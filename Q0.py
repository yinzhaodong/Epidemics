import numpy as np
import random
# from env import Env
from collections import defaultdict
import numpy as np
import pandas as pd

class QLearningAgent:
    def __init__(self, actions):
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # update q function with sample <s, a, r, s'>
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # using Bellman Optimality Equation to update q function
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    # get action for the state according to the q function table
    # agent pick action of epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # take random action
            action = np.random.choice(self.actions)
        else:
            # take action according to the q function table
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)





class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        print( self.actions)
        self.actions1 = list(range(5))
        self.actions2 = list(range(60))
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action1(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]

            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions,2)
        return action
    def choose_action2(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action2 = np.random.choice(self.actions1)
            action1 = np.random.choice(state_action[state_action == np.max(state_action)].index)
            action = np.random.choice(state_action[state_action == np.max(state_action)].index,2)
            print('1', action, action2)
            action[1] = action2
        else:
            # choose random action
            action = np.random.choice(self.actions1,2)
            action2 = np.random.choice(self.actions2)
            action[1] = action2
            print('2', action, action2)
        print('3', action, action2)
        return action
    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection

        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action1 = np.random.choice(state_action[state_action == np.max(state_action)].index)
            action2 = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action1 = np.random.choice(self.actions1)
            action2 = np.random.choice(self.actions2)
        # print(action1,action2)
        # action = [action1, action2]
        action = np.append(action1, action2)
        # action = pd.Series([action1, action2])
        # action = np.array(action1, action2)
        # filtered_columns = ['text', 'agreeCount']
        # action = action.reindex(columns=filtered_columns)
        # print(action1, action2)
        return action



    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )


