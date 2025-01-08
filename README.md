# Router Graph and Shortest Path Finder

## Overview

This repository contains a Python-based program for simulating and managing a network of routers. It uses Dijkstra's algorithm to find the shortest path between routers, create routing tables, and visualize the network using NetworkX and Matplotlib. The system is designed for educational purposes to understand routing and shortest path algorithms in computer networks.

## Features

1. **Graph Representation**:
   - Models routers and connections as a graph where nodes represent routers and edges represent connections.

2. **Shortest Path Calculation**:
   - Uses Dijkstra's algorithm to compute the shortest path between routers.

3. **Routing Table Generation**:
   - Automatically generates routing tables for each router.

4. **Router Removal**:
   - Dynamically removes routers from the network and updates the routing tables.

5. **Network Visualization**:
   - Creates a graphical representation of the network with routers and connections.

6. **Flexible Configuration**:
   - Easily configurable to add new routers, connections, or modify existing ones.

## Prerequisites

- Python 3.x
- Libraries:
  - `networkx`
  - `matplotlib`
  - `pandas`

Install the required libraries using:
```bash
pip install networkx matplotlib pandas
```

## Project Structure

- **`Router` Class**:
  - Handles operations related to a single router, including connections and edge costs.
  - Implements Dijkstra's algorithm to find the shortest path.
  - Maintains and prints routing tables.
  - Visualizes the graph structure using NetworkX.

- **`Graph` Class**:
  - Manages the entire network of routers.
  - Supports adding routers and edges (connections).

- **`main` Function**:
  - Demonstrates usage by creating a sample network, calculating shortest paths, and visualizing the graph.

## Usage

1. **Initialize the Graph**:
   ```python
   graph = Graph()
   ```

2. **Add Routers and Connections**:
   ```python
   graph.add_edge("a", "b", 7)
   graph.add_edge("a", "c", 9)
   graph.add_edge("b", "c", 10)
   ```

3. **Create Routers**:
   ```python
   router = Router("a", graph)
   router_two = Router("b", graph)
   ```

4. **Calculate Shortest Path**:
   ```python
   router.get_path("f")
   ```

5. **Print Routing Table**:
   ```python
   router.print_routing_table()
   ```

6. **Remove Router**:
   ```python
   router_two.remove_router("c")
   ```

7. **Visualize Network**:
   ```python
   G = nx.Graph()
   router_two.map_out_graph(G)
   ```

## Example Output

### Shortest Path
**Input**:
```python
router.get_path("f")
```
**Output**:
```
Start: a
End: f
Path: a->c->f
Cost: 11
```

### Routing Table
**Input**:
```python
router.print_routing_table()
```
**Output**:
```
   from  to  cost       path
0     a   b     7         a->b
1     a   c     9         a->c
2     a   d    20    a->c->d
3     a   e    26    a->c->d->e
4     a   f    11      a->c->f
```

## Visualization
- Displays the network graph with nodes (routers) and edges (connections).
- Labels nodes and edges with names and weights, respectively.

## Contribution

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes and push them to your fork.
4. Open a pull request describing your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enhance your understanding of routing algorithms and graph visualization with this Router Graph and Shortest Path Finder!

