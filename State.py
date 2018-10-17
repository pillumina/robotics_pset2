class State:

    def __init__(self, x=0, y=0, dir=0):
        self.x = x
        self.y = y
        self.dir = dir

    def getState(self):
        return self.x, self.y, self.dir