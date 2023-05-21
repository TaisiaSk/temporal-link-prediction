from queue import Queue
from graph.Graph import Graph


# BFS for component
def bfs(graph: Graph, src: int) -> list:
    visited = set()
    bfs_traversal = list()
    queue = Queue()

    queue.put(src)
    visited.add(src)

    while (not queue.empty()):
        curr_vertex = queue.get()
        bfs_traversal.append(curr_vertex)
        edges = graph.adj(curr_vertex)

        if (not edges):
            continue

        for neighbour in edges:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.put(neighbour)

    return bfs_traversal

# Average clustering coefficient
def average_clustering(graph: Graph, vertexId: int) -> float:
    cl = 0
    vertices = bfs(graph, vertexId)

    for vertex in vertices:
        neighbors = graph.adj(vertex)
        degree = len(neighbors)

        if (degree < 2):
            continue

        edges_neighbors_count = 0
        visited_neighbors = set()

        for neighbor in neighbors:
            curr_neighbors = graph.adj(neighbor)

            for item in curr_neighbors:
                if ((item not in visited_neighbors) and (item in neighbors)):
                    edges_neighbors_count += 1
            
            visited_neighbors.add(neighbor)

        cl += (2 * edges_neighbors_count)/(degree * (degree - 1))

    cl /= len(vertices)

    return cl
