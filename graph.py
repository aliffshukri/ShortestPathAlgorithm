import tkinter as tk
from tkinter import ttk
import heapq

class Graph:
    def __init__(self, graph):
        self.graph = graph

    def dijkstra(self, start, end):
        pq = []
        heapq.heappush(pq, (0, start))
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        predecessors = {vertex: None for vertex in self.graph}

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        path = self._construct_path(predecessors, start, end)
        return distances[end], path

    def bellman_ford(self, start, end):
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        predecessors = {vertex: None for vertex in self.graph}

        for _ in range(len(self.graph) - 1):
            for vertex in self.graph:
                for neighbor, weight in self.graph[vertex].items():
                    if distances[vertex] + weight < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + weight
                        predecessors[neighbor] = vertex

        # Check for negative weight cycles
        for vertex in self.graph:
            for neighbor, weight in self.graph[vertex].items():
                if distances[vertex] + weight < distances[neighbor]:
                    raise ValueError("Graph contains a negative weight cycle")

        path = self._construct_path(predecessors, start, end)
        return distances[end], path

    def floyd_warshall(self):
        vertices = list(self.graph.keys())
        distance = {vertex: {vertex2: float('infinity') for vertex2 in vertices} for vertex in vertices}
        next_node = {vertex: {vertex2: None for vertex2 in vertices} for vertex in vertices}

        for vertex in vertices:
            distance[vertex][vertex] = 0

        for vertex in self.graph:
            for neighbor, weight in self.graph[vertex].items():
                distance[vertex][neighbor] = weight
                next_node[vertex][neighbor] = neighbor

        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if distance[i][j] > distance[i][k] + distance[k][j]:
                        distance[i][j] = distance[i][k] + distance[k][j]
                        next_node[i][j] = next_node[i][k]

        return distance, next_node

    def floyd_warshall_path(self, start, end):
        distance, next_node = self.floyd_warshall()
        if next_node[start][end] is None:
            return float('infinity'), []
        path = self._construct_fw_path(next_node, start, end)
        return distance[start][end], path

    def _construct_path(self, predecessors, start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        if path[0] == start:
            return path
        else:
            return []

    def _construct_fw_path(self, next_node, start, end):
        path = []
        while start != end:
            path.append(start)
            start = next_node[start][end]
        path.append(end)
        return path

# Define the graph with points and distances
graph_data = {
    'A': {'B': 11, 'C': 14, 'E': 33},  # Kuala Lumpur
    'B': {'A': 11, 'D': 78, 'F': 47, 'G': 117},  # Ampang
    'C': {'A': 14, 'D': 66},  # Batu Caves
    'D': {'C': 66, 'B': 78, 'G': 99},  # Karak
    'E': {'A': 33, 'F': 29},  # Cyberjaya
    'F': {'B': 47, 'E': 29, 'G': 85, 'I': 147},  # Nilai
    'G': {'B': 117, 'D': 99, 'F': 85, 'H': 69},  # Bahau
    'H': {'G': 69, 'I': 79, 'J': 101},  # Segamat
    'I': {'F': 147, 'H': 79, 'J': 72},  # Muar
    'J': {'H': 101, 'I': 72}  # UTHM
}


# Note for reference
node_notes = {
    'A': 'Kuala Lumpur',
    'B': 'Ampang',
    'C': 'Batu Caves',
    'D': 'Karak',
    'E': 'Cyberjaya',
    'F': 'Nilai',
    'G': 'Bahau',
    'H': 'Segamat',
    'I': 'Muar',
    'J': 'UTHM',
}

# Create the Graph object
graph = Graph(graph_data)

# Create the main window
root = tk.Tk()
root.title("Shortest Path Finder")

# Dropdown for selecting start and end points
points = list(graph_data.keys())

# Function to find the shortest path and update the GUI
def find_shortest_path():
    start = start_var.get()
    end = end_var.get()
    algorithm = algorithm_var.get()

    if start == end:
        result_var.set("Start and End points are the same.")
        return

    try:
        if algorithm == "Dijkstra":
            distance, path = graph.dijkstra(start, end)
        elif algorithm == "Bellman-Ford":
            distance, path = graph.bellman_ford(start, end)
        elif algorithm == "Floyd-Warshall":
            distance, path = graph.floyd_warshall_path(start, end)
        
        if distance == float('infinity'):
            result = "No path found."
        else:
            result = f"Shortest distance: {distance}\nPath: {' -> '.join(path)}"
            draw_path(path)
        
        result_var.set(result)
    except ValueError as e:
        result_var.set(str(e))

# Function to draw the nodes and edges on the canvas
def draw_graph():
    canvas.delete("all")
    for node, coordinates in node_coordinates.items():
        x, y = coordinates
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue")
        canvas.create_text(x, y, text=node, fill="white")
    
    for start in graph_data:
        for end in graph_data[start]:
            x1, y1 = node_coordinates[start]
            x2, y2 = node_coordinates[end]
            canvas.create_line(x1, y1, x2, y2, fill="black")

# Function to highlight the shortest path on the canvas
def draw_path(path):
    draw_graph()  # Redraw the base graph
    for i in range(len(path) - 1):
        x1, y1 = node_coordinates[path[i]]
        x2, y2 = node_coordinates[path[i+1]]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

# Coordinates for each node (for visual representation)
node_coordinates = {
    'A': (100, 100),
    'B': (150, 90),
    'C': (120, 50),
    'D': (230, 30),
    'E': (100, 160),
    'F': (180, 190),
    'G': (330, 100),
    'H': (360, 200),
    'I': (310, 280),
    'J': (380, 300)
}

# Start point dropdown
tk.Label(root, text="Start Point").grid(row=0, column=1, padx=10, pady=10)
start_var = tk.StringVar(value=points[0])
start_menu = ttk.Combobox(root, textvariable=start_var, values=points)
start_menu.grid(row=0, column=2, padx=10, pady=10)

# End point dropdown
tk.Label(root, text="End Point").grid(row=1, column=1, padx=10, pady=10)
end_var = tk.StringVar(value=points[0])
end_menu = ttk.Combobox(root, textvariable=end_var, values=points)
end_menu.grid(row=1, column=2, padx=10, pady=10)

# Algorithm selection dropdown
tk.Label(root, text="Algorithm").grid(row=2, column=1, padx=10, pady=10)
algorithm_var = tk.StringVar(value="Dijkstra")
algorithm_menu = ttk.Combobox(root, textvariable=algorithm_var, values=["Dijkstra", "Bellman-Ford", "Floyd-Warshall"])
algorithm_menu.grid(row=2, column=2, padx=10, pady=10)

# Find button
find_button = tk.Button(root, text="Find Shortest Path", command=find_shortest_path)
find_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Result field
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, wraplength=400, justify="left")
result_label.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Canvas for graph visualization
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

# Draw the initial graph
draw_graph()

# Run the GUI event loop
root.mainloop()

