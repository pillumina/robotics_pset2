from Action import Action
from State import  State
import numpy as np

class Env:

    def __init__(self, length, width):

        self.length = length
        self.width = width
        self.num_dirs = 12
        self.states = []
        self.adj_states = [[[None for y in range(self.width)] for x in range(self.length)] for dir in range(self.num_dirs)]


        # initalize the states space and create the adjacent space given current space.
        for i in range(self.length):
            for j in range(self.width):
                for d in range(self.num_dirs):
                    self.states.append(State(i, j, d))
        self.states = set(self.states)



        for state in self.states:
            x, y, dir = state.getState()
            self.adj_states[dir][x][y] = self.cal_adjacent(state)

    def cal_adjacent(self, state):
            adj_states = []

            cur_x, cur_y, cur_dir = state.getState()

            # create lists representing all possible x, y and direction.
            pos_x = [cur_x]
            pos_y = [cur_y]
            pos_dirs = [(cur_dir - 2) % 12, (cur_dir - 1) % 12, cur_dir, (cur_dir + 1) %12, (cur_dir + 2) % 12 ]

            if cur_x - 1 >= 0 :
                pos_x.append(cur_x - 1)
            if cur_x + 1 < self.length:
                pos_x.append(cur_x + 1)
            if cur_y -1 >= 0:
                pos_y.append(cur_y - 1)
            if cur_y + 1 < self.width:
                pos_y.append(cur_y + 1)

            for x in pos_x:
                for y in pos_y:
                    for dir in pos_dirs:
                        adj_states.append(State(x, y, dir))

            return adj_states

    def getAdjStates(self, state):
        x, y, dir = state.getState()
        return self.adj_states[dir][x][y]

