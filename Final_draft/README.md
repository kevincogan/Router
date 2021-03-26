CA304 - Assignment 2 - Fancy Little Extra - Networkx Graph of the router relationships.

To graph the current active routers and their relationships use the <router>.map_out_graph(G)
the <router> section of the function is the name of the router you have created
and the G is a variable assignment for nx.Graph() for example:



router = Router("a", graph)



G = nx.Graph()



Once you have completed these steps you can now run the program and the graph of the current
relationships between the routers will be generated and displayed on screen in a stylish manner.
The graph will updates automatically when routers are removed/die or the costs between routers
change.
