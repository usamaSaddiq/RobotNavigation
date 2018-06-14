class Node(object):
    def __init__(self,x,y):
        self._x = x
        self._y = y
        self._visited = False
        
    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @property
    def y(self):
        """I'm the 'y' property."""
        return self._y
        
    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value
    
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __repr__(object):
        return ("{ x : %(x)s , y : %(y)s , visited : %(flag)s}" % {'x' : object.x , 'y' : object.y , 'flag' : object.visited})

    # def __setattr__(self, key, value):
    #     self.setattr(key,value)