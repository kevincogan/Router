import pandas as pd
import collections

class Router:
    def __init__(self, node, graph=None):
        self.id = node
        self.adjacent = {}
        self.graph = graph
        # Set distance to infinity for all nodes
        self.distance = 9999999
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_node(self, n):
        if n in self.graph.vert_dict:
            return self.graph.vert_dict[n]
        else:
            return None
#####################################################################################################

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def get_connections(self):
        return list(self.adjacent.keys())

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True




#####################################################################################################

    def get_path(self, router_name):
        start = self.get_node(self.id)
        goal = self.get_node(router_name)
        #print(start.id, goal.id)

        visited = []
        unseenNodes = self.graph
        path = [goal.id]

        start.set_distance(0)
        #print(unseenNodes.vert_dict['e'].get_distance())
        num = 0
        while num != unseenNodes.num_vertices -1: #######################################################
            minNode = None
            for node in unseenNodes.vert_dict:
                #print(unseenNodes.vert_dict[node].visited, node)

                #if unseenNodes.vert_dict[node].visited == True:#####################
                if unseenNodes.vert_dict[node].id in visited:########new list implementation################
                    #print(1)
                    continue

                elif minNode is None:
                    #print(2)
                    minNode = node

                elif unseenNodes.vert_dict[node].get_distance() < unseenNodes.vert_dict[minNode].get_distance(): #find distance of each node to compare.
                    minNode = node
                    #print(3)
                #print(minNode,"----------------------", unseenNodes.vert_dict[node].get_distance())

            for i in self.graph.vert_dict[minNode].get_connections():
                #print(self.graph.vert_dict[minNode].get_weight(i), unseenNodes.vert_dict[minNode].get_distance(), unseenNodes.vert_dict[i.id].get_distance())
                if self.graph.vert_dict[minNode].get_weight(i) + unseenNodes.vert_dict[minNode].get_distance() < unseenNodes.vert_dict[i.id].get_distance():
                    unseenNodes.vert_dict[i.id].set_distance(self.graph.vert_dict[minNode].get_weight(i) + unseenNodes.vert_dict[minNode].get_distance())
                    #print(unseenNodes.vert_dict[i.id].get_distance())
                    unseenNodes.vert_dict[i.id].set_previous(minNode)
                    #print(unseenNodes.vert_dict[i.id].previous)

            #unseenNodes.vert_dict[minNode].set_visited()################
            #print(unseenNodes.vert_dict[i.id].visited)

            visited.append(minNode) ######################new list implementation#########
            #print('_________________________________________________', minNode)

            if num == 100:
                break
            else:
                num += 1

        #print(unseenNodes.vert_dict["f"].adjacent)

        currentNode = goal
        currentNode = currentNode.previous
        path.append(currentNode)

        while currentNode != start.id:
            #=print(currentNode)
            currentNode = self.graph.vert_dict[currentNode].previous
            path.append(currentNode)
        #print(path)

        # print("Start: " + start.id)
        # print("End: " + goal.id)
        # print("Path: " + "->".join(path[::-1]))
        #print("Cost: " + str(self.graph.vert_dict[path[0]].distance))

        hello = [start.id, goal.id, "->".join(path[::-1]), self.graph.vert_dict[path[0]].distance]
        return hello
##############################################################################################################

    def print_routing_table(self):
        from_list = []
        to_list = []
        cost_list = []
        path_list = []

        router_destination = [i for i in self.graph.vert_dict if i != self.id]


        for destination in router_destination:
            items = self.get_path(destination)
            from_list.append(items[0])
            to_list.append(items[1])
            path_list.append(items[2])
            cost_list.append(items[3])

        table = collections.OrderedDict()

        table["from"] = from_list
        table["to"] = to_list
        table["cost"] = cost_list
        table["path"] = path_list

        df = pd.DataFrame(table)
        print(df)
##############################################################################################################

    def remove_router(self, router_name):
        print(self.graph.vert_dict.pop(router_name))
        print("---------------------------")
        for i in self.graph.vert_dict["a"].adjacent:
            if router_name == i.id:
                self.graph.vert_dict["a"].adjacent.pop(i)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0


    def add_router_node(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Router(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def add_router(self, start, goal, cost=0): #Adds an edge to the network graph.
        if start not in self.vert_dict:
            self.add_router_node(start)
        if goal not in self.vert_dict:
            self.add_router_node(goal)

        self.vert_dict[start].add_neighbor(self.vert_dict[goal], cost)
        #self.vert_dict[goal].add_neighbor(self.vert_dict[start], cost) #Uncomment to make the links bidirectional.
################################################################################################



g = Graph()
g.add_router("a", "b", 7)
g.add_router("a", "c", 9)
g.add_router("a", "f", 14)
g.add_router("b", "c", 10)
g.add_router("b", "d", 15)
g.add_router("c", "d", 11)
g.add_router("c", "f", 2)
g.add_router("d", "e", 6)
g.add_router("e", "f", 9)
router = Router("a", g)


#router.get_path("e")

#router.print_routing_table()

router.remove_router("c")
