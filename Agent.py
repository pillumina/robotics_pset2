import numpy as np
import matplotlib.pyplot as plt
from State import State
from Action import Action
from Env import Env
import random
from Policy import Policy

action_space=[(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, -1), (1, 0), (1, 1)]

class Agent:

    def __init__(self, length, width, error_prob):
        self.state = State()
        self.env = Env(length, width)
        self.length = length
        self.width = width
        self.pe = error_prob
        self.num_dirs = 12
        self.state_space_size = self.length * self.width * self.num_dirs
        self.up = [11, 0, 1]
        self.right = [2, 3, 4]
        self.down = [5, 6, 7]
        self.left = [8, 9, 10]

    def getSpaceSize(self):
        return self.state_space_size

    # given the info of current state and the action, calculate the next state without error probability.
    def next_state_no_error(self, cur_x, cur_y, dir, act):
        move, rotate = act.getAction()
        if dir in self.up:
            nxt_x = cur_x
            nxt_y = cur_y + move
        elif dir in self.right:
            nxt_x = cur_x + move
            nxt_y = cur_y
        elif dir in self.down:
            nxt_x = cur_x
            nxt_y = cur_y - move
        else:
            nxt_x = cur_x - move
            nxt_y = cur_y

        # check bound safety
        if nxt_x < 0  or nxt_x >= self.width:
            nxt_x = cur_x
        if nxt_y < 0 or nxt_y >= self.length:
            nxt_y = cur_y

        nxt_dir = (dir + rotate) % 12

        return nxt_x, nxt_y, nxt_dir


    # problem 1(c), get the transition probability given the current state, action, next_state and error prob.
    def get_trans_prob(self, pe, cur_state, act, nxt_state):
        move, rotate = act.getAction()

        # when we don't move, check out some edge conditions.
        if move == 0:
            if cur_state.getState() == nxt_state.getState():
                return 1
            else:
                return 0

        cur_x, cur_y, cur_dir = cur_state.getState()

        transprob = 0

        # check if the error truly happens during the action
        if self.next_state_no_error(cur_x, cur_y, (cur_dir+1)%12, act) == nxt_state.getState():
            transprob += pe
        if self.next_state_no_error(cur_x, cur_y, (cur_dir-1)%12, act) == nxt_state.getState():
            transprob += pe
        # check if no error happens
        if self.next_state_no_error(cur_x, cur_y, cur_dir, act) == nxt_state.getState():
            transprob += 1 - 2 * pe

        # any other scenarios would not happen, therefore return zero.
        return transprob

    # problem 1(d), calculate the next state given error prob, initial state and action
    def calc_nxt_state(self, pe, cur_state, act):
        nxt_states = []
        nxt_states_prob = []

        adj_states = self.env.getAdjStates(cur_state)

        for nxt_possible_state in adj_states:
            trans_prob = self.get_trans_prob(pe, cur_state, act, nxt_possible_state)
            if trans_prob != 0:
                nxt_states.append(nxt_possible_state)
                nxt_states_prob.append(trans_prob)

        nxt_state = np.random.choice(nxt_states, p=nxt_states_prob)
        return nxt_state

        # for x in range(self.length):
        #     for y in range(self.width):
        #         for dir in range(self.num_dirs):
        #             nxt_state = State(x, y, dir)
        #             trans_prob = self.get_trans_prob(pe, cur_state, act, nxt_state)
        #             if trans_prob:
        #                 if trans_prob == pe:
        #                     possible_error_state.append(nxt_state)
        #                 else:
        #                     nxt_no_error_state = nxt_state
        # if random.random() < 2 * pe:
        #     return random.choice(possible_error_state)
        # else:
        #     return nxt_no_error_state

    # probem 2, return the reward value given current state
    def get_reward(self, cur_state):
        cur_x, cur_y, cur_dir = cur_state.getState()

        if cur_x == 0  or cur_x == self.length - 1 or cur_y == 0 or cur_y == self.width - 1:
            reward =  -100
        elif (cur_x == 2 or cur_x ==4) and (cur_y >=2 and cur_y <= 4) :
            reward = -10
        elif cur_x == 3 and cur_y == 4:
            reward = 1
        else:
            reward = 0
        return reward

    # problem 3(b), plot the trajectory of a robot given policy, initial state and error prob
    def plot_trajectory(self, policy, init_state, pe):
        traj = []

        cur_state = init_state
        cur_x, cur_y, _= cur_state.getState()
        traj.append((cur_x, cur_y))

        while cur_x != 3 or cur_y !=4 :  # if the current state does not reach the goal position, then calculate the next state and update
            policy_action = policy.getPolicyAction(cur_state)
            nxt_state = self.calc_nxt_state(pe, cur_state, policy_action)
            cur_x, cur_y, dir = nxt_state.getState()
            traj.append((cur_x, cur_y))
            cur_state = nxt_state


        print(traj)

        fig, ax = plt.subplots()
        ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], minor=False)
        ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], minor=False)
        ax.yaxis.grid(True, which='major')
        ax.xaxis.grid(True, which='major')
        plt.axis([-0.5, 5.5, -0.5, 5.5])

        for i in range(len(traj) - 1):
            cur_x, cur_y = traj[i][0], traj[i][1]
            nxt_x, nxt_y = traj[i+1][0], traj[i+1][1]
            dx = nxt_x - cur_x
            dy = nxt_y - cur_y
            plt.arrow(cur_x, cur_y, dx, dy, head_width=0.05, head_length=0.1, length_includes_head=True)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Trajectory of the given policy')
        plt.show()
        return traj



    def plot_trajectory_mod(self, policy, init_state, pe):
        traj = []

        cur_state = init_state
        cur_x, cur_y, cur_dir= cur_state.getState()
        traj.append((cur_x, cur_y, cur_dir))

        while cur_x != 3 or cur_y !=4 or cur_dir >7 or cur_dir < 5:  # if the current state does not reach the goal position, then calculate the next state and update
            policy_action = policy.getPolicyAction(cur_state)
            nxt_state = self.calc_nxt_state(pe, cur_state, policy_action)
            cur_x, cur_y, cur_dir = nxt_state.getState()

            print(cur_x, cur_y, cur_dir)
            traj.append((cur_x, cur_y, cur_dir))
            cur_state = nxt_state


        print(traj)

        fig, ax = plt.subplots()
        ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], minor=False)
        ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], minor=False)
        ax.yaxis.grid(True, which='major')
        ax.xaxis.grid(True, which='major')
        plt.axis([-0.5, 5.5, -0.5, 5.5])

        for i in range(len(traj) - 1):
            cur_x, cur_y = traj[i][0], traj[i][1]
            nxt_x, nxt_y = traj[i+1][0], traj[i+1][1]
            dx = nxt_x - cur_x
            dy = nxt_y - cur_y
            plt.arrow(cur_x, cur_y, dx, dy, head_width=0.05, head_length=0.1, length_includes_head=True)

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Trajectory of the given policy')
        plt.show()
        return traj

    def traj_value(self, traj):
        value = 0

        for tuple in traj:
            x, y = tuple
            cur_state = State(x, y, dir=0)
            value += self.get_reward(cur_state)

        return value


    def traj_value_mod(self, traj):
        value = 0

        for tuple in traj:
            x, y, cur_dir = tuple
            cur_state = State(x, y, cur_dir)
            value += self.get_reward_modified(cur_state)

        return value




    # problem 3(d) & 5(b) Policy evaluation, return a matrix of values indexed by state.
    # if the mod argument is True, the get reward function would be modified w.r.t 5(b). Otherwise.
    def policy_eval(self, policy, discount, mod=False, pe=0):

        # confidence = 0.01

        converge = False
        prev_value = np.zeros((self.num_dirs, self.width, self.length))

        while not converge:
            new_value = np.zeros((self.num_dirs, self.width, self.length))

            state_space = self.env.states

            # update the value matrix by calculating the sum of values of current state w.r.t its adjacent states.
            for cur_state in state_space:
                cur_x, cur_y, cur_dir = cur_state.getState()
                adj_states = self.env.getAdjStates(cur_state)

                for nxt_state in adj_states:
                    act = policy.getPolicyAction(cur_state)
                    trans_prob = self.get_trans_prob(pe, cur_state, act, nxt_state)
                    if not mod:
                        reward = self.get_reward(cur_state)
                    else:
                        reward = self.get_reward_modified(cur_state)

                    nxt_x, nxt_y, nxt_dir = nxt_state.getState()
                    nxt_value = prev_value[nxt_dir][nxt_x][nxt_y]

                    new_value[cur_dir][cur_x][cur_y] += trans_prob * (reward + discount * nxt_value)

            # calculate the difference between the previous and current value matrices.
            # diff =  max(diff, np.sum(np.abs(new_value - prev_value)))
            diff = np.sum(np.abs(new_value - prev_value))
            prev_value = new_value            # print(diff)

            if diff == 0:
                converge = True

        return new_value

    # problem 3(f) using one-step lookahead on value matrix to return the pi giving the optimal policy.
    def one_step_lookahead(self, V, pe=0):
        new_policy_mat = [[[None for y in range(self.length)] for x in range(self.width)] for dir in range(self.num_dirs)]
        for state in self.env.states:
            adj_states = self.env.getAdjStates(state)
            max_action_value = float("-inf")
            best_action = None
            for action_tuple in action_space:
                move, rotate = action_tuple
                action = Action(move,rotate)
                action_value = 0
                for nxt_state in adj_states:
                    nxt_x, nxt_y, nxt_dir = nxt_state.getState()
                    action_value += self.get_trans_prob(pe, state, action, nxt_state) * V[nxt_dir][nxt_x][nxt_y]
                if action_value > max_action_value:
                    max_action_value = action_value
                    best_action = action

            cur_x, cur_y, cur_dir = state.getState()
            new_policy_mat[cur_dir][cur_x][cur_y] = best_action

        new_policy = Policy(new_policy_mat)
        return new_policy

    # problem 3(g) combine the functions above and do policy iteration, returning optimal policy with optimal value
    def policy_iter(self, init_policy, discount, pe=0):

        prev_value = self.policy_eval(init_policy, discount, pe)
        prev_policy = self.one_step_lookahead(prev_value, pe)
        converge = False

        while not converge:
            print ('\nPolicy iteration')
            new_value = self.policy_eval(prev_policy, discount, pe)
            new_policy = self.one_step_lookahead(new_value, pe)

            diff = np.sum(np.abs(new_value - prev_value))
            print ("Value difference is : ", diff)

            # converge if new_value = last_value, then we get the optimal policy.
            if np.array_equal(new_value, prev_value):
                converge = True

            prev_value = new_value
            prev_policy = new_policy

        return new_policy, new_value

    # problem 4(a), Value Iteration.
    def value_iter(self, discount, pe=0):
        prev_value = np.zeros((self.num_dirs, self.width, self.length))
        new_policy_matrix = [[[None for y in range(self.length)] for x in range(self.width)] for dir in
                             range(self.num_dirs)]

        converge = False

        while not converge:
            # print("\nValue Iteration ")
            new_value = np.zeros((self.num_dirs, self.width, self.length))
            for cur_state in self.env.states:
                cur_x, cur_y, cur_dir = cur_state.getState()
                adj_states = self.env.getAdjStates(cur_state)
                best_action = None
                max_action_value = float("-inf")
                for action_tuple in action_space:
                    move, rotate = action_tuple
                    action = Action(move, rotate)
                    action_value = 0
                    for nxt_state in adj_states:
                        x, y, dir = nxt_state.getState()
                        action_value += self.get_trans_prob(pe, cur_state, action, nxt_state) * (
                                    self.get_reward(cur_state) + discount * prev_value[dir][x][y])
                    if action_value > max_action_value:
                        best_action = action
                        max_action_value = action_value

                new_policy_matrix[cur_dir][cur_x][cur_y] = best_action
                new_value[cur_dir][cur_x][cur_y] = max_action_value

            diff = np.sum(np.abs(new_value - prev_value))
            # print("Value diff: ", diff)
            if np.array_equal(new_value, prev_value):
                converge = True
            prev_value = new_value
        new_policy = Policy(new_policy_matrix)
        return new_policy, new_value


    #  problem 5(b) change the reward
    def get_reward_modified(self, cur_state):
        cur_x, cur_y, cur_dir = cur_state.getState()

        if cur_x == 0  or cur_x == self.length - 1 or cur_y == 0 or cur_y == self.width - 1:
            reward =  -100
        elif (cur_x == 2 or cur_x ==4) and (cur_y >=2 and cur_y <= 4) :
            reward = -10
        elif cur_x == 3 and cur_y == 4 and (cur_dir == 5 or cur_dir == 6 or cur_dir ==7):
            reward = 1
        else:
            reward = 0
        return reward





# policy = Policy()
# init_state = State(1, 4, 6)
# #
# agent = Agent(6,6,0)
#
# agent.plot_trajectory(policy, init_state, 0)
# value = agent.policy_eval(policy, 0.9)
#
# print(value[6][1][4])



# pl_mat = policy.getPolicyMatrix()
# pl_mat = np.asarray(pl_mat)
#
# print(pl_mat[0][0][0].getAction())





