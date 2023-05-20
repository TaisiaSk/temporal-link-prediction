from queue import Queue
from graph.graph import Graph


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

# Degree assortativity
def degree_assortativity(graph: Graph) -> float:
    edges_count = 0
    vertices = graph.vertices()
    visited = set()
    sum_mult = 0
    sum_sum = 0
    sum_sumsquares = 0

    for vertex in vertices:
        neighbors = graph.adj(vertex)
        degree = len(neighbors)

        for neighbor in neighbors:
            if (neighbor in visited):
                continue

            curr_degree = len(graph.adj(neighbor))

            sum_mult += degree * curr_degree
            sum_sum += degree + curr_degree
            sum_sumsquares += degree ** 2 + curr_degree ** 2

            edges_count += 1

        visited.add(vertex)

    M = 1 / edges_count
    arg = M * ((0.5 * sum_sum) ** 2)
    r = (sum_mult - arg) / (0.5 * sum_sumsquares - arg)

    return r
