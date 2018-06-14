from Node import Node
from collections import defaultdict
import Queue
from itertools import product

# initialize the grid obejct with values
class Grid(object):
    def __init__(self,filename):
        self._graph= None
        self._start = None
        self._goal = None
        self._total_height = None
        self._total_width = None
        self._blocked_nodes = []
        self.loadFile(filename)
    
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
    
    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        self._goal = value
    
    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value
    
    @property
    def total_width(self):
        return self._total_width

    @property
    def total_height(self):
        return self._total_height

    @total_width.setter
    def total_width(self, value):
        self._total_width = value
    
    @total_height.setter
    def total_height(self, value):
        self._total_height = value

    @property
    def blocked_nodes(self):
        return self._blocked_nodes

    @blocked_nodes.setter
    def blocked_nodes(self, value):
        self._blocked_nodes = value


    def getCoordinates(self,data_points):
        start_data = data_points.split(',')
        y_coordinate = int(filter(str.isdigit,start_data[0]))
        x_coordinate = int(filter(str.isdigit,start_data[1]))
        return {"x" : x_coordinate, "y" :  y_coordinate}

    def loadStates(self,graph_data):
        start_data = self.getCoordinates(graph_data[1])
        self.start = Node(start_data["x"],start_data["y"])
        goal_data = self.getCoordinates(graph_data[2])
        self.goal = Node(goal_data["x"],goal_data["y"])
 
    def exists(self,x,y):
        return x >= 0 and x < self.total_height and y >= 0 and y < self.total_width

    def getDimensions(self,graph_data):
        dimensions = graph_data[0].split(',')
        height = int(filter(str.isdigit,dimensions[0]))
        width = int(filter(str.isdigit,dimensions[1]))
        return height,width

# extract all of the blocked nodes from the project
    def getBlockedNodes(self,graph_data):
        blocks =  defaultdict(list)
        blocked_nodes = []
        # start at the third index
        for key,value in enumerate(graph_data):
            if(key>2):
                if(value):
                    values = value.split(',')   
                    for k,v in enumerate(values):
                        blocks[key].append(int(filter(str.isdigit,v)))
        
        for index in blocks:
            y = blocks[index][0]
            x = blocks[index][1]
            blocked_nodes.append(Node(x,y))
            
            cell_width = blocks[index][2]
            cell_height = blocks[index][3]
            
            counter = 1
            while counter <= cell_width:
                if not (Node(x,(y+counter)-1)) in blocked_nodes: 
                    if self.exists(x,(y+counter)-1):
                        blocked_nodes.append(Node(x,(y+counter)-1))
                counter += 1
            counter = 1
            x = x + cell_height - 1
            while counter <= cell_width:
                if not (Node(x,(y+counter)-1)) in blocked_nodes:
                    if self.exists(x,(y + counter)-1):                   
                        blocked_nodes.append(Node(x,(y + counter)-1))
                counter += 1
        return blocked_nodes

    def createGraph(self,graph_data):
        self.loadStates(graph_data)
        self.total_height,self.total_width = self.getDimensions(graph_data)
        #construct a graph with dimensions
        self.graph = [[Node(x,y) for y in range(self.total_width)] for x in range(self.total_height)]
        self.blocked_nodes = self.getBlockedNodes(graph_data)


    def loadFile(self,filename):
        text_file = open(filename, "r")
        graph_data = text_file.read().split('\n')      
        self.createGraph(graph_data)

    def should_visit(self,node):
        return not(node in self.blocked_nodes or node.visited == True)

    def rec_dfs(self,current,recPath):
        self.graph[current.x][current.y].visited = True 
        recPath.append([current.y,current.x])
        if current == self.goal:
            return None
        if(self.exists(current.x-1,current.y) and self.should_visit(self.graph[current.x-1][current.y])):
            self.rec_dfs(self.graph[current.x-1][current.y],recPath)
        if(self.exists(current.x,current.y-1) and self.should_visit(self.graph[current.x][current.y-1])):
            self.rec_dfs(self.graph[current.x][current.y-1],recPath)
        if(self.exists(current.x+1,current.y) and self.should_visit(self.graph[current.x+1][current.y])):          
            self.rec_dfs(self.graph[current.x+1][current.y],recPath)
        if(self.exists(current.x,current.y+1) and self.should_visit(self.graph[current.x][current.y+1])):
            self.rec_dfs(self.graph[current.x][current.y+1],recPath)

    def dfs(self,current):
        q = []
        path = []
        q.append(current)
        while(not q.count == 0):
            current = q.pop(0)
            self.graph[current.x][current.y].visited = True
            path.append([current.y,current.x])
            if current == self.goal: return path
            if(self.exists(current.x,current.y+1) and self.should_visit(self.graph[current.x][current.y+1])):
                q.insert(0 , self.graph[current.x][current.y+1])
            if(self.exists(current.x+1,current.y) and self.should_visit(self.graph[current.x+1][current.y])): 
                q.insert(0, self.graph[current.x+1][current.y])
            if(self.exists(current.x,current.y-1) and self.should_visit(self.graph[current.x][current.y-1])):
                q.insert(0, self.graph[current.x][current.y-1])
            if(self.exists(current.x-1,current.y) and self.should_visit(self.graph[current.x-1][current.y])):
                q.insert(0, self.graph[current.x-1][current.y])
            
    def bfs(self,current):
        q = Queue.Queue()
        path = []
        q.put(current)
        while(not q.empty()):
            current = q.get()
            self.graph[current.x][current.y].visited = True
            path.append([current.y,current.x])
            if current == self.goal: return path
            if(self.exists(current.x-1,current.y) and self.should_visit(self.graph[current.x-1][current.y])):
                self.graph[current.x-1][current.y].visited = True
                q.put(self.graph[current.x-1][current.y])
            if(self.exists(current.x,current.y-1) and self.should_visit(self.graph[current.x][current.y-1])):
                self.graph[current.x][current.y-1].visited = True
                q.put(self.graph[current.x][current.y-1])
            if(self.exists(current.x+1,current.y) and self.should_visit(self.graph[current.x+1][current.y])):          
                self.graph[current.x+1][current.y].visited = True
                q.put(self.graph[current.x+1][current.y])
            if(self.exists(current.x,current.y+1) and self.should_visit(self.graph[current.x][current.y+1])):
                self.graph[current.x][current.y+1].visited = True               
                q.put(self.graph[current.x][current.y+1])