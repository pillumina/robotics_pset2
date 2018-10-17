from Action import Action
import numpy as np

class Policy:
    def __init__(self, input=None):
        if input is None:
            self.up = [11, 0, 1]
            self.right = [2, 3, 4]
            self.down = [5, 6, 7]
            self.left = [8, 9, 10]
            self.policy_mat = [[]] * 12

            # the policy matrix is a tensor indexed by direction, cur_x and cur_y. Given the current position and known
            # goal position, we can determine the policy for given heading direction.

            policy_mat_up = [[None for y in range(6)] for x in range(6)]
            policy_mat_right = [[None for y in range(6)] for x in range(6)]
            policy_mat_down = [[None for y in range(6)] for x in range(6)]
            policy_mat_left = [[None for y in range(6)] for x in range(6)]


            # If the heading direction is up, then create a policy matrix storing all policies towards goal with up heading.
            for x in range(6):
                for y in range(6):

                    if x == 3 and y == 4: # the state is on the goal position, don't move or rotate:
                        move = 0
                        rotate = 0
                    else:
                        if x > 3: # if the state is on the right side of goal, turn left.
                            rotate = -1
                        elif x == 3: # if the state is on the goal already, don't rotate
                            rotate = 0
                        else: # if the state is on the left side of goal, turn right
                            rotate = 1

                        if y <= 4: # if the state is below the goal or just directly on the left/right of it move forward.
                            move = 1
                        else:  # if the state is above the gaol, move backward.
                            move = -1




                    action = Action(move, rotate)

                    policy_mat_up[x][y] = action

            # if heading direction is right, then determine all the policies in this matrix.
            for x in range(6):
                for y in range(6):

                    if x == 3 and y == 4:
                        move = 0
                        rotate = 0
                    else:
                        if y < 4: # if the state is below the goal, turn left
                            rotate = -1
                        elif y == 4:
                            rotate = 0 # state is on the goal position
                        else:
                            rotate = 1

                        if x <= 3 : # the state is on the left side of goal, move forward
                            move = 1
                        else:  # on the right side of goal, move backward.
                            move = -1

                    action = Action(move, rotate)
                    policy_mat_right[x][y] = action



            # if heading direction is down, then determine all the policies in this matrix.
            for x in range(6):
                for y in range(6):

                    if x == 3 and y == 4:
                        move = 0
                        rotate = 0
                    else:
                        if x <= 2 : # if the state is on the left side of the goal, turn left
                            rotate = -1
                        elif x == 3:
                            rotate = 0 # state is on the goal position
                        else:   # on the right side of goal, turn right
                            rotate = 1

                        if y < 4 : # the state is below the goal, move backward
                            move = -1
                        else:  #  otherwise, move backward.
                            move = 1

                    action = Action(move, rotate)
                    policy_mat_down[x][y] = action



            # if heading direction is left, then determine all the policies in this matrix.
            for x in range(6):
                for y in range(6):

                    if x == 3 and y == 4:
                        move = 0
                        rotate = 0
                    else:
                        if y > 4: # if the state is above the goal, turn left
                            rotate = -1
                        elif y == 4:
                            rotate = 0 # state is on the goal position
                        else:
                            rotate = 1

                        if x >= 3 : # the state is on the left side of the goal, move forward
                            move = 1
                        else:  # the state is on the right side f the goal, move backward.
                            move = -1

                    action = Action(move, rotate)
                    policy_mat_left[x][y] = action

            for dir in range(12):
                if dir in self.up:
                    self.policy_mat[dir] = policy_mat_up
                elif dir in self.right:
                    self.policy_mat[dir] = policy_mat_right
                elif dir in self.left :
                    self.policy_mat[dir] = policy_mat_left
                else:
                    self.policy_mat[dir] = policy_mat_down
        else:
            self.policy_mat = input


    def getPolicyAction(self, cur_state):
        cur_x, cur_y, cur_dir = cur_state.getState()
        return self.policy_mat[cur_dir][cur_x][cur_y]

    def getPolicyMatrix(self):
        return self.policy_mat









