import Grid,copy
from AGrid import AGrid, ANode
from itertools import product
import sys

def construct_graph(data):
    # initialize all of the astar nodes
    nodes = [[ANode(x, y) for y in range(data['height'])] for x in range(data['width'])]
    graph = {}
    # make a graph with child nodes
    for x, y in product(range(data['width']), range(data['height'])):
        node = nodes[x][y]
        graph[node] = []
        for i, j in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if not (0 <= x + i < data['width']): continue
            if not (0 <= y + j < data['height']): continue
            if [x+i,y+j] in data['obstacle']: continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes

def construct_diaganol_graph(data):
    # initialize all of the astar nodes
    nodes = [[ANode(x, y) for y in range(data['height'])] for x in range(data['width'])]
    graph = {}
    # make a graph with child nodes
    for x, y in product(range(data['width']), range(data['height'])):
        node = nodes[x][y]
        graph[node] = []
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < data['width']): continue
            if not (0 <= y + j < data['height']): continue
            if [x+i,y+j] in data['obstacle']: continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes

def getObstacles():
    blocked = []
    for node in g.blocked_nodes:
        blocked.append([node.y,node.x])
    return blocked
if __name__ == '__main__':
    try:
        g = Grid.Grid(sys.argv[1])
        recPath = []
        path = []
        no_of_nodes = []
        graph, nodes = construct_graph({"width": g.total_width, "height": g.total_height, "obstacle": getObstacles()})
        agrid = AGrid(graph)
        start, goal = (nodes[g.start.y][g.start.x], nodes[g.goal.y][g.goal.x])

        if sys.argv[2] == 'Dfs':
            path = g.dfs(g.start)
        elif sys.argv[2] == 'Bfs':
            path = g.bfs(g.start)
        elif sys.argv[2] == 'Gbfs':
            path,no_of_nodes = agrid.gbf_search(start, goal)
        elif sys.argv[2] == 'Astar':
            path,no_of_nodes = agrid.search(start,goal)
        elif sys.argv[2] == 'Rdfs':
            g.rec_dfs(g.start,recPath)
        elif sys.argv[2] == 'Adiaganol':
            graph, nodes = construct_diaganol_graph({"width": g.total_width, "height": g.total_height, "obstacle": getObstacles()})
            grid = AGrid(graph)
            path,no_of_nodes = grid.search(nodes[g.start.y][g.start.x], nodes[g.goal.y][g.goal.x])
        else:
            print("Not a valid search method. Please try Dfs,Bfs,Gbfs,Astar,Rdfs,Adiaganol")
            raise Exception

        if path:
            path_length = len(no_of_nodes)
            print sys.argv[0], sys.argv[2], path_length
            print path
        elif sys.argv[2] == 'Rdfs':
                print sys.argv[0], sys.argv[2], len(recPath)
                print recPath
        else:
            print "No path found."

    except Exception as e:
        print "Something went wrong while running the project. Please make sure you have entered the correct parameters."
        print "Valid parameters are filename and the search method name." 
        print "All parameters are mandatory"
        print (e.message)