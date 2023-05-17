from queue import Queue

from .graph import Graph


# BFS for component
def bfs(graph: Graph, src: int) -> list:
    visited = set() 
    bfs_traversal = list()
    queue = Queue()
    
    queue.put(src)
    visited.add(src)
    
    while queue:
        curr_vertex = queue.get()
        bfs_traversal.append(curr_vertex)
        
        for neighbour in graph.adj(curr_vertex).keys():
            if neighbour not in visited:
                visited.add(neighbour)
                queue.put(neighbour)

    return bfs_traversal

# Average clustering coefficient
def average_clustering(graph: Graph, vertexId: int) -> float:
    cl = 0
    vertices = bfs(graph, vertexId)

    for vertex in vertices:
        neighbors = graph.adj(vertex).keys()
        degree = len(neighbors)

        if (degree < 2):
            continue

        edges_neighbors_count = 0
        visited_neighbors = set([vertex])

        for neighbor in neighbors:
            curr_neighbors = graph.adj(neighbor).keys()

            for item in curr_neighbors:
                if (item not in visited_neighbors & item in neighbors):
                    edges_neighbors_count += 1
                    visited_neighbors.add(item)

        cl += (2 * edges_neighbors_count)/(degree * (degree - 1))

    cl /= len(vertices)

    return cl

# Degree assortativity
def degree_assortativity(graph: Graph) -> float:
    M = 1 / graph.edges_count
    vertices = graph.vertices()
    visited = set()
    sum_mult = 0
    sum_halfsum = 0
    sum_sumsquares = 0

    for vertex in vertices:
        edges = graph.adj(vertex)
        neighbors = edges.keys()
        degree = len(neighbors)

        for neighbor in neighbors:
            key = edges[neighbor][0]

            if (key in visited):
                continue

            curr_degree = len(graph.adj(neighbor).keys())

            sum_mult += degree * curr_degree
            sum_halfsum += 0.5 * (degree + curr_degree)
            sum_sumsquares += 0.5 * (degree * degree + curr_degree * curr_degree)

            visited.add(key)

    arg = M * (sum_halfsum * sum_halfsum)
    r = (sum_mult - arg) / (sum_sumsquares - arg)

    return r
