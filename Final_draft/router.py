import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import math
import collections


class Router:
    def __init__(self, router_name, graph=None):
        self.router_name = router_name #Retrieves the name of the router
        self.connectioned_routers = {} #Finds the routers that are neighrbours to the current router.
        self.graph = graph #This is the graph that shows what routers are mapped to each other and the weights/costs associated with them.
        self.edge_cost = math.inf #This gives you theEdge length for this router.
        self.previous_router = None # Keeps track of the previous connection for each router so we can get the shortest path.
        self.table = [] #This contains the routing table for the specific router.

    #Adds a router connection to the graph.
    def add_connections(self, connection, cost=0):
        self.connectioned_routers[connection] = cost

    #Gets the router neightbours for a given router from the graph.
    def get_connections(self):
        return list(self.connectioned_routers.keys())

    #Gets the edge weight between two routers on the graph.
    def get_weight(self, connection):
        return self.connectioned_routers[connection]

    #Sets the edge length.
    def set_edge_cost(self, dist):
        self.edge_cost = dist

    #Gets the edges costs for a router.
    def get_edge_cost(self):
        return self.edge_cost

    #This resets the values of the router so the router table can be recalculate again.
    def reset_values(self):
        for router in self.graph.router_dict: #Itterates through all the routers.
            for j in self.graph.router_dict[router].connectioned_routers: # Itterates through all the connections to a given router.
                j.previous_router = None #re-setting the previous router to None
                j.set_edge_cost(math.inf) # re-setting the edge cost to infinity.


    #Uses dijkstra's algorithm to find the shortest path from the start to the goal.
    def get_path(self, router_name, access=None):
        start = self.graph.router_dict[self.router_name] #Staring router.
        goal = self.graph.router_dict[router_name] #End router.

        self.reset_values() # Reset the router so that we can recalculate the shortest path and a new routing table.

        visited = [] #Routers visited are add to this list to ensure we do not skip an router and recalculate the edge length twice.
        router_graph = self.graph # This is the routing table.
        path = [goal.router_name] # The path if the shortest path is put in this list.

        start.set_edge_cost(0) # Set the starting length to be zero.

        counter = 0
        while counter != router_graph.router_total -1: # Iterates through the router table until the incremented number reaches the number of router in the routing table.
            minimium_cost = None #Set minimium cost of node to None

            #Iterates the graph to find the minimium edge cost between the current router and the connected routers.
            for router in router_graph.router_dict:
                if router_graph.router_dict[router].router_name in visited: #Checks if the router has been visited already
                    continue
                elif minimium_cost is None: #If the minimium cost is None.
                    minimium_cost = router #Set to the current router.
                elif router_graph.router_dict[router].get_edge_cost() < router_graph.router_dict[minimium_cost].get_edge_cost(): #Compares the combined edge costs to the other paths for a particular router and finds the shortest cost.
                    minimium_cost = router #Set to the current router.

            for neighbour in router_graph.router_dict[minimium_cost].get_connections(): #Finds the router connections to the minimium cost router.
                if router_graph.router_dict[minimium_cost].get_weight(neighbour) + router_graph.router_dict[minimium_cost].get_edge_cost() < router_graph.router_dict[neighbour.router_name].get_edge_cost():
                    router_graph.router_dict[neighbour.router_name].set_edge_cost(router_graph.router_dict[minimium_cost].get_weight(neighbour) + router_graph.router_dict[minimium_cost].get_edge_cost()) #Sets the new combined edge cost.
                    router_graph.router_dict[neighbour.router_name].previous_router = minimium_cost #Sets the previous router for the current router.

            visited.append(minimium_cost) #Router added to visited list.

            counter += 1 #Increments the counter of routers visted.

        #We create a path from the goal router to the start router by finding the previous router of each router then we add the value to the path list.
        current_router = goal
        current_router = current_router.previous_router # Gets the previous router for the current router.
        path.append(current_router) #Adding router to path list.

        #adding the shortest router to the path until the current router is equal to the start router.
        while current_router != start.router_name:
            current_router = router_graph.router_dict[current_router].previous_router #Finds the previous router for the current router.
            path.append(current_router) #Adds router to the path list.

        if access == 1: # Access acts as a flag only allowing the print_routing_table() to access this section of code that is need to build a formated routing table using pandas.
            hello = [start.router_name, goal.router_name, "->".join(path[::-1]), router_graph.router_dict[path[0]].edge_cost]
            return hello
        else: # The shortest path will be formated and outputted to the user with the information below.
            print("Start: " + start.router_name) #Prints out the starting router.
            print("End: " + goal.router_name) #Prints out the end router.
            print("Path: " + "->".join(path[::-1])) # Reverses the#adding the shortest router to the path until the current router is equal to the start router. path list and prints out the sortest path.
            print("Cost: " + str(router_graph.router_dict[path[0]].edge_cost)) #Prints out the length of the shortest path to the desired router.


    #Creates a table for the routing table.
    def print_routing_table(self):
        # Dividing each column into lists.
        self.table = []
        from_list = []
        to_list = []
        cost_list = []
        path_list = []

        router_destination = [i for i in self.graph.router_dict if i != self.router_name] #Gets all the destination routers.

        #Sorts the information into its relevant list so it can be displayed in the table.
        for destination in router_destination:
            items = self.get_path(destination, 1)
            self.table.append([items[1], items[3]]) # Creates the router table
            from_list.append(items[0])
            to_list.append(items[1])
            path_list.append(items[2])
            cost_list.append(items[3])

        table = collections.OrderedDict() # Using an ordered dictionary so the format of the graph does not change into a default order.

        #Creating the table and headers of the table.
        table["from"] = from_list
        table["to"] = to_list
        table["cost"] = cost_list
        table["path"] = path_list

        df = pd.DataFrame(table) #Constructing the table using pandas.
        print(df)

    #Removes the router from the routing table.
    def remove_router(self, router_name):
        remove_edges = [] #list of edges to be removed

        self.graph.router_total = self.graph.router_total -1 # Decrements the number of routers in the router count.

        #Resetting the routing table
        for router in self.graph.router_dict:
            for neighbour in self.graph.router_dict[router].connectioned_routers: # Accesses all neighbour routers to the current router.
                neighbour.previous_router = None #setting the previous router to None
                neighbour.set_edge_cost(math.inf) #setting the edge length of the router to infinity
                if neighbour.router_name == router_name: #if this is the router to be removed then remove the router.
                    remove_edges.append(neighbour)

        #Removes the connections to the removes router.
        for router in self.graph.router_dict: #Gets the routers in the graph
            for edges in remove_edges: #Iterates through the remove list
                if edges in self.graph.router_dict[router].connectioned_routers: #If the edge is a connection to the existing router then remove the connection.
                    self.graph.router_dict[router].connectioned_routers.pop(edges) #Connection is removed from the graph.
        self.graph.router_dict.pop(router_name) # Router is removed from the graph.

        self.print_routing_table() #Print the routing table.



    #Creates a visual graph using the information from the routing table.
    def map_out_graph(self, G):
        #Iterates through the routing table to create the nodes and edges of the graph with its respective weights and names.
        for router in self.graph.router_dict:
            for connected_router in self.graph.router_dict[router].connectioned_routers:
                start = router
                goal = connected_router.router_name
                cost = self.graph.router_dict[router].get_weight(connected_router)
                G.add_edge(start, goal, cost=cost)

        routers = [(start, goal) for (start, goal, d) in G.edges(data=True)]

        position = nx.spring_layout(G, scale=2) #Generates a dictionary of nodes with their associated weights usding an inbuilt function.
        nx.draw_networkx_nodes(G, position, node_color="Red", node_size=800) #Draws the nodes to the table with the customisations inputted.
        edge_value = nx.get_edge_attributes(G,'cost') #Gets the edge values in the graph and stores them.
        nx.draw_networkx_edge_labels(G, position, edge_labels = edge_value) #This adds the weight lables to the edges on the graph.
        nx.draw_networkx_edges(G, position, edgelist=routers, width=7, alpha=0.5, edge_color="blue", style="dashed") #This draws the connections between each node and allows difftent designs.
        nx.draw_networkx_labels(G, position, font_size=19, font_color="oldlace",font_weight="bold", font_family="sans-serif") #Allows us to label the nodes.



        plt.draw() #Plots the graph.
        plt.show() #Displays the graph on the screen.


class Graph:
    def __init__(self):
        self.router_dict = {} # Router table that contains all the inforamtion about the routers and edge lengths between routers.
        self.router_total = 0 # Keeps count of the number of active routers.

    # Creates a new router and adds it to the routing table.
    def add_router(self, router):
        new_router = Router(router) # Creates an object for a router.
        self.router_dict[router] = new_router # adds to the router_dict which is a dictionary with all routers and router edge costs.
        self.router_total = self.router_total + 1 # Increments the router count by one.
        return new_router

    #Creates an edges between two routers that is multi-directional.
    def add_edge(self, start, goal, cost=0):
        if start not in self.router_dict: #Check if the router is already in the router dictionary (Routing table).
            self.add_router(start) # Adds router to the router table.
        if goal not in self.router_dict: #Check if the router is already in the router dictionary (Routing table).
            self.add_router(goal) # Adds router to the router table.

        #Creates a multi-directional graph.
        self.router_dict[start].add_connections(self.router_dict[goal], cost) #adds the connections and cost between two routers.
        self.router_dict[goal].add_connections(self.router_dict[start], cost)

def main():

    #Creates adds edges to the routing table.
    graph = Graph()
    G=nx.Graph() #Networkx initation of the graph.
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


    router.get_path("f")

    router.print_routing_table()
    router_two.print_routing_table()
    router_two.remove_router("c")
    router_two.print_routing_table()


    #Nice little extra: Using Networkx to graph the router relationships.
    router_two.map_out_graph(G)



if __name__ == '__main__':
    main()
