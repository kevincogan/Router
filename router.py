import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = 9999999
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return list(self.adjacent.keys())

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True



    # def __str__(self):
    #     return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(list(self.vert_dict.values()))

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return list(self.vert_dict.keys())

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def dijkstra(graph,start,goal):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = 9999999
    path = [goal.id]

    start.set_distance(0)
    #print(unseenNodes.vert_dict['b'].get_distance())
    num = 0
    while num != len(unseenNodes.vert_dict)-1: #######################################################
        minNode = None
        for node in unseenNodes.vert_dict:
            #print(unseenNodes.vert_dict[node].visited, node)

            if unseenNodes.vert_dict[node].visited == True:
                #print(1)
                continue

            elif minNode is None:
                #print(2)
                minNode = node

            elif unseenNodes.vert_dict[node].get_distance() < unseenNodes.vert_dict[minNode].get_distance(): #find distance of each node to compare.
                minNode = node
                #print(3)
            #print(minNode)

        for i in graph.vert_dict[minNode].get_connections():
            #print(graph.vert_dict[minNode].get_weight(i), unseenNodes.vert_dict[minNode].get_distance(), unseenNodes.vert_dict[i.id].get_distance())
            if graph.vert_dict[minNode].get_weight(i) + unseenNodes.vert_dict[minNode].get_distance() < unseenNodes.vert_dict[i.id].get_distance():
                unseenNodes.vert_dict[i.id].set_distance(graph.vert_dict[minNode].get_weight(i) + unseenNodes.vert_dict[minNode].get_distance())
                #print(unseenNodes.vert_dict[i.id].get_distance())
                unseenNodes.vert_dict[i.id].set_previous(minNode)
                #print(unseenNodes.vert_dict[i.id].previous)

        unseenNodes.vert_dict[minNode].set_visited()
        #print(unseenNodes.vert_dict[i.id].visited)
        #print("end")
        #print("------------------------------------------------------------------")

        if num == 100:
            break
        else:
            num += 1

    # print(graph.vert_dict['a'].previous)
    # print(graph.vert_dict['b'].previous)
    # print(graph.vert_dict['c'].previous)
    # print(graph.vert_dict['d'].previous)
    # print(graph.vert_dict['e'].previous)
    # print(graph.vert_dict['f'].previous)


    currentNode = goal
    currentNode = currentNode.previous
    path.append(currentNode)

    while currentNode != start.id:
        currentNode = graph.vert_dict[currentNode].previous
        path.append(currentNode)
        return path[::-1]

#####################################################################################################
def get_path(ending):

    #print("Start: " + )

    shortest_path = dijkstra(g, g.get_vertex('a'), g.get_vertex(ending))
    print("Path: " + " -> ".join(shortest_path))

#####################################################################################################
if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)


    print(dijkstra(g, g.get_vertex('a'), g.get_vertex("d")))
