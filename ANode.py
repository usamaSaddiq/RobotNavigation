from math import sqrt

class ANode(object):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.g = 0
        self.h = 0
        self.predecessor = None
# string representation of the object
    def __repr__(self):
        return '%d %d' % (self.x, self.y)

# determine the move cost for the current node
    def move_cost(self, rhs):
        diag = abs(self.x - rhs.x) == 1 and abs(self.y - rhs.y) == 1
        if diag:
            return 14
        else:
            return 10