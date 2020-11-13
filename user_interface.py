import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import math
import collections


class Router:
    def __init__(self, router_name, graph=None):
        self.router_name = router_name #name of the router
        self.connectioned_routers = {} #finds the routers that are connected to the current router.
        self.graph = graph #This is the routering table for this router.
        self.edge_length = math.inf #Edge length for this router.
        self.previous_router = None # Keeps track of the previous connection.

    # adds a connection to the router's routing table.
    def add_connections(self, connection, cost=0):
        self.connectioned_routers[connection] = cost

    # gets the connections to the router from the router's routing table.
    def get_connections(self):
        return list(self.connectioned_routers.keys())

    # gets the edge weight of the graph.
    def get_weight(self, connection):
        return self.connectioned_routers[connection]


    # sets the edge length.
    def set_edge_length(self, dist):
        self.edge_length = dist
    # gets the edges length.
    def get_edge_length(self):
        return self.edge_length


    #Uses dijkstra's algorithm to find the shortest path from the start to the goal.
    def get_path(self, router_name, access=None):
        start = self.graph.router_dict[self.router_name] #Staring router.
        goal = self.graph.router_dict[router_name] #End router.

        visited = [] #Routers visited are add to this list to ensure we do not skip an router and recalculate the edge length twice.
        router_table = self.graph # This is the routing table.
        path = [goal.router_name] # The path if the shortest path is put in this list.

        start.set_edge_length(0) # set the starting length to be zero.

        num = 0
        while num != router_table.router_total -1: # Iterates through the router table until the incremented number reaches the number of router in the routing table.
            minimium_length_router = None

            #Iterates the graph to find the minimium edge length between the current router and the connected routers to the current router.
            for router in router_table.router_dict:
                if router_table.router_dict[router].router_name in visited: #Check if the router has been visited already
                    continue
                elif minimium_length_router is None: #If the minimium router length is at None.
                    minimium_length_router = router
                elif router_table.router_dict[router].get_edge_length() < router_table.router_dict[minimium_length_router].get_edge_length(): #Compares the combined edge length to the other paths to the same router and finds the shortest length.
                    minimium_length_router = router

            for i in router_table.router_dict[minimium_length_router].get_connections():
                if router_table.router_dict[minimium_length_router].get_weight(i) + router_table.router_dict[minimium_length_router].get_edge_length() < router_table.router_dict[i.router_name].get_edge_length():
                    router_table.router_dict[i.router_name].set_edge_length(router_table.router_dict[minimium_length_router].get_weight(i) + router_table.router_dict[minimium_length_router].get_edge_length())
                    router_table.router_dict[i.router_name].previous_router = minimium_length_router

            visited.append(minimium_length_router) #Router added to visited list as we have already visited that router.

            num += 1 #Increments the number of routers we visted by one.

        #We create a path from the goal not to the start node by finding the previous router of each router then we add the value to the path list.
        current_router = goal
        current_router = current_router.previous_router # Getting the previous router.
        path.append(current_router) #Adding router to path list.

        while current_router != start.router_name: #Creating the shortest path until the current router is equal to the start router.
            current_router = router_table.router_dict[current_router].previous_router
            path.append(current_router)

        if access == 1: # Access acts as a flag only allowing the print_routing_table() to access this section of code that is need to build a formated routing table using pandas.
            hello = [start.router_name, goal.router_name, "->".join(path[::-1]), router_table.router_dict[path[0]].edge_length]
            return hello
        else: # The shortest path will be formated and outputted to the user with the information below.
            print("Start: " + start.router_name) #Prints out the starting router.
            print("End: " + goal.router_name) #Prints out the end router.
            print("Path: " + "->".join(path[::-1])) # Reverses the path list and prints out the sortest path.
            print("Cost: " + str(router_table.router_dict[path[0]].edge_length)) #Prints out the length of the shortest path to the desired router.


    #Creates a table for the routing table.
    def print_routing_table(self):
        # Dividing each column into lists.
        from_list = []
        to_list = []
        cost_list = []
        path_list = []

        router_destination = [i for i in self.graph.router_dict if i != self.router_name] #Gets all the destination routers.

        #Sorts the information into its relevant list so it can be displayed in the table.
        for destination in router_destination:
            items = self.get_path(destination, 1)
            from_list.append(items[0])
            to_list.append(items[1])
            path_list.append(items[2])
            cost_list.append(items[3])

        table = collections.OrderedDict() # Using an ordered dictionary so the format of the graph does not change.

        #Creating the table and headers of the table.
        table["from"] = from_list
        table["to"] = to_list
        table["cost"] = cost_list
        table["path"] = path_list

        df = pd.DataFrame(table) #Constructing the table using pandas.
        print(df)

    #Removes the router from the routing table.
    def remove_router(self, router_name):
        remove_edges = [] #list of edges to be romoved

        self.graph.router_total = self.graph.router_total -1 # Decrements the number of routers in the router count.

        #Resetting the routing table
        for router in self.graph.router_dict:
            for j in self.graph.router_dict[router].connectioned_routers:
                j.previous_router = None #setting the previous router to None
                j.set_edge_length(math.inf) #setting the edge length of the router to infinity
                if j.router_name == router_name: #if this is the router to be removed then remove the router.
                    remove_edges.append(j)

        #Removes the connections to the removes router.
        for router in self.graph.router_dict:
            for edges in remove_edges:
                if edges in self.graph.router_dict[router].connectioned_routers: #if the edge is a connection to the existing router then remove the connection.
                    self.graph.router_dict[router].connectioned_routers.pop(edges)
        self.graph.router_dict.pop(router_name) # Edge removed

        self.print_routing_table()



    #Creates a visual graph using the information from the routing table.
    def map_out_graph(self, G):
        #Iterates through the routing table to create the nodes and edges of the graph with its respective weights and names.
        for node in self.graph.router_dict:
            for innernode in self.graph.router_dict[node].connectioned_routers:
                u = node
                v = innernode.router_name
                value = self.graph.router_dict[node].get_weight(innernode)
                G.add_edge(u, v, r=value)

        nodes = [(u, v) for (u, v, d) in G.edges(data=True)]

        pos = nx.spring_layout(G, scale=2) #Generates a dictionary of nodes with their associated weights usding an inbuilt function.
        nx.draw_networkx_nodes(G, pos, node_color="Red", node_size=700) #Draws the nodes to the table with the customisations inputted.


        edge_labels = nx.get_edge_attributes(G,'r') #Gets the edge vaues in the graph ans stores them.

        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels) #This adds the weight lables to the edges on the graph.
        nx.draw_networkx_edges(G, pos, edgelist=nodes, width=6, alpha=0.5, edge_color="blue", style="dashed") #This draws the connections between each node.

        nx.draw_networkx_labels(G, pos, font_size=20, font_color="oldlace",font_weight="bold", font_family="sans-serif") #Allows us to label the nodes.



        plt.draw() #Plots the graph.
        plt.show() #Displays the graph on the screen.


class Graph:
    def __init__(self):
        self.router_dict = {} # Router table that contains all the inforamtion about the routers and edge lengths between routers.
        self.router_total = 0 # Counts the number of active routers.

    # Creates a new router and adds it to the routing table.
    def add_router(self, router):
        new_router = Router(router) # Creates an object for a router.
        self.router_dict[router] = new_router # adds to the router_dict which is a dictionary with all routers and router edge lengths.
        self.router_total = self.router_total + 1 # Increments the router count by one.
        return new_router

    #Creates an edges between two routers that is multi-directional.
    def add_edge(self, start, goal, cost=0):
        if start not in self.router_dict: #Check if the router is already in the router dictionary (Routing table).
            self.add_router(start) # Adds router to the router table.
        if goal not in self.router_dict: #Check if the router is already in the router dictionary (Routing table).
            self.add_router(goal) # Adds router to the router table.

        #Creates a multi-directional graph.
        self.router_dict[start].add_connections(self.router_dict[goal], cost)
        self.router_dict[goal].add_connections(self.router_dict[start], cost)
################################################################################################


#Creates adds edges to the routing table.
graph = Graph()
graph.add_edge("a", "b", 7)
graph.add_edge("a", "c", 9)
graph.add_edge("a", "f", 14)
graph.add_edge("b", "c", 10)
graph.add_edge("b", "d", 15)
graph.add_edge("c", "d", 11)
graph.add_edge("c", "f", 2)
graph.add_edge("d", "e", 6)
graph.add_edge("e", "f", 9)

router = Router("a", graph)
router_two = Router("b", graph)

G=nx.Graph()


router.get_path("f")

router.print_routing_table()
#router.remove_router("c")
router.print_routing_table()

router_two.remove_router("c")

router_two.remove_router("f")

router_two.map_out_graph(G)
