from ANode import ANode

class AGrid(object):
    def __init__(self, graph):
        self.graph = graph
    # heuristic function to determine the distance form goal node
    def heuristic(self, node, start, goal):
        return abs(goal.x - node.x) + abs(goal.y - node.y)

    def search(self, start, goal):
        open = set()
        closed = set()
        curr = start
        no_of_nodes = []
        open.add(curr)
        no_of_nodes.append(curr)    
        while open:
            curr = min(open, key=lambda o:o.g + o.h)
            if curr == goal:
                path = []
                while curr.predecessor:
                    path.append(curr)
                    curr = curr.predecessor
                path.append(curr)
                return path[::-1],no_of_nodes
            open.remove(curr)
            closed.add(curr)
            for vertice in self.graph[curr]:
                if vertice in closed:
                    continue
                if vertice in open:
                    new_g = curr.g + curr.move_cost(vertice)
                    no_of_nodes.append(vertice)
                    if vertice.g > new_g:
                        vertice.g = new_g
                        vertice.predecessor = curr
                else:
                    vertice.g = curr.g + curr.move_cost(vertice)
                    vertice.h = self.heuristic(vertice, start, goal)
                    vertice.predecessor = curr
                    open.add(vertice)
        return None
        
    def gbf_search(self, start, goal):
        open = set()
        closed = set()
        no_of_nodes = [] 
        curr = start
        open.add(curr)
        no_of_nodes.append(curr)
        while open:
            curr = min(open, key=lambda o:o.h)
            if curr == goal:
                path = []
                while curr.predecessor:
                    path.append(curr)
                    curr = curr.predecessor
                path.append(curr)
                return path[::-1],no_of_nodes
            open.remove(curr)
            closed.add(curr)
            for vertice in self.graph[curr]:
                no_of_nodes.append(vertice)                 
                if vertice in closed:
                    continue
                else:
                    vertice.h = self.heuristic(vertice, start, goal)
                    vertice.predecessor = curr
                    open.add(vertice)
        return no_of_nodes
        