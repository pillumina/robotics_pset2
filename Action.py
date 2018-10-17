class Action:

    # each movement can be represented by {-1, 0, 1}. backward - -1, still - 0, forward - 1
    # each rotation can be represented by {-1, 0, 1}, left - -1, still - 0, forward - 1

    def __init__(self, move, rotate):

        assert move in [-1, 0, 1]
        assert rotate in [-1, 0, 1]

        self.move = move
        self.rotate = rotate

    def getAction(self):
        return self.move, self.rotate

    def getActionSpace(self):
        return [(-1. -1), (-1, 0), (-1, 1), (0, 0), (1, -1), (1, 0), (1, 1)]